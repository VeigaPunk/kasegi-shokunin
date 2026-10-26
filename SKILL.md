---
name: kasegi-shokunin
description: Domain specialist — bounty & security research — scopes ~/Projects/bounties, program rules, claim packages. Rank: shonen.
---

# kasegi-shokunin — bounty & security research craft

**Round-15 status of the ground truth.** This skill was grounded in
`/home/vgpnk/Projects/bounties` (UFO fleet HQ): 274 program dirs / 295
packages (280 status-gated) under `claims/`, 1088 program records under
`bounty-map/programs/`, a 486-line verdict ledger at
`docs/review-verdicts.jsonl`, and the operator-facing queue at
`docs/claim-ready-index.md`. **That tree was removed from the filesystem at
2026-09-28T23:51:31Z** (actor UNDETERMINED, data PRESUMED-LOST locally;
detection, timeline, forensics and the per-file provenance of what survives:
`corpus/knowledge/source-tree-loss-2026-09-28.md`). Every rule below still
cites a file — but as of round 15 each citation resolves against one of three
bases, named per block: the frozen 2026-09-05 mirror
`~/Projects/the-bounty-hunter` HEAD `1cfbd86` (ops code — **ABSENT since
2026-10-12**; recorded claims remain, see below), the
other surviving root `~/Projects/origin-work/open-bug-bounties` (26 claim
packages + `submission-review/` receipts + 43 `.ufo-missions` + `data/*.json`
inventories — **also ABSENT since 2026-10-12**), or the lost tree, marked
`[lost-tree] <path>:<line>` and
[corpus-attested as-of 2026-09-28T23:32Z]. **Round-19 re-census (2026-10-14):**
both surviving roots are gone — `~/Projects/the-bounty-hunter` and the whole
`~/Projects/origin-work` tree (no relocated copy found under `~`; the third
tree, `ufo-fsd-alpha`, relocated intact to `~/Projects/ufo-fsd-alpha` @
`964f443e`). Citations that resolved against them are now marked
`[lost-base] <path>:<line>` — a second loss class, same semantics as
`[lost-tree]` (recorded, never checked, never counts as verified) — evidence:
`corpus/knowledge/root-loss-2026-10-12.md`. Counts that came from the lost DATA
`PROVINCE.md` re-points is an open L0 question (`.ufo/l0-questions.md`,
kasegi round-15 row).

## Pipeline (observed, not invented)

```
policy read (AR14, passive only)          → evidence/<program>/scope-snapshot.json
authorization envelope from scope bytes   → evidence/authorization-envelope.json
custodian decision per action             → evidence/custodian/*.decision.json
hunt (local/static preferred)             → evidence/hunt-*.md, poc/
package wrap (positive or honest-zero)    → claims/<program>/<slug>/ (six-file contract)
package validator                         → ops/claim-check.mjs  (fail-closed)
payload staging, deterministic            → ops/prepare-claims.mjs → submit-payload.json
operator queue                            → node ops/claim-index.mjs → docs/claim-ready-index.md
submission                                → OPERATOR ONLY, never automated (decree 2026-09-05)
```

Mission contract: `fleets/mission-template.md` — the L1 judge prompt. The only
standing grant is one bounded passive policy read (AR14). Everything else needs
a grant derived from verbatim policy text.

## Program-rule checklist (step 1 of any mission)

Fill `evidence/<program>/scope-snapshot.json` — observed schema
(`[lost-tree] claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json:1-57`,
18 top-level keys; the bullets below name 10, the rest are listed after):

- [ ] `url`, `fetched_at`, `content_sha256` of the official policy page
      (`…/scope-snapshot.json:2-4`; hash basis = sanitized capture, 5
      volatile nonces replaced — `:21`, `:26`)
- [ ] `in_scope_assets[]` — exact asset names. Generic prose ("we invite you
      to test our web applications") is NOT an asset: `:5` records `[]` while
      `:18` holds exactly that invitation as the grant; `:56` — `[]` means
      "none observed", never "program has no scope"
- [ ] `out_of_scope[]` + `prohibitions_verbatim[]` — copy the text, do not
      paraphrase (SEEK's four, one per line: no automated tooling `:10`,
      customer instances forbidden `:11` (mirrored in `out_of_scope[]` `:7`),
      @bugcrowdninja.com identity required `:12`, AI-generated reports
      rejected `:13`)
- [ ] `testing_grant_verbatim[]` — the sentence that grants testing, verbatim
      (`:17-19`; a non-empty grant beside `in_scope_assets: []` is
      `coverage.status:"incomplete"` `:30` + `scope_decision` "PARKED at
      SCOPED" `:54`)
- [ ] `safe_harbor` — record `null` when absent (`:15`); distinguish SEAL
      Whitehat (active exploits only —
      `[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:14-15`,
      `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:34-35`) from a routine-research safe harbor
- [ ] `reward_table_url`, reward band, currency — round-14 correction: the
      SEEK exemplar carries only `reward_table_url` (`:16`, null); band +
      currency keys live in other snapshots
      (`[lost-tree] evidence/hackerone-starbucks-japan/scope-snapshot.json:112-118`
      reward_table 150/500/1500/3000, `currency:"USD"` `:117`;
      `[lost-tree] evidence/sherlock-106/scope-snapshot.json:12-15` max_reward 100000
      USDC); 29/785 snapshots carry a `currency` key
- [ ] `coverage.status` — `incomplete` when the fetch is a login shell
      (`:29-31`); second observed value `insufficient_for_authorization`
      (`[lost-tree] claims/bugcrowd-opus-guard-market/honest-zero/evidence/scope-snapshot.json:24`);
      `coverage.missing[]` names exactly what was absent (`:38-43`, 4 items);
      58/785 snapshots carry `coverage.status` (round-14 census)

Remaining top-level keys of the exemplar, carrying the anti-fabrication
semantics: `normalized_scope_sha256` `:20`, `content_hash_basis` `:21`,
`sanitized_observation` `:22-28` (`raw_capture_retained:false` `:27`),
`authenticity` `:45`, `retrieval` `:46-53` (`credentials_used`,
`accounts_created`, `terms_accepted` all false `:50-52`), `scope_decision`
`:54`, `prior_snapshot_artifact_sha256` `:55`, `notes` `:56`.

Program quirks to check before planning work:
submission fee (Cantina Pendle: $100 —
`[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:18`
`submissionFee: $100`; `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:9`
makes a live-balance check the claimability gate; `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:27-28`
and `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:52` are the do-not-pay-until rules), KYC
requirement (`[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:18` `kycRequired: false`,
`[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:36`), AI-disclosure requirement
(`[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:33`,
`[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:31`), evidence-source parity
(deployed bytecode ↔ repo commit —
`[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:19-20` names commit `f242659`;
round-14 correction: `provenance.json.pin` has four observed shapes —
structured block `[lost-tree] claims/cantina-pendle/ingestion-20260915/provenance.json:27-31`
{remote, commit, note}, bare string
`[lost-tree] claims/hackerone-wordpress/honest-zero-wp-cli/provenance.json:8`,
nested in `commands[]`
`[lost-tree] claims/hackerone-anthropic/honest-zero-claude-code/provenance.json:29`,
version pin `"0.2.9"`
`[lost-tree] claims/hackerone-airtable/honest-zero-mcp-cli/provenance.json:32`).
Per-program pattern list: `corpus/knowledge/program-quirks.md:10` (fee gate),
`:13` (vulnerable-pattern OOS), `:17` (SEAL), `:19` (`kycRequired`), `:24`
(sampled siblings).

### Policy access playbook (fleet-learned)

| Platform | Reality | Move |
|---|---|---|
| HackerOne | HTML is a JS shell; `/policy` can 403 unauthenticated (`[lost-tree] docs/autopsies/hackerone-figma.md:6` `403 sign_in` + `figma.json 404`) | Public GraphQL `team(handle)` query — policy/scope/structured_scopes, no auth (`[lost-tree] evidence/paypal-bug-bounty/provenance.json:27` POST → `HTTP 200` `policy_len 25844`; query envelope `[lost-tree] evidence/hackerone-1password/fetch-evidence/graphql-request-20260905T165623Z.json:2`) |
| Bugcrowd | Auth-walled SPA for anonymous fetches (`[lost-tree] evidence/bugcrowd-barracuda/scope-snapshot.json:11` HTTP 200 React shell) | Try public brief/changelog JSON once — `engagement_known_issues.json` 401 (`[lost-tree] evidence/bugcrowd-barracuda/scope-snapshot.json:42`, `[lost-tree] evidence/bugcrowd-asana/scope-snapshot.json:12`), brief doc 404 (`[lost-tree] docs/autopsies/bugcrowd-openai.md:6`, `[lost-tree] docs/autopsies/bugcrowd-spacex.md:6`, `[lost-tree] docs/autopsies/bugcrowd-blofin-crypto-mbb-og.md:6`; 401+406+404 combined `[lost-tree] docs/continuation-notes.md:50`); else park at SCOPED (`[lost-tree] claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json:54`), don't burn budget |
| Immunefi/Cantina/HackenProof | Public bounty pages with contract scope (`[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:9` deployments JSON keys + whitelisted markets) | Capture page HTML into `evidence/` (pendle `[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:37`); hash it (`policy_sha256` — pendle `[lost-tree] claims/cantina-pendle/ingestion-20260915/provenance.json:32-33`, `[lost-tree] claims/hackenproof-atomone/honest-zero-atomone/provenance.json:36`; round-14 correction: no provenance page hash on Immunefi ingestions — `claims/immunefi-beanstalk/ingestion-20260915/provenance.json` has zero hash keys; their page hashes land as `html_sha256` in `[lost-tree] .ufo/bounty-fleet/ledger/telemetry.jsonl:181`) |
| RFC 9116 security.txt | A stub is not a scope (`[lost-tree] evidence/bugcrowd-asana/scope-snapshot.json:12` Contact/Policy → bugcrowd stub, Expires 2026-12-31, no assets) | No assets + no grant → park (`[lost-tree] evidence/bugcrowd-barracuda/scope-snapshot.json:45` 404 "no RFC 9116 security.txt") |
| Terms-gated policy (SIX Group) | Reading requires accepting Program Rules (`[lost-tree] docs/autopsies/hackerone-six-group.md:6` reason verbatim) | Terms acceptance is a forbidden external effect → autopsy + retire (`:3` `RETIRED (structurally blocked)`; `corpus/knowledge/policy-access-playbook.md:13`) |

## Finding-triage decision table

Terminal classes observed across 486 non-claim-ready missions
(`docs/continuation-notes.md`) and the claim queue:

| Condition | Class | Package state | Evidence |
|---|---|---|---|
| In-scope finding, reproducible locally, reviewer APPROVED, all gates PASS | Claimable | `status.json state:"DONE", claimable:true` | `docs/claim-ready-index.md` (12 queued — round-14 note: the on-disk file is STALE: generated stamp `:3` = 2026-09-06T01:35:16Z, 11 rows; the 12th claim-check-OK package `claims/intigriti-yahoo/ingestion-20260914` (DONE + `claimable:true`, `[lost-tree] claims/intigriti-yahoo/ingestion-20260914/status.json:2`, `[lost-tree] claims/intigriti-yahoo/ingestion-20260914/status.json:11`) appears only on live regeneration) |

| Defect proven, live precondition unverified (e.g. needs read-only chain/state check) | Positive-blocked | `state:"BLOCKED", verdict:"positive-blocked-*", claimable:false`, `resume_condition` set | `claims/cantina-pendle/ingestion-20260915/status.json` — exactly 2 attested instances (+ cantina-dydx); free-form verdict string: no schema defines it, claim-check.mjs:169's not-claimable regex doesn't recognize it (round-13 annotation) |
| Finding needs operator-owned substrate (VM, device, account) | Positive-blocked | `submit/BLOCKED.md` names the exact gate | `claims/hackerone-3cx/…` (uid=0 disposable-VM capture) |
| Bounded negative result: authorized surface tried, nothing claimable | LEARNED honest-zero (438/486) | `state:"BLOCKED", verdict:"honest-zero-*", finding_count:0`, `submit/BLOCKED.md` | `claims/bugcrowd-seek/honest-zero/` |
| Scope never verifiable (auth wall, SPA shell, terms gate) | RETIRED auth-walled (19/486) | `docs/autopsies/<program>.md` + parked status | `docs/autopsies/bugcrowd-openai.md` |
| Mission broke on infra/quota, not on evidence | FAILED-infra (26/486) | `mission_failed` telemetry; fix is status reconciliation, not new testing | `docs/continuation-notes.md` class table |
| Live path exists (new public input, exhausted model route reset) | RETRY / `continue` | verdict `continue` + exact `next_step` | `docs/review-verdicts.jsonl` (430 leave / 50 continue / 6 drop) |

Verdict rule from `fleets/review-mission.md`: **drop** = dead end, **continue**
= name the one executable next step, **leave** = don't touch again. "Leave" is
the default: 430/486.
`claim-check.mjs` enforces all of it (authoritative list:
`corpus/knowledge/claim-gates.md`): required-file presence, `report.md`
"Scope excerpt" + "no submission performed" markers, per-artifact sha256 +
path/symlink confinement + same-digest redaction receipts (producer ≠
verifier), non-empty custodian chain where every `scope_signal` is exactly
`NO_SCOPE_OBJECTION` and `head_sha256` == last decision ==
`manifest.expected_head_sha256`, a secrets regex over all package text, and
`status.json` — `DONE` + `claimable:true` + `finding_count≥1` +
`manifest_sha256` binding + `APPROVED` review by a distinct `kx-reviewer`
(role, requested/resolved model, fallback flag) + four hard gates + two
subchecks PASS + not-claimable heuristics + a global duplicate-submission scan
across all `claims/*/*/status.json` + `submit/BLOCKED.md` and nested-readiness
blockers. `prepare-claims.mjs` then stages `submit-payload.json` only for
passing DONE packages with an explicit https route, attaches
`claim_checklist.md` + positive-polarity artifacts only, refuses to rewrite a
manifest-bound payload without re-review, and restores original bytes if the
post-write recheck fails.

## Intake surface — the map is decorative, ingestion is hidden

`bounty-map/programs/*.json` (1088 records, one import
`refresh-20260829T190850329Z`, nothing since) is **not** mission state:
`mission_state` is DISCOVERED×1087/PLANNED×1 and read only for a `--dry`
log line; `lane` is `executor`×1088; `ev_inputs` non-empty×1; the `reward`
object exists on 48 records (all `source_kind=independent`) but numeric
`reward.min` on only 14 (round-13 correction) — `ev-report.mjs` prints
UNKNOWN for 1087 programs. `check-freshness.mjs` live exit 1: all three
board datasets 358 h stale at round 11, 359.4 h at the round-13 live re-run
(the counter grows between runs; 26 h threshold, AR4 alarm standing).
Dispatch ordering (`buildQueue`, fleet-dispatch.mjs:88,110) is five-termed:
`priority(9e12) > continue(2e12) > curated(1e12, boolean on non-empty
ev_inputs) > reward.min×1000 > is_live(1)` (round-13 correction: earlier
text omitted `is_live(1)`) — exactly 1024 of 1088 records score 0 (796) or
1 (228), so for 94.1% of the map ordering degenerates to readdir order;
`priority.json` (14) is a strict subset of the 50 continue programs, so the
9e12 tier only breaks ties inside the continue cohort. Canonical derivation:
`corpus/knowledge/triage-thresholds.md`. Real state is
`ledger/missions.jsonl` + `fleets/run/`, real termination is
status-file TERMINAL + telemetry `attempts()≥2`.

Two intake paths: `import-board.mjs` writes the map (evidence-bound);
the `.ufo-ingestion/` cycle (2026-09-14, 16 scouts rerouted off a grok
403 onto `devin/swe-2:max`) EV-ranked 32 programs and seeded 13 directly
into `claims/<slug>/ingestion-20260914/` — 7 of the 12 queue rows.
**Round-13 correction:** the seeding bypassed the map for only 4 of the 13
slugs (spacex-starlink, yahoo, monzo, personio); the other 9 have map
records. The 22 map-less claims dirs = 4 seeded + 18 archive-era (incl. all
Cantina/immunefi dirs). Name-drift joins: map `bugcrowd-spacex`
vs claims `bugcrowd-spacex-starlink`; map `github-bug-bounty` (the one
curated record) vs claims `github-bounty`. Cycle 2 never ran — its
deferred/queued frontier (~80 programs) is enumerated in
`cycle-20260914T171257Z.md`. `.ufo-ingestion/claim-tracker.py` is a dead
third watcher (READY.md/no-BLOCKED.md, weaker than claim-check) that also
scans the origin-work claim-packages tree; `tracker.log` last line
2026-09-14T17:24:52Z — the "20:40Z" recorded in earlier rounds is the `.md`
snapshot's mtime (17:40:15 -0300 = 20:40:15Z), not a tracker cycle
(round-13 correction).

`fleets/registry.json` is in-domain: the `operator_decrees` block is the
authoritative decree ledger — filing order (mozilla→spotify→airtable→
intel), **3cx never-submitted decree** (free disclosure pending rep),
intel hold (no Intigriti KYC), freebie-class ATTRIBUTED not anonymous
(supersedes the anonymity clause — anthropic), paid track =
`vgpnk1337`(H1)/`veigapunk`(Intigriti) operator accounts, severity-
evidence-trail requirement. The file accretes with in-place `superseded`
markers (astra is simultaneously doctrine-banned and LIVE-routed;
`(parked until 2026-09-07)` bucket notes are stale vs `PARKED=[]`).
Authoritative detail: `corpus/knowledge/intake-surface.md`.

## Mission ledger & audit store

`ledger/missions.jsonl` is the append-only hunter-contract state machine
(writer: `ops/shared.mjs::appendLedger`, 3500-byte line cap for O_APPEND
atomicity). Transition census (718 lines / 260 missions):
`SCOPED` 232 → `PLANNED` 219 → `LEARNED` 244 dominates;
`SCOPED→PLANNED→LEARNED` alone is 207 missions. Deep path
`EXECUTED→EVIDENCED→VERIFIED→SUBMISSION_PREPARED` is rare; `SUBMITTED` (3)
and `DISCLOSED_FREE` are operator-attributed ledger facts, never fleet
actions. `ledger/telemetry.jsonl` (7,224 lines as of 2026-09-28; append-only — treat line counts as-of their date) is the dispatcher heartbeat
(`dispatcher_tick`, `mission_parked`, `claim_commit_failed`,
`model_reroute`, `operator_decree`…). `ledger/candidates.jsonl` is
`the-bounty-hunter` intake (run_id `b1k-NNN`); `ledger/imports.jsonl` binds
board imports to an `evidence_id` (fail-closed in `import-board.mjs`).
`rank.mjs` emits `rankings-<ts>.json` with `inputs_basis:"curated"` vs
`default_estimate` priors.

`evidence/<program-id>/` (592 dirs) is the per-program audit store —
`scope-snapshot.json` 583, `authorization-envelope.json` 580, `provenance`
532, `custodian-receipts` 514, `honest-zero-record.json` (schema
`honest-zero/v1`) 346, `status.json` 275 — plus `raw/` fetched bytes,
`history/` superseded envelopes, `custodian/` input+decision pairs,
`b1k-NNN/` per-run output. Distinct tree from `claims/*/*/evidence/`:
missions append freely; the strict manifest contract applies only inside a
claim package. Authoritative detail: `corpus/knowledge/mission-ledger.md`,
`corpus/knowledge/evidence-dir.md`.

## Mission control plane

`ops/fleet-dispatch.mjs` is the `/loop` engine: tmux panes under
`ufo_sighting:fleet-grid`, 2 h leases in `fleets/leases.json`, slot
rotation on terminal status, `reconcile()` rebuilds from leases + pane
titles on restart. Queue score = priority(9e12) > continue(2e12) >
curated(1e12) > reward.min×1000 > is_live(1) (round-13 correction: five
terms; `curated` is a boolean on non-empty `ev_inputs`, never an EV
magnitude) — EV orders, never gates (AR12). Dispatcher
is the sole committer to `claims/` (P21) gated on fresh `claim-check.mjs`
(P20), tags `claim-ready/<id>/<slug>` and pushes atomically after proving
the tagged commit's bytes match (`claim_tag_rejected` telemetry on
mismatch). Mission L1s are 584 generated `fleets/missions/<program>.md`
assignments reporting back through the file protocol
`fleets/run/<program>.status.json` (703 files: PARKED 646, DONE 27,
SCOPING 20, RETIRED 6, plus `_`-prefixed seat statuses). Model routing is a
time-windowed decree (UTC-3 12:00–22:00 → deepseek-v4-pro, else
gpt-6-astra) + strict log-signature limit detection → grok-4.6:low lane.
Sibling L1s: `fleets/claimer-mission.md` (CDP browser submissions,
operator-authed), `fleets/review-mission.md` (486-item drop/continue/leave
sweep). Audit lanes: `.ufo-mission-report-bh*.md` (22 readiness audits:
20 BLOCKED, 2 READY — intigriti-yahoo + hackerone-superhuman, both
claim-check OK), `.ufo-warden/` (readiness dispatch ledger), `.ufo-ingestion/`
(scout cycles + claim-ready tracker over the separate
`origin-work/open-bug-bounties` tree). Resume: `docs/RUNBOOK-resume.md` +
`fleets/state-snapshots/`. Authoritative detail:
`corpus/knowledge/mission-control.md`.

## UFO runtime workspaces — the untracked `.ufo/` layer + `.omp/`

`~/Projects/bounties/.ufo/` (1.5 G, `git ls-files` → 0, mostly *not ignored*) is
the runtime tree no ops tool reads: 25 `bh*` warden-audit workspaces (19
top-level + 6 under `bounty-fleet/sessions/`) vs 22 root reports (19 shared /
3 report-only / 6 workspace-only + 1 phantom dispatch), the 805 M
`bounty-fleet/` keeper tree, 117 M of `sessions/` bpolish transcripts, and two
frozen audits.

- Model provenance = the resolved route at run time: `reroutes.jsonl` (121
  records, every cause a grok/xai 403/429 → `devin/swe-2:max`), not the
  registry pin. The warden's `state.json` is keyed by PROGRAM → re-dispatch
  silently overwrites runIds; the yahoo READY package cites the *superseded*
  runId (provenance split — never prune workspace-only ids).
- `bounty-fleet/` = the bounty-keeper overnight fleet: a second
  `ledger/missions.jsonl` (525 rows / 184 run_ids — a different state machine
  than the root `ledger/`); 265 launched / 249 reported / 184 ledgered — 81
  runs never reached a ledger; two halts (launch_cap@64, night_budget).
- `sessions/bpolish1..8` = omp recorder v3 transcripts (2026-09-15): zero
  submission evidence (`submitted_url` all null; receipts = custodian
  hash-chain); grep trap — `no_submission_performed: true` → 471 false
  positives, 0 real.
- `grok-bounty-assessment-20260911/` = frozen 266-mission reconciliation:
  88.30/100 descriptive (never quote without its
  `BLOCKED_BY_NONCOMPENSABLE_GATES` — `clean_repository_closure` is
  unpassable by construction on a dirty tree), and self-invalidating: its
  validator re-reads live file line-ranges, so re-running it today fails.
- 656 `claims/` files cite `.ufo/…` provenance paths; 51 of 543 JSON refs
  already dangle and `claim-check.mjs` resolves none of them → **copy bytes
  into the package; a `.ufo/` citation is not durable evidence**.
- `.omp/` = the second routing truth (uncommitted `config.yml` rewrites all
  six `fleet_*` roles; `registry-check` RED with 7 violations; 4 non-registry
  cards invisible to every check; `skills/ufo` a drifted fork) — mechanics are
  cross-domain (kumitate/protocol); the bounty consequence is the
  resolved-route rule above.
- Outermost layer: the repo is stalled mid-rebase since before 2026-09-11
  (903 dirty entries) — `gitMutationBlocker` refuses every fleet commit; all
  Sep 7–15 work is working-tree-only (`corpus/knowledge/repo-git-state.md`).

Authoritative detail: `corpus/knowledge/ufo-workspaces.md`, `repo-git-state.md`,
`target-checkouts.md`.

## Ops integrity layer — invariants, intake, finalize

`ops/shared.mjs` (mirror: 41 lines, sha256 `2497578a44e5`) owns the
constants every ops file imports: `BANNED = ['cursor','opencode']`
(`[lost-base] ops/shared.mjs:7`), enforced as a word-boundary scan
`(^|[^a-z])<b>([^a-z]|$)` (`[lost-base] ops/validate.mjs:56`); `PARKED = []` — empty
since the chatgpt park lifted 2026-09-04 (`[lost-base] ops/shared.mjs:8`), which makes
the parked check **vacuous by construction**: `PARKED_TOKEN` falls back to
`/(?!)/`, a never-match (`[lost-base] ops/validate.mjs:28`); `K3_SEATS = ['judge',
'planner']` (`ops/shared.mjs:9`) with the route regex
`/kimi-code\/k3|kimi-k3|moonshot\/kimi-k3/i` (`[lost-base] ops/shared.mjs:11`);
`sha256File` = digest of exact bytes, `null` when absent
(`[lost-base] ops/shared.mjs:25-31`); `appendLedger` caps a line at **3500 bytes** so
concurrent cross-session `O_APPEND` writes stay atomic within POSIX
`PIPE_BUF` (`[lost-base] ops/shared.mjs:33-34`), replaces an oversize entry with a
`truncated:true` stub (`[lost-base] ops/shared.mjs:38`) and appends to
`ledger/<kind>.jsonl` (`[lost-base] ops/shared.mjs:39`). `gitMutationBlocker`
(fail-closed on rebase/merge/cherry-pick or non-main HEAD) is **absent from
the mirror** — 0 hits repo-wide; it existed only in the lost tree
(`[lost-tree] ops/shared.mjs:55`, `corpus/knowledge/ops-invariants.md:24`).

**`TELEMETRY_EVENTS` is a decorative whitelist** (round-15 finding,
mirror-verified): `[lost-base] ops/shared.mjs:13-22` declares 8 event names
(`lane_parked`, `lane_degraded`, `operator_decree`, `xask_dry`,
`board_imported`, `binding_verified`, `reroute_drill`, `provenance_drift`),
but `grep -rn TELEMETRY_EVENTS --include='*.mjs' --include='*.sh'` over the
mirror returns **only that declaration** — nothing imports it, and
`appendLedger` never checks the event name (`[lost-base] ops/shared.mjs:36-41`). The ops
scripts actually append **17** distinct `event:` values (`mission_failed` ×3
sites, `model_reroute` ×2, `claim_rejected` ×2, then `reroute_drill`,
`provenance_drift`, `mission_unparked`, `mission_retired`, `mission_done`,
`mission_dispatched`, `freshness_check`, `fleet_synced`, `finalize_all`,
`dispatcher_tick`, `claims_pushed`, `board_imported`, `binding_verified`,
`attempt_reset`): only 4 of the 17 are whitelisted, and 4 whitelisted names
(the `lane_*`/`operator_decree`/`xask_dry` set) are appended by no ops script
at all — they are lane-side events. Same defect class as the decorative
bounty map: a declared contract with no enforcement point.

`ops/validate.mjs` (130 lines) is a schema-subset + referential gate:
RFC3339 regex `[lost-base] ops/validate.mjs:27`, program `freshness.as_of` must match it
(`[lost-base] ops/validate.mjs:118`), a record's `lane` must exist in
`fleets/registry.json` (`[lost-base] ops/validate.mjs:119`), `--strict` additionally
requires non-empty `ev_inputs` (`[lost-base] ops/validate.mjs:120-121`), `k3_seats` must
be exactly `[judge, planner]` (`[lost-base] ops/validate.mjs:63-65`), every `BANNED`
provider must appear in the `operator_decrees.banned_providers` decree
(`[lost-base] ops/validate.mjs:72-73`), and `modelRoles` is parsed from `.omp/config.yml`
with `/^\s{2}(\w+):\s*(\S+)\s*$/` (`[lost-base] ops/validate.mjs:82`). Output contract:
`validate: FAIL (<programs>, <lanes>, <errors>)` + exit 1, else
`validate: OK (...)` (`[lost-base] ops/validate.mjs:125-130`).
`ops/registry-check.mjs` (189 lines) owns the deep bijection: every non-k3
lane has exactly one `.omp/agents/kx-<lane>.md` card
(`[lost-base] ops/registry-check.mjs:57-80`), `mission_l1` resolves instead to
`fleets/mission-template.md` (`[lost-base] ops/registry-check.mjs:70-72`), card `model:`
pins resolve through `.omp/config.yml` modelRoles to the lane primary
(`[lost-base] ops/registry-check.mjs:82-108`), `judge` must keep an empty bucket plus an
`honest.halt` note (`[lost-base] ops/registry-check.mjs:117-118`), any other lane with an
empty bucket needs an explicit `degrade` note
(`[lost-base] ops/registry-check.mjs:121-122`), banned providers must be absent
(`[lost-base] ops/registry-check.mjs:134-157`), k3 routes confined to the two seats
(`[lost-base] ops/registry-check.mjs:159-170`), and every `grok` route must end `:low`
exactly (`[lost-base] ops/registry-check.mjs:34-43`, `:172-183`); the OK line prints the
lane count and the resolved k3 seats (`[lost-base] ops/registry-check.mjs:190`).
`ops/reroute-drill.mjs --simulate park:<lane>` is simulation-only by header
contract (`[lost-base] ops/reroute-drill.mjs:2-3`): it parses `/^park:(.+)$/`
(`[lost-base] ops/reroute-drill.mjs:20`), picks the first non-banned/non-parked/non-k3
bucket entry (`[lost-base] ops/reroute-drill.mjs:44-57`), degrades to `local` when none
(`[lost-base] ops/reroute-drill.mjs:60`), and writes `reroute_drill` telemetry with
`simulated: true` (`[lost-base] ops/reroute-drill.mjs:63-69`) — never mutates the
registry, never spawns, never calls the network.
`ops/check-freshness.mjs` alarms at `THRESHOLD_H = 26` hours
(`[lost-base] ops/check-freshness.mjs:15`), prefers
`last_permitted_check_at_utc ?? last_attempted_check_at_utc ?? snapshot_at_utc`
(`[lost-base] ops/check-freshness.mjs:43`), prints `FRESH`/`STALE`
(`[lost-base] ops/check-freshness.mjs:50`), exits `liveStale > 0 ? 1 : 0`
(`[lost-base] ops/check-freshness.mjs:59`) and appends one `freshness_check` telemetry
line per invocation (`[lost-base] ops/check-freshness.mjs:61`) — which is why the lost
tree's telemetry count grew between runs. Its default board was the other
then-surviving root, `/home/vgpnk/Projects/origin-work/open-bug-bounties`
(`[lost-base] ops/check-freshness.mjs:14`; root ABSENT since 2026-10-12).

Two ops scripts write beyond `ledger/`:
`import-board.mjs --from <board>` binds the three board datasets
(sha256 + record count + `refresh_run_id` all must match
`refresh_evidence.json`) before writing any `bounty-map/programs/*.json`;
new records land as `{ev_inputs:{}, lane:"executor",
mission_state:"DISCOVERED"}`; past-DISCOVERED files are byte-protected
but provenance drift emits `provenance_drift` telemetry (S4). Only the
independent dataset filters records (active + public + confirmed_cash +
high confidence) — the filter is mirror-anchored at
`[lost-base] ops/import-board.mjs:132`. `finalize-all.mjs` is the batch claim sweep: per
DONE package it re-runs claim-check, commits, byte-proofs then annotates
`claim-ready/<id>/<slug>` (conflicting existing sha → `claim_tag_conflict`,
never rewrites), refreshes the index, one atomic `push --atomic`
[corpus-attested as-of 2026-09-28T23:32Z; source tree absent] — the mirror
carries only the 39-line genesis version, whose sole git step is
`rev-parse --verify` + skip-an-existing-tag (`[lost-base] ops/finalize-all.mjs:25`), so
the byte-proof/conflict/`--atomic` behaviour is a lost-tree fact
(`corpus/knowledge/intake-and-finalize.md:78-92`).

Observation, not authority: `ops/sighting*.sh` manage four windows in
`ufo_sighting` — literally `for w in fleet ledger missions dispatcher`
(`[lost-base] ops/sighting.sh:8`, `:12`, `:18`) — and never kill mission panes or the
session itself (`[lost-base] ops/sighting.sh:17`); the board window runs
`watch -n5 -t ops/sighting-board.sh` (`[lost-base] ops/sighting.sh:24`).
`sighting-missions.sh` capture-pane frames are the live view — the
missions window's `tail -f fleets/run/*.log` dead-globs once logs rotate
to `.log.gz`.

**Never run the mirror's ops scripts in place** (round-15 hazard). All 11
derive their write root from their own location —
`const root = join(dirname(fileURLToPath(import.meta.url)), '..')`
(`[lost-base] ops/ev-report.mjs:21`, `[lost-base] ops/rank.mjs:43`, `[lost-base] ops/fleet-dispatch.mjs:21`,
`[lost-base] ops/park-disposition.mjs:12`, `[lost-base] ops/import-board.mjs:30`,
`[lost-base] ops/finalize-all.mjs:11`, `[lost-base] ops/validate.mjs:18`, `[lost-base] ops/registry-check.mjs:12`,
`[lost-base] ops/check-freshness.mjs:12`, `[lost-base] ops/claim-index.mjs:11`,
`[lost-base] ops/reroute-drill.mjs:10`) — so a run inside
`~/Projects/the-bounty-hunter` would create and mutate `ledger/`,
`fleets/run/`, `docs/autopsies/`, `evidence/` and `bounty-map/programs/` in a
read-only product repo (`[lost-base] ops/rank.mjs:140`, `[lost-base] ops/rank.mjs:203`,
`[lost-base] ops/rank.mjs:222`, `[lost-base] ops/shared.mjs:39`, `[lost-base] ops/park-disposition.mjs:43`,
`[lost-base] ops/park-disposition.mjs:53`). The mirror has no `ledger/` at all, so the
first `appendLedger` would throw ENOENT — `appendFileSync` creates no
directory [INFERENCE, derived not executed]. Only `ops/ev-report.mjs` is
side-effect-free (read-only imports, `[lost-base] ops/ev-report.mjs:17`), and r15 still
smoke-ran it from a byte-identical **copy** outside the mirror
(`/tmp/kasegi-r15/ev-smoke`). Detail: `corpus/knowledge/ops-invariants.md`,
`corpus/knowledge/intake-and-finalize.md`,
`corpus/knowledge/source-tree-loss-2026-09-28.md` §4.1.


## VDP disclosure packages (sibling format)

`vdp-disclosures/<slug>/` is a distinct, lighter contract: `ROUTE.md` (channel
+ attribution decree — observed: free + fully attributed via the vendor's
security.txt Contact route, e.g. an H1 `embedded_submissions` URL), a
`cover-note.md`, the same-craft `report.md` ("Disclosed freely by", pinned
commit/file/sha256, CWE, CVSS, verbatim scope excerpt), and `SUBMITTED.md`
(timestamp + verbatim platform confirmation). Operator personally sends; the
fleet stages, never sends. Parked VDP-adjacent programs show up as two-file
honest-zero claims (`report.md` + `status.json`, e.g.
`claims/hackerone-ruby/honest-zero-vdp-no-payout/`).

**This entire surface is corpus-attested only** [as-of 2026-09-28T23:32Z;
source tree absent]. The surviving mirror carries **no VDP runtime
knowledge**: `grep -rniE 'vdp|disclos|no.?payout|disclosed_free'` over
`~/Projects/the-bounty-hunter` (excluding `.git`) hits no `ops/*.mjs` file at
all — only the report-field list ("disclosure timeline",
`[lost-base] fleets/mission-template.md:50`), the genesis plan (`[lost-base] docs/genesis-plan.md:15`,
`[lost-base] docs/genesis-plan.md:17`) and two agent cards
(`[lost-base] .omp/agents/scope-evidence-custodian.md:83`,
`[lost-base] .omp/agents/the-bounty-hunter.md:28`); there is no `vdp-disclosures/`
directory, and `[lost-base] ops/finalize-all.mjs:20` filters on `state !== 'DONE'` with no
`DISCLOSED_FREE` case. Every VDP fact above is anchored in
`corpus/knowledge/vdp-disclosure-packages.md` (`:3-5`, `:9`, `:13-16`, `:20`,
`:22-31`), which is now the only record.

## Retirement lane — autopsies & the detail regex

`ops/park-disposition.mjs` (mirror: 80 lines, sha256 `868057c96cc8`; dry-run
by default, `--apply` acts — `[lost-base] ops/park-disposition.mjs:14`, dry-run exits 0
at `[lost-base] ops/park-disposition.mjs:41`; decree 2026-09-05: retry live paths, retire
structural blocks) regex-classifies every `fleets/run/*.status.json`
(directory constant `[lost-base] ops/park-disposition.mjs:13`) whose `state` is PARKED or
FAILED (`[lost-base] ops/park-disposition.mjs:23-25`) by its `detail` string — **first
match wins** (`[lost-base] ops/park-disposition.mjs:28-32`): `HONEST = /honest.zero/i`
(`[lost-base] ops/park-disposition.mjs:21`) → LEARNED (terminal-good);
`H1SPA = /scope unverifiable.*hackerone|hackerone.*SPA|content-negotiated to
RFC 9116|security\.txt stub/i` (`ops/park-disposition.mjs:20`) → RETRY_METHOD
(GraphQL path); `AUTH` (`[lost-base] ops/park-disposition.mjs:18` — 16 alternatives,
including `auth-walled`, `requires login`, `SPA login`, `accept_terms`,
`account creation`, `AUTH_UNVERIFIED`, `in_scope_assets empty`, `SPA shell`,
`login-walled`, `no testing grant`, `testing paused`, `requires agreement`,
`privacy hard stop`, `forbidden`, `prohibited personal-data`,
`not in publi`) → RETIRE_AUTH;
`TRANSIENT = /unreachable|timeout|HTTP 5\d\d|ECONN|ENOTFOUND|DNS|network/i`
(`[lost-base] ops/park-disposition.mjs:19`) → RETRY_TRANSIENT; else **REVIEW = no action**
(`[lost-base] ops/park-disposition.mjs:32`). The dry-run prints the five class counts
(`[lost-base] ops/park-disposition.mjs:36-39`).

RETRY_* is a real requeue: `attempt_reset` + `mission_unparked` telemetry then
`rmSync` of the status file so the dispatcher re-picks it on the current window
model (`[lost-base] ops/park-disposition.mjs:45-49`). RETIRE_AUTH reads the program record
(`[lost-base] ops/park-disposition.mjs:52`) and writes
`docs/autopsies/<id>.md` (`[lost-base] ops/park-disposition.mjs:43`, `:53`) with a fixed
**seven-part** body — round-15 correction, this section previously said
"five-part" while listing seven: 4 bold metadata lines `**Outcome:**`
(`[lost-base] ops/park-disposition.mjs:56`), `**Program URL:**` (`:57`),
`**State at retirement:**` (`:58`), `**Reason (verbatim):**` (`:59`), then 3
`##` sections — "Why it could not succeed autonomously"
(`[lost-base] ops/park-disposition.mjs:61-65`), "Unlock prerequisite"
(`[lost-base] ops/park-disposition.mjs:67-70`), "Evidence"
(`[lost-base] ops/park-disposition.mjs:72-73`). It then rewrites the status to
`state:'RETIRED'` with `detail: retired: <cls> — see docs/autopsies/<id>.md`
(`[lost-base] ops/park-disposition.mjs:75-77`) and emits `mission_retired` telemetry
carrying the autopsy path (`[lost-base] ops/park-disposition.mjs:78`). Requeue = operator
session or public policy, then delete BOTH the autopsy and the status file —
the instruction is printed into the artifact itself
(`[lost-base] ops/park-disposition.mjs:70`).

`detail` is machine-consumed, not prose: the 85-mission REVIEW cohort
(live census 2026-09-28 — 529 LEARNED / 85 REVIEW / 30 RETIRE_AUTH / 2
RETRY) is the same auth-wall class worded as "no exact in-scope assets" /
"active-testing grant" / "custodian HARD_STOP" — none of which the regex
knows, so they park invisibly [corpus-attested as-of 2026-09-28T23:32Z;
source tree absent; the regex half is mirror-verified above — those three
phrasings match none of `[lost-base] ops/park-disposition.mjs:18-21`]. **When parking a
mission, embed a literal classifier keyword in `detail`**
(`in_scope_assets empty`, `no testing grant`, `auth-walled`,
`scope unverifiable: ...hackerone`) or the disposition pass no-ops.

The 31 autopsies partition: auth-walled SPA ×27, terms-gate ×1 (SIX),
privacy hard stop ×1 (Airtable), paused/non-enumerable ×2
[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]. The generated
"Why" paragraph is boilerplate — it always says "account login"
(`[lost-base] ops/park-disposition.mjs:62-65`), so trust `Reason (verbatim)`
(`[lost-base] ops/park-disposition.mjs:59`), not the prose. Authoritative detail:
`corpus/knowledge/retirement-autopsies.md`.

## Evidence-package anatomy

`claims/<program>/<slug>/` — six files, per `fleets/mission-template.md` and
verified in `claims/cantina-pendle/ingestion-20260915/` (sampled reality,
round 14: 18/20 packages hold the full six-file set;
`claims/hackerone-hyatt/ingestion-20260914/` holds 1/6 canonical
(`status.json`) + `BLOCKED.md`/`INGESTION.md`/`claim.json`,
`claims/bugcrowd-northwestern-mutual-mbb-og/honest-zero/` holds 1/6 +
`submit/` — `corpus/knowledge/claim-anatomy-sample.md`):

| File | Contract |
|---|---|
| `report.md` | title; program + official URL; verbatim "Scope excerpt" + URL + observed_at + sha256; vuln class; repro steps (no secrets); impact tied to the policy's severity/reward language; affected asset; suggested fix; disclosure timeline; explicit "No submission performed" |
| `claim_checklist.md` | exact per-program submission steps; portal quirks; marked OPERATOR-GATED; names residual gates (fees, VM captures) |
| `evidence/manifest.json` | `evidence-manifest/v1`: sha256 per artifact, `polarity` (≥1 positive), `redactions[]` — same-digest receipt per artifact with distinct producer/verifier; `redactions:[]` is never claim-ready |
| `custodian-receipts.json` | decision chain {action, input_sha256, decision_sha256, matched_grant_id, scope_signal}; every action needs nonempty grant + `scope_signal:"NO_SCOPE_OBJECTION"` exactly; `head_sha256` == manifest `expected_head_sha256` |
| `provenance.json` | agents + requested/resolved models per transition, commands + exit codes, commit pin, policy_sha256, `external_effects_performed: []`, secrets sweep attestation |
| `status.json` | state machine; `manifest_sha256` binds status to manifest bytes; `claim_review` block with hard_gates + subchecks. Round-14 sampling (30/280 read line-by-line): the full contract holds in only 20/280 — 92.9% deviate; `claim_review` present 26/280, `claimable` present 39/280, `manifest_sha256` absent/null 84/280; the b1k-* keeper cohort (233/280) carries a minimal 13-key status without `claimable`/`claim_review` (`corpus/knowledge/claim-anatomy-sample.md`) |

`status.json` field semantics (from real packages):
`claimable` — the operator-queue bit. `do_not_submit` / `no_submission_performed`
— belt+braces on the external-effect gate. `claim_review.hard_gates` —
`written_scope`, `authorization`, `evidence_integrity`,
`no_duplicate_or_prior_submission`. `claim_review.subchecks` — `no_secrets`,
`operator_attribution`. Reviewer must be distinct from producer, with
requested/resolved model + fallback recorded. Any failed/unknown gate →
`state:"BLOCKED"`, `claimable:false`, never a silent downgrade to "DONE-ish".

## Disclosure anti-patterns (all observed in fleet wrap review)

From `[lost-tree] docs/wrap-report.md` — 7 canonical packages, 0 clean GO, 0 immediate
submissions (counts `:25-32`: 0 GO / 5 GO-WITH-FIX-NEEDED / 2 NO-GO / 7
canonical / 8 tag refs). Round-14 correction: the 5 GO-WITH-FIX rows failed
on disclosure/packaging defects, but the 2 NO-GO rows are reproduction
gates, not disclosure defects (`:9` decision rule; `:20` 3CX uid=0 capture,
`:21` WordPress pinned-checkout rerun). Per-package source rows are `:17-23`
(anthropic `:17`, mozilla `:18`, intel `:19`, 3cx `:20`, wordpress `:21`,
spotify `:22`, airtable `:23`).

Per-item anchor map (round-14 addition; the r13 repair-3 deliverable):

| # | wrap-report row(s) | wrap verdict | primary source anchor |
|---|---|---|---|
| 1 | anthropic `:17`, intel `:19`, spotify `:22`; payload audit `:91-97` | GO-WITH-FIX ×5 | `[lost-tree] docs/wrap-report.md:93` `positive_finding`; `:94`,`:97` `positive` |
| 2 | intel `:19` descope; airtable `:23` ceiling advice overridden | decree `2ef530c6` | `[lost-tree] fleets/claimer-mission.md:22`, `[lost-tree] fleets/claimer-mission.md:29` |
| 3 | mozilla `:18`, payload row `:92` | GO-WITH-FIX | `[lost-tree] claims/mozilla-security-bounties/lando-diff-warning-missing-authz/report.md:79-82` |
| 4 | airtable `:23`,`:97` (8 files vs 3); wordpress `:95` (17 files); anthropic `:17`,`:91` | GO-WITH-FIX | `[lost-tree] claims/hackerone-airtable/airtable-js-record-id-path-traversal/claim_checklist.md:35` |
| 5 | all 8 tag refs `:5`,`:118`,`:122-124`,`:126` | tag drift | `[lost-tree] docs/claim-ready-index.md:32-38` + `[lost-tree] ops/claim-index.mjs:4` |
| 6 | — (not wrap-sourced) | incident record | `[lost-tree] claims/bugcrowd-seek/honest-zero/submit/BLOCKED.md:17-20` |
| 7 | — (not wrap-sourced) | ingestion record | `[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:14-15` |
| 8 | — (not wrap-sourced) | invariant I8 | `[lost-base] fleets/mission-template.md:20` + `[lost-tree] docs/continuation-notes.md:19`, `[lost-tree] docs/continuation-notes.md:26` |
| 9 | 3cx `:20`, wordpress `:21` | NO-GO ×2 | pendle `[lost-tree] claims/cantina-pendle/ingestion-20260915/status.json:4-5`, `[lost-tree] claims/cantina-pendle/ingestion-20260915/status.json:21`; 3cx `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:2`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:5`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:21` |
| 10 | — (not wrap-sourced) | runbook rule | `[lost-tree] docs/claim-runbook.md:11-20` (§A step 2) |
1. **Internal verdict strings as portal severity** — payloads carried
   `positive_finding` / `positive` instead of the platform's severity
   language (H1 `High` + CVSS, Intigriti `Unscored` when the program
   self-assigns): `[lost-tree] docs/wrap-report.md:19` (`positive_finding` → `Unscored`
   — Intel assigns CVSS v4.0), `:17` (H1 `High`/CVSS 7.8 "rather than an
   internal verdict string"), `:22` (`Medium`/CVSS 5.5); all 7 payload-audit
   rows flag it (`:91-97` — `positive_finding` `:93`, `positive` `:94`,`:97`).
2. **Severity hedging below evidence, and inflation above it** — decree
   2026-09-05: claim at full supported strength; strip "Low-to-Medium
   ceiling" phrasing where Medium is proven; keep descoped language where
   precondition isn't proven (Intel: direct OOB write only, no code-exec
   claim). Decree verbatim: `[lost-tree] fleets/claimer-mission.md:29`; it postdates the
   wrap review (git: wrap fixes `b3b1b7e3` 19:54 −03:00 → decree applied
   `2ef530c6` 20:56 −03:00, "airtable claims Medium at full strength") and
   overrides `[lost-tree] docs/wrap-report.md:23`'s keep-the-ceiling advice — pre-decree
   staging line `[lost-tree] fleets/claimer-mission.md:22`, applied at
   `[lost-tree] claims/hackerone-airtable/airtable-js-record-id-path-traversal/claim_checklist.md:32`;
   descope side `[lost-tree] docs/wrap-report.md:19` (no code-execution/LPE claim, no
   requested High) + tag-inflation side `:122` (Intel tag still asked High).
3. **Absolute statements falsified by the package's own provenance** —
   Mozilla report said "no live host was contacted" while provenance
   recorded earlier GET/HEAD recon (`[lost-tree] docs/wrap-report.md:18`, payload row
   `:92`); corrected to "no live host contacted *to verify this finding*" —
   fix applied live at
   `[lost-tree] claims/mozilla-security-bounties/lando-diff-warning-missing-authz/report.md:79-82`.
4. **Internal orchestration artifacts in attachments** — authorization/scope
   records, duplicate checklists, internal files submitted alongside the
   report (`[lost-tree] docs/wrap-report.md:17`, `:91`,`:93`; wordpress staged 17
   attachments against a 3-file allowlist `:95`). Attach only triage-useful
   proof (Airtable: `poc.js`, `poc-output.json`, `proof.json` — nothing else,
   `:23`,`:97`; allowlist at
   `[lost-tree] claims/hackerone-airtable/airtable-js-record-id-path-traversal/claim_checklist.md:35`).
5. **Stale `claim-ready/*` tag treated as current authority** — a historical
   tag never overrides current bytes (`[lost-tree] docs/claim-runbook.md:3-5`);
   `[lost-tree] ops/claim-index.mjs:4` ("tags are provenance only" — string
   absent from the surviving mirror's `ops/claim-index.mjs`, whose `:3-4`
   header instead reads "regenerate docs/claim-ready-index.md from the repo's
   claim-ready/* tags … Run after any claim-ready tag lands"), and only current
   bytes passing `ops/claim-check.mjs` enter the queue
   (`[lost-tree] docs/claim-ready-index.md:3`). The mechanism is live: 3 tags sit
   excluded from the operator queue with per-row failing gates
   (`[lost-tree] docs/claim-ready-index.md:32-38`); all 8 wrap-era tags lack their
   generated payload (`[lost-tree] docs/wrap-report.md:118`), annotations drifted
   (`:122-124`: Intel asks High, 3CX `$1,150–$3,500` vs current
   `$1,150–$2,300`, Mozilla stale manifest digest), and the alias package
   must not be submitted from (`:126`).
6. **Overclaiming the negative** — an empty `in_scope_assets` means "not
   observed in this response", never "the program has no scope"
   (`[lost-tree] claims/bugcrowd-seek/honest-zero/submit/BLOCKED.md:17-20`; gate row
   `:26`; `[lost-tree] claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json:5`, `[lost-tree] claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json:56`).
7. **Claiming safe harbor the program doesn't grant** — SEAL Whitehat covers
   active exploits only; routine findings get no safe-harbor credit
   (`[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:14-15`, `[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:31`, `[lost-tree] claims/cantina-pendle/ingestion-20260915/INGESTION.md:34`;
   `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:34-35`).
8. **Manufactured findings** — I8: "never manufacture a finding"
   (`[lost-base] fleets/mission-template.md:20`; ufo-substrate invariant "Honesty
   outranks progress"); honest-zero is a first-class deliverable — the
   designed-outcome gloss is
   `[lost-tree] fleets/ufo-archive-2026/missions/groknight-mentor/lane-connector.md:24`.
   438/486 non-claim-ready missions terminate as LEARNED honest-zero
   (`[lost-tree] docs/continuation-notes.md:19`, heading `[lost-tree] docs/continuation-notes.md:26`; partition
   `[lost-tree] docs/continuation-notes.md:20-22`: 19 RETIRED + 3 RETRY-method + 26 FAILED-infra).
9. **Precondition laundering** — a local PoC proves the defect, not live
   impact. The package stays gated until the named precondition check runs:
   Pendle `state:"BLOCKED"` + `positive-blocked-live-precondition`
   (`[lost-tree] claims/cantina-pendle/ingestion-20260915/status.json:4-5`,
   `resume_condition` `[lost-tree] claims/cantina-pendle/ingestion-20260915/status.json:21`; live-balance gate `[lost-tree] claims/cantina-pendle/ingestion-20260915/claim_checklist.md:9-16`);
   3CX `claimable:false` + review `outcome:"BLOCKED"` despite DONE state
   (`[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:2`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:5`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:21`;
   uid=0 capture required `[lost-tree] docs/wrap-report.md:20`). WordPress differs
   (round-14 correction): package state is DONE + `claimable:true`
   (`[lost-tree] claims/hackerone-wordpress/unchecked-aaaa-ssrf/status.json:2`, `[lost-tree] claims/hackerone-wordpress/unchecked-aaaa-ssrf/status.json:13`) —
   the hold was the wrap NO-GO gate (`[lost-tree] docs/wrap-report.md:21`, `[lost-tree] docs/wrap-report.md:157`), since
   cleared (`[lost-tree] claims/hackerone-wordpress/unchecked-aaaa-ssrf/status.json:25` APPROVED; `[lost-tree] claims/hackerone-wordpress/unchecked-aaaa-ssrf/status.json:48` delta_note: 2026-09-15 poc.sh
   re-executed, exit 0).
10. **Treating "DONE" as claimable** — `DONE` alone is insufficient:
    claimable requires `claimable:true`, positive `finding_count`,
    status↔manifest digest, custodian head binding, redaction receipts,
    reviewer distinctness, secret + attribution subchecks
    (`[lost-tree] docs/claim-runbook.md:11-20` = §A step 2, item-for-item; live proof:
    3CX DONE + `claimable:false`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:2`, `[lost-tree] claims/hackerone-3cx/sudo-nopasswd-argument-injection-root/status.json:5`).

Same source, not itemized above (round-14 additions): payloads used absolute
workstation paths — regenerate on the submission host
(`[lost-tree] docs/wrap-report.md:99`); program-wide reward range ≠ finding-specific
requested band (Mozilla `$500–$20,000` vs proposed High `$3,000–$6,000`,
`:92`,`:107`); secret scans must tolerate inert fixtures (Airtable's
one-char `Bearer x`, `:83`); final gate was HOLD — zero immediate
submissions (`:155-157`).

## Claim-hardening wave — the defect layer above the gates

`fleets/ufo-archive-2026/missions/claim-*/report.json` (20 L1 hardening
missions, 2026-09-14 — round-13 correction: this line stayed at 19 after
r12 fixed the companion) is the empirical superset of `claim-check.mjs`:
what packages actually get wrong, beyond what the checker catches. The
top recurrence classes (full 22-class taxonomy:
`corpus/knowledge/ufo-archive-2026.md`):

| Class | Signature | Fix pattern |
|---|---|---|
| Custodian head mis-binding | `head_sha256` absent; `expected_head_sha256` used as receipt field name; terminal `event_sha256` bound instead of terminal `decision_sha256` | rebind to final decision digest |
| Redaction-receipt drift | artifacts without same-digest receipts; orphan receipts binding *stale* digests (incl. reusable receipts existing in `evidence/` but never copied into `manifest.redactions`) | receipts bind current manifest digests, producer ≠ verifier |
| Missing in-package `submission-draft.md` | dominant defect — nearly every `claim-ready` package | stage canonical paste-ready draft: verbatim scope excerpt, clone prerequisite, prior-art/dedupe disclosures |
| Stale packet drafts | `submission-review/packets/` admin drafts contradict in-package state — one was *materially wrong* (dev-trunk-only conclusion omitted the vulnerable stable v1 endpoint) | `DO-NOT-USE` banner; in-package draft is canonical |
| Receipt drift (duplicate-submission hazard) | package reads pre-submission while a real receipt exists (H1 #4028846 = `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/receipts/k8s-nodebound-token-impersonation.json:5-8` + `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/submission-receipts.csv:2`; Bugcrowd a169f309 = `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/receipts/ld-node-stream-tls-bypass.json:5-6` + `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/submission-receipts.csv:3`) | `RECEIPT EXISTS — DO NOT RESUBMIT` banner; reconcile every admin file to submitted-state — round-14 correction: the bounties-repo reconcilers do NOT hold these receipts (`[lost-tree] fleets/run/portal-reconciliation-2026-09-11.json:9-11` covers only the Sep-11 trio 4002776/4002810/4002789; `[lost-tree] .ufo/claim-recovery/final-audit.json` has zero 4028*/a169f309 matches) — the origin-work `submission-review/` store does (incl. `[lost-base] ~/Projects/origin-work/open-bug-bounties/claim-packages/submission-review/queue.json:11-12`) |
| "Verified" but never executed | vectors claimed verified, never run (exemplars: coinbase vectors 3-4 + path-form boundary; sibling class = overclaims contradicted by the package's own evidence, e.g. spacex "both resolvers" = DoH only — `corpus/knowledge/ufo-archive-2026.md:150-154`) | execute against real extracted code; regenerate RUN_LOG |
| Stale file:line citations | most common narrative defect — citations drift every repair (exemplars: metamask `:161→:162`, elastic `:604→:605` + api.search.go range, aiven quoted stale anchor "README.rst:706" (source base not retained), web3 ranges narrower than function extents, web1 `READY.md` systematically stale — `corpus/knowledge/ufo-archive-2026.md:145-149`) | re-cite post-repair numbering before staging |
| Manifest↔report disagreement | REPORT flags `UNRESOLVED CONFLICT` while manifest says `claim-ready` | manifest is gate-visible; reconcile (`hold-prior-filing-conflict`, preserve `prior_status`) |
| Alias indistinguishable from canonical | alias carried `claim-ready` + own contradictory severity | `status:"claim-ready-alias"`, `claim.json alias_of`, evidence-handoff stub draft, `DO-NOT-ATTACH` flag |
| Proven-but-not-claimable | vuln proven by PoC but published audit finding + deployed asset verified fixed first-hand (gamma-deposit) | `NOT-SUBMITTABLE` state; exclusion-notice draft (elastic falsified-by-execution) |

Outcome vocabulary the wave established: `REFINED→DONE` (gates pass,
submission still operator-gated), `HOLD` with named blockers,
`NOT-SUBMITTABLE`, `reconcile-only` (verified prior submission),
`stop — frontier saturated`. No mission submitted anything —
`no_submission_performed` is the norm even in DONE packages.

The archive also holds the `b1k-NNN` provenance: `bounty-keeper/keeper.mjs`
(16-pane wall, launched 265, halted on 12 h night budget) is the producer
of the run_ids `ledger/candidates.jsonl` and `evidence/*/b1k-NNN/` still
reference. Archive `claim-packages/<slug>` paths are the pre-rename tree —
they now live at `claims/<platform>-<program>/<slug>/`. Mine the archive
for defect patterns; it is not live state.

## Submitted-state registry — the do-not-refile set

Full table: `corpus/knowledge/submitted-registry.md`. Submission truth is
scattered — `claims/*/*/status.json` (six field spellings), `ledger/missions.jsonl`,
`fleets/run/portal-reconciliation-2026-09-11.json`,
`.ufo/claim-recovery/final-audit.json`, `vdp-disclosures/`, stale
`claim-ready/*` tags, and archive-era mission reports. Consolidated set:

- **Verified:** H1 `4002776` mozilla (closed_duplicate), H1 `4002810` spotify
  (closed_duplicate), H1 `4002789` airtable (`not_established`; status.json is
  BLOCKED but `submission_state:"SUBMITTED"` + `submitted_url` carry the truth).
- **Archive-era** (`claim-web1/2`): H1 `4028846` k8s-nodebound, Bugcrowd
  `a169f309` ld-node-stream, Bugcrowd `e4f41218-6036-4bcf-80f1-1e2b6bf86d4e`
  mattermost-jira-oauth2 — all filed 2026-09-14. The packages **were** not gone:
  they lived in the sibling tree `~/Projects/origin-work/open-bug-bounties/
  claim-packages/` — whose `submission-review/submission-receipts.csv`
  (3 rows) + `receipts/` (6 JSONs) + `queue.json` were the real receipt store
  — **that tree is ABSENT since 2026-10-12** (round-19 re-census,
  `corpus/knowledge/root-loss-2026-10-12.md`); the claims are now
  corpus-attested only.
  No bounties-repo tool reads that tree — a second blind spot.
- **Probable-unverified** (login-wall, ~65–70% real per claim-elastic):
  H1 `4028904`/`4028953` elastic, Bugcrowd `4ecbaf46` aiven. Do not refile;
  do not delete receipts.
- **VDP:** `anthropic-plugin-dev-cmd-injection` freely disclosed 2026-09-06
  (ledger `DISCLOSED_FREE` row at the same timestamp).
  ⚠ Queued row 4 (`hackerone-anthropic/plugin-dev-test-hook-command-injection`,
  DONE+claimable) is the SAME finding (same commit/file/sha256/CWE-78) — the
  duplicate scan tests only `submitted_url`/`submission_performed`/
  `submission_state` inside `claims/*/*/status.json`, misses `vdp-disclosures/`
  and archive receipts; live `claim-check` run on the package returns OK.
  A `claim-hold/*` tag exists on it, yet the generated index still queues it.
  Report upstream (bounties owner); not fixed here (cross-domain).

Field traps: `submitted_url` (filed report, contains `/reports/`) ≠
`submission_url` (destination endpoint). `submission_performed:false` does NOT
mean unsubmitted — airtable carries it plus a real `submitted_url`. Trust
`submitted_url`-with-`/reports/`, `submit/receipt.md`, or `submission_state`
SUBMITTED, cross-checked against ledger SUBMITTED/DISCLOSED_FREE rows.
Aliases are structured when used — `hackerone-mozilla` status.json carries
`duplicate_of` + `submission_state:"DUPLICATE_OF_SUBMITTED"` pointing at the
mozilla canonical; the `claim.json alias_of` convention is unused repo-wide.
`claim-ready/*` tags (3) all predate the SUBMITTED commits; `claim-hold/*`
tags (9) exist alongside. 15 of 295 `claims/<p>/<s>/` dirs have no
`status.json` (13 `ingestion-seeded` stubs: `INGESTION.md`+`claim.json`;
stiltsoft partial; t-mobile `BLOCKED.md`-only; histogram over the 280 gated:
PARKED 248 / BLOCKED 15 / DONE 15 / SUBMITTED 2 — the single OPERATOR_GATED
is intel's *nested* `submission.state`, not a top-level state). Root
`*-2026-09-15.zip` bundles are dated snapshots, not filtered live state.

## Operator queue — live audit

`docs/claim-ready-index.md` (generator: `ops/claim-index.mjs`) queues every
`claims/*/*/status.json` package whose current bytes pass `claim-check.mjs`.
Live re-run 2026-09-28 (round 13): all 12 queued rows pass the gate;
tree-wide 281 `status.json` = 280 packages (PARKED 248 / DONE 15 / BLOCKED
15 / SUBMITTED 2) + 1 evidence-copy grep trap
(`claims/bugcrowd-seek/honest-zero/evidence/status.json`, state PARKED);
claim-check over the 15 DONE → 12 OK + 3 FAIL (doit 7 errors, github-bounty
8, 3cx 8), exactly matching the generated index's blocked table. Dossier:
`corpus/knowledge/operator-queue.md`. Two systemic holes in the queue path:

- **`claim-hold/*` tags are inert** — `claim-index.mjs` only reads
  `claim-ready/*` tags; no hold filter exists. Queued rows 2 (8x8),
  4 (anthropic), 7 (wordpress), 10 (intel) — FOUR, round-13 correction; the
  8x8 hold tag has existed since 2026-09-05T19:28:41-03:00 — carry
  `claim-hold/*` tags the index ignores (9 hold tags total, all creatordate
  2026-09-05).
- **Duplicate scan reads `claims/` only** — row 4
  (`hackerone-anthropic/plugin-dev-test-hook-command-injection`) is
  byte-identical to the operator's own VDP disclosure
  (`vdp-disclosures/anthropic-plugin-dev-cmd-injection`: same commit
  `d7dbd9a`, file, sha256 `ded642e8`, CWE-78) and still returns
  `claim-check: OK`. **Do not file row 4.**

Other per-row traps: all 12 queued rows carry `submitted_url: null`
(round-13 correction — earlier text called the route URLs `submitted_url`;
they live in `submission_url` (spacex), `claim_url`
(8x8/anthropic/wordpress/intel), and `submit-payload.json` route fields);
real `/reports/<id>` receipts exist only on the 2 SUBMITTED packages
(airtable, spotify). Queue membership means "never submitted" by field value,
not inference. Personio (row 11): takeover proof is REQUIRED by program
OOS, not optional. SpaceX (row 1): same class, "recommended". Intel (row 10):
`submit/BLOCKED-2026-09-11.md` still on disk — no authenticated Intigriti
session. 8x8 (row 2): asset is `eligible_for_bounty=false` — the index itself
flags "No payout claim". Mutable-precondition rows (spacex DNS, amazonvrp
registry state, x source drift, beanstalk deployed-bytecode, yahoo rolling
1-year release window) all carry mandatory re-verify gates in their
`claim_checklist.md`.

## Triage economics

`ops/ev-report.mjs` computes the hunter-contract EV for one program record
(`bounty-map/programs/<id>.json` → `ev_inputs`; path built at
`[lost-base] ops/ev-report.mjs:28-29`) and persists nothing — it imports only
`readFileSync`/`existsSync` (`[lost-base] ops/ev-report.mjs:17`) and ends in
`process.exit(0)` (`[lost-base] ops/ev-report.mjs:92`). Reporting tool, never a gate.

**Anchor base (round 15).** `~/Projects/bounties` is GONE — removed
2026-09-28T23:51:31Z (`corpus/knowledge/source-tree-loss-2026-09-28.md`).
Cites below were re-read this round from the frozen 2026-09-05 mirror
`~/Projects/the-bounty-hunter` HEAD `1cfbd86`. Its `ops/ev-report.mjs`
(92 lines, sha256 `ba5485ed6a5d`) resolves all 14 spans the corpus recorded
from the lost tree at the same line numbers — **anchor-compatible, not proven
byte-identical** (the lost bytes are gone); `ops/rank.mjs` (249 lines,
`e724186c1330`) matches at `DEFAULTS :55-59`. `ops/fleet-dispatch.mjs` is 330
lines vs the lost 427 (`corpus/knowledge/mission-control.md:3`) and diverges
in content, so its anchors are cited twice and every lost-tree anchor is
written `[lost-tree] <path>:<line>` — a token that cannot resolve against the
mirror by accident. Counts from the lost DATA half carry [corpus-attested
as-of 2026-09-28T23:32Z; source tree absent].

```
p_success    = p_in_scope × p_reproducible × p_unique × p_accepted
gross_value  = p_success × expected_reward
total_cost   = effort_hours × opportunity_rate + direct_cost + delay_cost
               + expected_risk_cost
adjusted_ev  = gross_value − total_cost
```

Terms: `[lost-base] ops/ev-report.mjs:77` (`p_success` — left-fold
`reduce((a,b)=>a*b, 1)` over the 4 factors mapped at
`[lost-base] ops/ev-report.mjs:73`), `[lost-base] ops/ev-report.mjs:78` (`gross_value`),
`[lost-base] ops/ev-report.mjs:79-81` (`total_cost`; the 5 `costKeys` at
`[lost-base] ops/ev-report.mjs:74`), `[lost-base] ops/ev-report.mjs:82` (`adjusted_ev`); all four
printed at `[lost-base] ops/ev-report.mjs:86-89`. Guards: `[lost-base] ops/ev-report.mjs:46`
`isNum = typeof v === 'number' && Number.isFinite(v)` — no coercion, so a
JSON string `"0.5"` prints UNKNOWN while numeric `0.5` prints;
`[lost-base] ops/ev-report.mjs:47` `fmt = String(Number(v.toFixed(6)))` — six decimals
then trailing-zero stripping: `0.0735`, never `0.073500`.

Missing inputs print `UNKNOWN`, never 0/1; the affected term and the verdict
degrade to `unknown`, fail-closed (`[lost-base] ops/ev-report.mjs:47`,
`[lost-base] ops/ev-report.mjs:91`). Verdict is strict — `positive_adjusted_ev: true`
only when `adjusted_ev > 0`, `false` at ≤ 0 (exactly 0 → `false`), `unknown`
when either term is non-finite (`[lost-base] ops/ev-report.mjs:91`). Exits: 0 always on a
report (`[lost-base] ops/ev-report.mjs:92`); **2** for a missing program-id argument
(`[lost-base] ops/ev-report.mjs:23-26`) OR a missing program file
(`[lost-base] ops/ev-report.mjs:30-33`); unparseable file → `WARNING` + `rec = null`
(`[lost-base] ops/ev-report.mjs:38-41`) → `ev = {}` (`[lost-base] ops/ev-report.mjs:43`) → all 10
inputs and all 4 terms UNKNOWN, exit 0 — fail-closed on values, not on parse.
All branches **runnable-verified**: r15 ran a byte-identical copy of the
mirror script (`/tmp/kasegi-r15/ev-smoke`, copy sha256 == mirror sha256) and
observed every exit code and every UNKNOWN path.

Row shape `  <key> = <value> basis: <basis><detail>`, `padEnd(20)` /
`padEnd(10)` (`[lost-base] ops/ev-report.mjs:70`); `as_of` raw or UNKNOWN
(`[lost-base] ops/ev-report.mjs:50`); `sources[k].basis` = `source_url` (URL appended at
`[lost-base] ops/ev-report.mjs:65`), `estimate`, else `unknown`
(`[lost-base] ops/ev-report.mjs:59-70`), `rationale` appended after ` | `
(`[lost-base] ops/ev-report.mjs:69`). The basis column is never exercised live — 0/1088
records carry any `sources[].basis`, so all 10 inputs print basis `unknown`
[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]. The
operator-only contract (vault unlock, MFA, KYC, the Submit click, payout
rails) lived in the lost `docs/claim-runbook.md` [corpus-attested as-of
2026-09-28T23:32Z; source tree absent].

`ops/rank.mjs` DEFAULTS are a **separate machine**, never read by ev-report
(`[lost-base] ops/rank.mjs:55-59`, values `[lost-base] ops/rank.mjs:56-58`): p_in_scope 0.7,
p_reproducible 0.7, p_unique 0.25, p_accepted 0.6, effort_hours 60,
opportunity_rate 25, direct_cost 0, delay_cost 0, expected_risk_cost 250.
Derived: 0.7×0.7 = 0.49, ×0.25 = 0.1225, ×0.6 = **0.0735**; total_cost =
60×25+0+0+250 = **1750**. Same formula behind `round6` (`[lost-base] ops/rank.mjs:63`,
`compute` at `[lost-base] ops/rank.mjs:66-77`) but a different reward source: rank takes
`rec.reward?.min` (`[lost-base] ops/rank.mjs:92`, `[lost-base] ops/rank.mjs:118-119`) and copies only
the 9 PROB+COST keys for a curated record (`[lost-base] ops/rank.mjs:104`), so
`ev_inputs.expected_reward` (`[lost-base] bounty-map/schema.json:40`) is read by
**ev-report alone** (`[lost-base] ops/ev-report.mjs:78`) — one symbol, two sources;
never conflate them.

Consequence: `adjusted_ev = 0.0735 × reward.min − 1750`, so break-even needs
`reward.min > 1750/0.0735 = 23 809.52`; the highest observed floor was 10 000
(0.0735×10000 = 735 → **−1015**), i.e. every default-basis program is
negative-EV [corpus-attested as-of 2026-09-28T23:32Z; source tree absent].
Under DEFAULTS p_success and total_cost are constant, so the sort at
`[lost-base] ops/rank.mjs:123` (`adjusted_ev` desc, then `id` asc) degenerates to
`reward.min` desc: only a curated record can reorder the queue. That is AR12
in arithmetic — EV is ORDERING, never a gate (`[lost-base] ops/fleet-dispatch.mjs:11`
comment); the negative-EV `ev_note` branch (mirror
`[lost-base] ops/fleet-dispatch.mjs:156`; `[lost-tree] ops/fleet-dispatch.mjs:204`)
ledgers the fact, it does not block.

Run contract: `node ops/rank.mjs [--top N] [--write-queue]` — `--top` default
20 (`[lost-base] ops/rank.mjs:46`), non-integer or < 1 → `rank: ERROR` + exit 1
(`[lost-base] ops/rank.mjs:48-49`). Without `--write-queue` it prints and exits 0
(`[lost-base] ops/rank.mjs:161`); with it, S3 queue admission runs (`[lost-base] ops/rank.mjs:163`).
Either way it writes `ledger/rankings-<YYYYMMDDTHHMMSSZ>.json` (stamp
`[lost-base] ops/rank.mjs:53`, path `[lost-base] ops/rank.mjs:140`, collision suffix `-1`/`-2`/…
`[lost-base] ops/rank.mjs:141-142` — never overwrites, so sha256 attestations never
break) holding `{generated_at, defaults{basis:'default_estimate', …DEFAULTS,
as_of}, ranked, unknown}` (`ops/rank.mjs:143-148`). Every queued mission
appends `{mission_id:'mission-<id>', transition:'RANKED',
producer:'kx-executor', model:'alibaba-token-plan/qwen3.8-max:xhigh',
adjusted_ev, basis, artifact_sha256}` (`ops/rank.mjs:186-190`; the digest is
taken over the artifact bytes at `[lost-base] ops/rank.mjs:178`) — the attestation binds
the ranking file, not just the number. `stateOrder` (`[lost-base] ops/rank.mjs:179`) is
the 12-step pre-terminal ladder DISCOVERED → NORMALIZED → DEDUPED → SCOPED →
RANKED → PLANNED → AUTHORIZED → EXECUTED → EVIDENCED → VERIFIED →
SUBMISSION_PREPARED → LEARNED: it carries `AUTHORIZED`, which the live ledger
never recorded a transition for, and omits both the operator-only
SUBMITTED/DISCLOSED_FREE and the terminal PARKED/FAILED/RETIRED
[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]. The top 5
RANKED curated candidates also get `evidence/<id>/custodian-input.json`,
written only if absent (`[lost-base] ops/rank.mjs:216-219`): a
`custodian-input-skeleton/v1` for one `read_public_policy` action
(`[lost-base] ops/rank.mjs:223`, `[lost-base] ops/rank.mjs:229`), impact ceiling "none — read-only
public metadata", `data_classes: ['public']`, `credential_binding` and
`external_effect` both none, `scope_snapshot.note: 'no live fetch'`
(`[lost-base] ops/rank.mjs:231-235`, `[lost-base] ops/rank.mjs:241`), window = now + 7 days
(`[lost-base] ops/rank.mjs:214`, `7 * 864e5`). The AR14 bounded passive policy read is
pre-staged as a skeleton that itself fetches nothing.

| `rank.mjs` admission condition | outcome | cite |
|---|---|---|
| `reward.min` not a finite number | filed `unknown`, reason `no verified reward floor` | `[lost-base] ops/rank.mjs:92-96` |
| curated `ev_inputs` missing any of the 9 PROB+COST keys | filed `unknown`, reason names the missing keys | `[lost-base] ops/rank.mjs:105-108` |
| `adjusted_ev ≤ 0` | not in `positives`, never queued | `[lost-base] ops/rank.mjs:151`, `[lost-base] ops/rank.mjs:164` |
| positive but `inputs_basis === 'default_estimate'` | **held**, not queued — "not sufficiently evidenced" | `[lost-base] ops/rank.mjs:164-165`, `[lost-base] ops/rank.mjs:247` |
| positive + curated, last ledger line already `RANKED` with the same `adjusted_ev` | duplicate attestation suppressed (counted, not appended; malformed history lines fail open) | `[lost-base] ops/rank.mjs:185`, `[lost-base] ops/rank.mjs:175` |
| positive + curated + `mission_state === 'DISCOVERED'` | advanced to `RANKED`; any state ≥ RANKED never regresses | `[lost-base] ops/rank.mjs:200-204` |
| in the top 5 of the RANKED curated set | custodian skeleton written unless it exists | `[lost-base] ops/rank.mjs:209-219` |

`adjusted_ev` is derived-only, never persisted: `ev_inputs` is pinned
`additionalProperties: false` (`[lost-base] bounty-map/schema.json:34`, block
`[lost-base] bounty-map/schema.json:32-52`) with no such property, ev-report writes no
file (`[lost-base] ops/ev-report.mjs:17`), and 0/1088 records carry the key
[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]. The dispatcher
reads it anyway — `rec.ev_inputs?.adjusted_ev` (mirror
`[lost-base] ops/fleet-dispatch.mjs:152`; `[lost-tree] ops/fleet-dispatch.mjs:200`) — and
logs `adjusted_ev: ev ?? 'unknown'` (mirror `[lost-base] ops/fleet-dispatch.mjs:155`), so
every `mission_dispatched` line records `"unknown"` and `ev_note` is dead code.

Worked example — github-bug-bounty, the single complete record, live
round-13: 0.9×0.8×0.35×0.7 = 0.1764, gross 1764, cost 1250, adjusted_ev
**514**, positive true [corpus-attested as-of 2026-09-28T23:32Z; source tree
absent]. Two re-verifications survive the loss: the mirror's consistency gate
fails the run unless `adjusted_ev === 514` (`[lost-base] ops/rank.mjs:126-137`, assertion
`[lost-base] ops/rank.mjs:136`, "M2 verified value"), and the r15 smoke run of the mirror
`ops/ev-report.mjs` on those inputs printed 0.1764 / 1764 / 1250 / 514 / true.

| EV input | mirror INPUTS cite | mirror DEFAULTS cite | default | consumed by |
|---|---|---|---|---|
| `p_in_scope` | `[lost-base] ops/ev-report.mjs:55` | `[lost-base] ops/rank.mjs:56` | 0.7 | `p_success` `[lost-base] ops/ev-report.mjs:77` |
| `p_reproducible` | `[lost-base] ops/ev-report.mjs:55` | `[lost-base] ops/rank.mjs:56` | 0.7 | `p_success` `[lost-base] ops/ev-report.mjs:77` |
| `p_unique` | `[lost-base] ops/ev-report.mjs:55` | `[lost-base] ops/rank.mjs:56` | 0.25 | `p_success` `[lost-base] ops/ev-report.mjs:77` |
| `p_accepted` | `[lost-base] ops/ev-report.mjs:55` | `[lost-base] ops/rank.mjs:56` | 0.6 | `p_success` `[lost-base] ops/ev-report.mjs:77` |
| `expected_reward` | `[lost-base] ops/ev-report.mjs:56` | `reward.min` `[lost-base] ops/rank.mjs:92` | — | `gross_value` `[lost-base] ops/ev-report.mjs:78` |
| `effort_hours` | `[lost-base] ops/ev-report.mjs:56` | `[lost-base] ops/rank.mjs:57` | 60 | `total_cost` `[lost-base] ops/ev-report.mjs:79-81` |
| `opportunity_rate` | `[lost-base] ops/ev-report.mjs:56` | `[lost-base] ops/rank.mjs:57` | 25 | `total_cost` `[lost-base] ops/ev-report.mjs:79-81` |
| `direct_cost` | `[lost-base] ops/ev-report.mjs:57` | `[lost-base] ops/rank.mjs:57` | 0 | `total_cost` `[lost-base] ops/ev-report.mjs:79-81` |
| `delay_cost` | `[lost-base] ops/ev-report.mjs:57` | `[lost-base] ops/rank.mjs:57` | 0 | `total_cost` `[lost-base] ops/ev-report.mjs:79-81` |
| `expected_risk_cost` | `[lost-base] ops/ev-report.mjs:57` | `[lost-base] ops/rank.mjs:58` | 250 | `total_cost` `[lost-base] ops/ev-report.mjs:79-81` |

Cantina's $100 submission fee belongs in `direct_cost`; the schema's other
cost/time fields are `deadline` (`[lost-base] bounty-map/schema.json:46`), `duration_p90`
(`[lost-base] bounty-map/schema.json:47`) and `submission_buffer`
(`[lost-base] bounty-map/schema.json:48`), all inside `[lost-base] bounty-map/schema.json:35-51`.
Authoritative derivation:
`corpus/knowledge/triage-thresholds.md` §5 (its `SKILL.md:NNN` cites are
pinned to blob `fc6d398`), `corpus/knowledge/ev-model.md`.


## Gates & probes registry

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| recheck-audit.py | gate|probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | .ufo/waves/round-26/c1-receipt-index.txt | corpus/ read-only + its own receipt dir | kasegi |
| anchorcheck.py | gate|probe | python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: exit 0 clean \| exit 1 on MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT (LOST-RECORDED recorded, not fail; bounties base = `$KASEGI_BOUNTIES` override, else canonical `~/Projects/bounties`) | python3 corpus/instruments/anchorcheck.py --selftest -> one isolating fixture per limb, prints `selftest cases=N failures=0` | .ufo/waves/round-28/c1-receipt-index.txt | all inputs read-only + its own receipt dir | kasegi |

The audit is stateful against the committed expected list (the pinned receipt index): the present knowledge-entry set is compared to it, so deleting an entry is a red audit (exit 1 naming the missing entry), never a silent green pass.

## Cited paths (verified 2026-09-28 against the then-live tree; round-13 full-set re-audit 705/708 resolved — **and as of round 15 the `~/Projects/bounties` root itself is gone**, so every path below is `[lost-tree]`; **round-19 re-census (2026-10-14): the mirror and origin-work roots that used to carry the exceptions are also gone**, so there are no live exceptions left — the previous clause "unless it has a mirror equivalent in `~/Projects/the-bounty-hunter` or lives under `~/Projects/origin-work/open-bug-bounties`" is historical. Resolvability is measured, not assumed: `corpus/instruments/resolve.py`, census of record `corpus/instruments/citation-survival.md` — SKILL.md 47/289 = 16.26 % before the round-15 re-anchor, 222/486 = 45.68 % at round-15 close, re-censused at round 19; this header is itself inside the measured file, so the figure is a fixed point only to ±1 token)

- `~/Projects/bounties/fleets/mission-template.md` — L1 mission contract, six-file deliverable spec
- `~/Projects/bounties/docs/claim-runbook.md` — preflight + operator-only actions
- `~/Projects/bounties/docs/claim-ready-index.md` — generated operator queue + blocked-package table
- `~/Projects/bounties/docs/continuation-notes.md` — 486-mission class partition
- `~/Projects/bounties/docs/wrap-report.md` — GO/GO-WITH-FIX/NO-GO review evidence
- `~/Projects/bounties/docs/review-verdicts.jsonl` — drop/continue/leave ledger
- `~/Projects/bounties/docs/autopsies/` — 31 structural-failure writeups (fixed 5-part schema, generated)
- `~/Projects/bounties/ops/{claim-check,claim-index,prepare-claims,ev-report}.mjs` — fail-closed gates
- `~/Projects/bounties/claims/cantina-pendle/ingestion-20260915/` — complete positive-blocked exemplar
- `~/Projects/bounties/claims/bugcrowd-seek/honest-zero/` — complete honest-zero exemplar
- `~/Projects/bounties/bounty-map/schema.json` — program record schema (draft-07, fail-closed `additionalProperties:false`)
- `~/Projects/bounties/ledger/{missions,telemetry,candidates,imports}.jsonl` — append-only mission state machine + dispatcher heartbeat + hunter intake + board-import binding. Round-13: telemetry line counts grow between runs (`[lost-base] check-freshness.mjs:61` appends one `freshness_check` line per invocation — round-14 as-of: **7227 lines at 2026-09-28T23:32:32.720Z**; the +2 mid-round lines are `freshness_check` 23:32:22Z + a judge-lane `reroute_drill` (simulated) 23:32:32Z — same minute as an mtime-only touch on `docs/claim-ready-index.md`, bytes unchanged HEAD==worktree, actor [UNVERIFIED], not lane-originated); the worktree copy also carries 3 committed merge-conflict marker lines from a 2026-09-06 merge (JSON.parse fails on exactly those 3; the sole in-repo consumer `attempts()` is regex-only, so the fleet never notices); `rankings-*.json` = 234 artifacts / 229 stamps with zero consumers.
- `~/Projects/bounties/evidence/<program>/` — per-program audit store (592 dirs; scope-snapshots, envelopes, custodian pairs, honest-zero records)
- `~/Projects/bounties/ops/shared.mjs` — `appendLedger` (3500B O_APPEND cap) + `gitMutationBlocker` + `TELEMETRY_EVENTS`
- `~/Projects/bounties/ops/fleet-dispatch.mjs` — the `/loop` dispatcher: leases, slot rotation, sole claims/ committer, tag+push proof, model-window routing
- `~/Projects/bounties/fleets/{missions/<id>.md,run/,leases.json,claimer-mission.md,review-mission.md,priority.json,state-snapshots/}` — generated L1 assignments, status file-protocol, sibling-lane contracts
- `~/Projects/bounties/docs/RUNBOOK-resume.md` — snapshot restore + dispatcher relaunch procedure
- `~/Projects/bounties/.ufo-mission-report-bh*.md` — 22 hunter-mission readiness-audit reports (20 BLOCKED, 2 READY: intigriti-yahoo + hackerone-superhuman)
- `~/Projects/bounties/.ufo-{ingestion,warden}/` — intake-cycle + readiness-tracker artifacts for the origin-work claim tree
- `~/Projects/bounties/ops/park-disposition.mjs` — PARKED/FAILED detail-regex classifier; producer of all `docs/autopsies/*` and the RETIRED rewrite + `mission_retired` telemetry
- `~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs` — integrity gates: schema+referential, lane↔card bijection/k3/grok-pin, simulation-only reroute drill, 26 h live-source staleness alarm
- `~/Projects/bounties/ops/{import-board,finalize-all}.mjs` — evidence-bound program feed and batch claim tag+push sweep (other beyond-`ledger/` writers: `rank.mjs` → `bounty-map/programs` + `ledger/rankings-*`; `fleet-dispatch`, `park-disposition`, `prepare-claims`, `claim-index`)
- `~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh` — `ufo_sighting` observation windows (display only)
- `~/Projects/bounties/fleets/ufo-archive-2026/` — pre-consolidation fleet snapshot: 20 `claim-*` hardening missions (defect census), `bounty-keeper` (b1k-NNN origin), L0 mission briefs, old per-program evidence shape
- `~/Projects/bounties/bounty-map/{schema.json,programs/*.json}` — 1088-record census: single refresh run, decorative `mission_state`/`lane`/`ev_inputs`, 352 untouched, map↔claims name drift
- `~/Projects/bounties/.ufo-ingestion/{cycle-20260914T171257Z.md,rankings.md,claim-tracker.py,claim-ready-tracker.*}` — the second intake path + dead continuous watcher over claims/ AND origin-work claim-packages
- `~/Projects/bounties/fleets/registry.json` — lane/bucket routing + `operator_decrees` ledger (claim queue, 3cx/intel/anthropic dispositions, disclosure-class guardrails)
- `~/Projects/bounties/.ufo/bh*/` + `.ufo/bounty-fleet/sessions/bh*/` — 25 warden-audit workspaces (`plan.md`, `proposals/<Agent>.md`, `reroutes.jsonl` model-fallback log); untracked, invisible to every ops scan
- `~/Projects/bounties/.ufo/bounty-fleet/` — overnight bountyfleet1/b1k-NNN keeper tree: own `ledger/missions.jsonl` (second state machine), `plan-b1k-*.md` ×233, `report.md` halt, `reports/` (249 b1k + 8 claim reconciliations), `scopes/`, `session/` vs `sessions/`
- `~/Projects/bounties/.ufo/sessions/` — bpolish1..8 omp-recorder-v3 transcripts (2026-09-15); zero submission evidence; grep-trap corpus
- `~/Projects/bounties/.ufo/{grok-bounty-assessment-20260911,claim-recovery}/` — frozen 266-mission reconciliation (88.30 descriptive, gate BLOCKED, self-invalidating validator) + b1k post-mortem (`final-audit.json`, superseded in place by the package readiness-audit)
- `~/Projects/bounties/.omp/{config.yml,agents/,skills/}` — second routing truth: live `config.yml` ≠ README/HEAD; 11 cards (9 tracked); registry-check RED; drifted untracked `skills/ufo` fork
- `~/Projects/bounties/{README.md,.gitignore}` — README describes git HEAD, not the live router ("9 lanes" stale = 10); asymmetric 11-line ignore set (`fleets/run/` ignored by design, `.ufo/` bulk mostly not)
- `~/Projects/bounties/.git/` — stalled interactive rebase (onto `7dce2872`, detached `58acb6d8`, 0 commands left, autostash present), 903 dirty entries, all 12 `claim-*` tags pushed, `claim-ship` a superseded ancestor line
- `~/Projects/bounties/pendle-core-v2-public/` — vendored hunt target (shallow clone, `f242659` = v6.10.0, pinned by `claims/cantina-pendle/…/provenance.json`); 187/255 provenance files carry a `pin` — `claim-check.mjs` never validates pins

## Frontier decision table (round 22)
Use the source IDs in `corpus/SOURCES.md` to trace these report-review rules to their current public guidance; each entry was admitted against `corpus/QUALITY.md` (Q1–Q6).

| situation | rule | entry | source |
|---|---|---|---|
| A report states a CVSS v4.0 number | Include its vector and metric-group label; CVSS-B alone is severity, not a complete risk assessment. | `corpus/knowledge/cvss-v4-severity-and-vector.md` | S001, S002 |
| A disclosure date or deadline is discussed | Name the policy, trigger, patch relationship, and documented exceptions; do not assume one universal interval. | `corpus/knowledge/coordinated-disclosure-timelines.md` | S003–S005 |
| A program displays safe harbor | Check its actual asset scope, testing grant, and prohibited methods separately; a badge does not expand scope. | `corpus/knowledge/authorization-safe-harbor-and-scope.md` | S006–S008 |
| An AI system produces a finding | Keep it a candidate until reproduced and human-reviewed for impact and reachability; preserve program-specific AI rules. | `corpus/knowledge/ai-assisted-finding-validation.md` | S009–S012 |
| A report cites the 2025 CWE Top 25 | Use a technically supported root-cause mapping; do not turn aggregate rank into target risk or reward. | `corpus/knowledge/cwe-top25-2025-methodology.md` | S013–S015 |

Round-28 note (2026-10-25, supersedes the frozen C1 `corpus_disclosure` cell): zero backticked anchored `~/Projects/bounties/` citations exist lane-wide, so the new `BOUNTIES-ABSENT` arm in `CITE` is invisible to all existing bytes — no verdict-class movement on any file, corpus or `SKILL.md` (erratum, with the sweep command and scratch probe: `.ufo/waves/round-28/claims-erratum-1.md`).

## Round-29 Gates & probes registry addition (appended 2026-10-25)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| anchorcheck.py | gate|probe | python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: exit 0 clean \| exit 1 on MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT (LOST-RECORDED recorded, not fail; bounties base = `$KASEGI_BOUNTIES` override, else canonical `~/Projects/bounties`) | python3 corpus/instruments/anchorcheck.py --selftest -> one isolating fixture per fail limb, prints `limbs=9 covered=9` and `selftest cases=12 failures=0`, exit 0; git-free PATH run (env -i PATH=<python-only>) skips `pin-broken` (`SKIP pin-broken (git not found)`) and exits 0 — clean skip, no traceback | .ufo/waves/round-29/c1-receipt-index.txt | all inputs read-only + its own receipt dir | kasegi |

This row records the round-29 state of the same instrument as the row above (R6 append; no existing line moved). It carries the round-29 selftest completeness (limbs=9 covered=9, cases=12) and hermetic git-free behavior for that measurement.

## Round-29 frontier note (appended 2026-10-25)

F13 — program severity ladders and reward scales — admitted 2026-10-25; entry `corpus/knowledge/program-severity-ladders-and-reward-scales.md`; sources S043 (HackerOne standard program policy set), S044 (Bugcrowd VRT README), S045 (Bugcrowd VRT CWE crosswalk); captures pinned in `corpus/source-snapshots/round-29/manifest.json`. (F13 is the first frontier row whose admission this round is tied to sources first registered this round as S043–S045.)


## Round-30 Gates & probes registry addition (appended 2026-10-25)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| frontier-recheck-count.py | gate|probe | python3 corpus/instruments/frontier-recheck-count.py [--root DIR] [--json PATH] | exit 0 when every admitted Frontier row passes (recheck `--source` ids ⊇ header `source:` ids, ⊆ cited ids, named manifest exists/schema-valid/lists them, line is a `source-recheck.py` invocation); exit 1 on any failing row or fail-closed condition (missing entry → `problems=missing-entry` naming the row and path; two admitted rows resolving to the same entry realpath → `DUPLICATE-ENTRY` naming both); exit 2 on harness/read error | no built-in `--selftest`; discrimination exercised by the committed C1 controls `.ufo/waves/round-30/c1-controls/harness-root-a1` (missing entry → exit 1 naming the row) and `harness-root-a2` (duplicate target → exit 1 naming the duplicate) | .ufo/waves/round-30/c1-controls/before.txt | all inputs read-only + its own receipt dir | kasegi |
| source-recheck.py | gate|probe | python3 corpus/instruments/source-recheck.py --manifest <path> --source S### | exit 0 when every pinned assertion for the asked id verifies (sha256 OK; quote exactly-once in the capture, or its declared `anchor` line verifies; capture file stem == record id); exit 1 on a failed assertion (`reason=stem-mismatch` / `reason=occurrence-not-unique` / `reason=anchor-out-of-range` / `reason=anchor-broken` / `reason=quote-not-found` / sha `MISMATCH`); exit 2 on UNAVAILABLE (manifest-level reasons plus `invalid-path`, `invalid-sha256`, `missing-quotes`, `invalid-quote-id`, `quote-too-short-to-be-evidence`, `outside-manifest-directory`, `not-utf8`, `not-listed`) | python3 corpus/instruments/source-recheck.py --selftest -> isolated clean / corrupt / missing-source / missing-manifest / stem-mismatch / double-occurrence (+anchored, out-of-range, broken) controls, exit 0 only when all pass | .ufo/waves/round-30/c1-controls/before.txt | all inputs read-only + its own receipt dir | kasegi |

These rows register the two wave-C1 instruments absent from the earlier registry (the rounds-23/24-onward verdict surface). Measured at append time (working tree, 2026-10-25): frontier-recheck-count.py sha256 `bab0d321f75f…`, source-recheck.py sha256 `0b841d5ddb80…` (committed base analogues in `.ufo/waves/round-30/c1-controls/before.txt`: `c8a62888…` / `9fe6a4a0…`). Counter smoke at those bytes: A1 exit 1 naming F98; A2 exit 1 via a `NameError` traceback (duplicate limb mid-landing); B1 exit 1 `reason=stem-mismatch`; B2 exit 1 `reason=stem-mismatch` (fixture capture stem precedes the occurrence limb); source-recheck selftest `cases=9 failures=1` (stem-mismatch fixture) — the rows record the contract the landed fix must satisfy; post-integration re-runs belong to `ExecPostCommitRecheck`.


## Round-31 Gates & probes registry addition (appended 2026-10-25)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| limb-mutation-check.py + limb-ledger.json | gate\|probe | cd <lane> && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json | exit 0 iff 13 `LIMB ` lines all print `verdict=killed`, then `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3`; exit 1 on any `survivor`/`invalid:*`/control mismatch; exit 2 on usage, ledger or lane-root error. Per row, in run order: `invalid:live-baseline` (unmutated exit ≠ `live_exit` or `signal` no match) → `invalid:find-count` (`find` not exactly once) → `invalid:noop` (mutant bytes == original) → `invalid:nocompile` (`py_compile` fails) → `invalid:timeout` (120 s) → else `killed` when the mutant's exit differs from `live_exit` or its stdout+stderr loses `signal`, else `survivor` | python3 corpus/instruments/limb-mutation-check.py --selftest -> one fixture per verdict path (killed, survivor, find-count, noop, nocompile, live-baseline, timeout), 5 ledger-validation cases and 3 aggregate/control cases; 1 s command timeout so the timeout path is provable: `selftest cases=16 failures=0`, exit 0 | .ufo/waves/round-31/wave1/ExecLedgerMerge.md | scratch only (`tempfile.mkdtemp`, deleted at exit); no lane write, no git | kasegi |
| score-gap.py | reporter (read-only, NOT a claim) | cd <lane> && python3 corpus/instruments/score-gap.py [--root DIR] | exit 0 on a complete read even when the gates it reads are red — it reports, it does not judge; exit 2 when an input is missing/unreadable or no longer yields its field (`score-gap: INPUT-UNREADABLE …`) | python3 corpus/instruments/score-gap.py --selftest -> two fixture lanes differing in every field, each field must move and each fixture tree digest must be unchanged after the run, plus 4 unreadable-input cases asserted rc=2: `selftest fields=7 failures=0`, exit 0 | .ufo/waves/round-31/wave1/ExecScoreGap.md | none (opens inputs read-only; no JSON, no receipt, no `__pycache__`) | kasegi |

`limb-mutation-check.py` + `limb-ledger.json` are the round-31 one-limb mutation surface (R13 in executable form): per limb it runs the limb's `kill` command on an unmutated scratch copy of `corpus/` (baseline), applies exactly one `find`→`replace` patch, and runs the same command again — `killed` only when the mutant changes the observable result, so a limb is shown load-bearing against the instrument's own `--selftest`/fixtures instead of asserted. 13 limbs in frozen order: RA-parse, RA-cwd, RA-paths (recheck-audit frozen limbs a–c), RA-cdroot, RA-instrument, RA-own (strict limbs d–f), RA-completeness, RA-expect-missing, RA-expect-unexpected — 9 on `corpus/instruments/recheck-audit.py`, each killed by one isolating `--selftest` case (`parseonly.md`, `cwd.md`, `ghost.md`, `elsewhere.md`, `instonly.md`, `selftesty.md`, the two `complete-*` fixtures, `expect-missing`, `expect-unexpected`); SR-stem-mismatch, SR-occurrence-not-unique — 2 on `corpus/instruments/source-recheck.py` against `corpus/instruments/limb-fixtures/sr/` (B2's fixture is stem-correct, closing M30-1's confound); FR-missing-entry, FR-duplicate-entry — 2 on `corpus/instruments/frontier-recheck-count.py` against `corpus/instruments/limb-fixtures/fr/` (the missing-entry row is killed by signal, not exit: the mutant still exits 1 with a traceback). Expected lines, byte-exact: `LIMB <id> live=<exit>/<sig:y|n> mutant=<exit>/<sig:y|n> verdict=killed`, `CONTROL <id> verdict=<v> expected=<e> ok=y`, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`. The 3 controls are the counter's own negative proof: CTL-noop (`find` == `replace` on `def digest(data):` → `invalid:noop`), CTL-nocompile (that line loses its colon → `invalid:nocompile`), CTL-equivalent (a comment appended to `def normalize(text):` in source-recheck.py, same exit and `reason=stem-mismatch` → `survivor`); a naive harness that only runs the mutant reports those as survivor and killed respectively, so both pre-mutant gates are load-bearing (`.ufo/waves/round-31/wave1/ExecLedgerMerge.md` §7).

Measured at append time (working tree, 2026-10-25): ledger sha256 `c042adf6…`; counter `f926bf75…` (the merge receipt's FINAL was `cde7c2b6…`; the file moved once more after that merge and both digests print the same 18 lines — per M30-3 this row pins behaviour, not one digest); the three instruments at `5d4842da…` (recheck-audit), `fd2e01e8…` (source-recheck), `aa60b581…` (frontier-recheck-count). Counter exit 0 in ~10 s from the lane root, and with an absolute `--ledger` from `/tmp` — the default root derives from the script path, so `cd <lane> &&` is canonical, not required. No-harm on the same bytes: `recheck-audit.py --quiet` → `strict pass=44/44`, exit 0; `source-recheck.py --selftest` → `cases=10 failures=0`; `frontier-recheck-count.py` → `entries=18 pass=18 exit=0`. Known limits: it proves a limb load-bearing against the instrument's own selftest/fixtures only — the SR/FR limbs run on committed `limb-fixtures/` trees, not on the 44 live recheck lines, so a green ledger says nothing about those; a limb id is a label, not a proof of the patched line (the frozen row schema has no `reach` field), mitigated by each row's `note` naming its implementing line and isolating fixture plus the hand re-derivation of all 16 rows in the merge receipt, with a full `reach` gate routed to the L1; `invalid:timeout` is emitted but sits outside the frozen verdict enum (routed); equivalent mutants are reported honestly as `survivor`, which is exactly what CTL-equivalent proves; and it is scratch-only and git-free, so it proves nothing about the lane's git state.

`score-gap.py` answers considerthese/2026-10-25.md proposal 2 as a read-only reporter: the four committed-byte measurements that decide whether depth:verifiability 5 is reachable, each with the command it came from, then one computed `gap` line. Measured at append time: `recheck: lines=44 executes=20 gated=24 broken=0 exit=0` (from `recheck-audit.py --root <root> --quiet`); `anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0` (from `anchorcheck.py SKILL.md` with cwd=root); `census-lane: 134/1480 = 9.05%` and `census-skill: 32/506 = 6.32%` quoted from `corpus/instruments/citation-survival.md` with its own definition sentence; the score-5 bar quoted from `SCORECARD.md` line 331 — "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."; and `gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`, computed from field 1 and never typed. Every run also prints `source: <rel> sha256=<…>` for its four inputs, so a number traces to bytes. It is not a claim and asserts no score move; exit 0 even when the gates it reads are red, exit 2 when an input no longer yields its field (a reworded SCORECARD bar goes loud rather than printing a stale line). Its census field is the committed r18 census of record, not a live `resolve.py` re-run — that rewrites the census and belongs to another seat; limits in `.ufo/waves/round-31/wave1/ExecScoreGap.md` §8.

## Round-33 Gates & probes registry addition (appended 2026-10-26)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| capture-binding-check.py | gate\|probe | cd <lane> && python3 corpus/instruments/capture-binding-check.py [--root DIR] | exit 0 iff no `FAIL` line; 1 on any `FAIL`; 2 on `UNAVAILABLE reason=no-snapshot-tree\|read-error\|manifest-JSONDecodeError\|manifest-shape\|record-shape`. A `FAIL rule=missing-manifest dir=<dir>`; B1 `FAIL rule=no-row record=<id>`; B2 `FAIL rule=dup-id record=<id> rows=<n>`; B3 `FAIL rule=url-mismatch record=<id> [row=<id>\|detail=absent]`; C `FAIL rule=provenance-missing record=<id> dir=<dir>`, a `round-32`+ dir (or an unparsable name, fail-closed) refusing the `archival` exemption | cd <lane> && python3 corpus/instruments/capture-binding-check.py --selftest -> one subprocess run of this file per fixture lane tree: 11 `selftest case=<name> exit=E want=W verdict=pass` lines then `selftest cases=11 failures=0`, exit 0 | `.ufo/waves/round-33/wave1/ExecCaptureBinding.md` | inputs opened read-only, nothing written; fixtures under `--scratch` else `$HYAKU_SCRATCH` else `$TMPDIR`, removed in `finally` | kasegi |

It proves manifest *binding*, not capture truth: each `corpus/source-snapshots/*/manifest.json` record must sit in a manifest-carrying dir, name the row of its own id (`corpus/SOURCES.md:55-56`, the S049/S050 rows), and carry `fetched_utc` or `"archival": true`; grammar at `corpus/instruments/capture-binding-check.py:1-92`, binding at `corpus/instruments/capture-binding-check.py:166-181` inside `corpus/instruments/capture-binding-check.py:184-262`.
Rule-B id scoping is the L1 erratum `.ufo/waves/round-33/claims-erratum-1.md:1-36`: S024/S029 and S006/S028 share a URL and only raise the informational `multi_row_url=N`.

Measured on quiescent bytes, digest `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` (492 lines, two `diff`-identical runs, `corpus/SOURCES.md` at 50 rows): 9 `MANIFEST` lines (round-23 4/4, round-24 19/19, round-25 5/5, round-26 1/1, round-28 2/2, round-29 3/3, round-30 3/3, round-31 1/1, round-32 2/2 `fetched=2`), then `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2` and `records=40 bound=40 unbound=0`, exit 0.

Bound captures `corpus/source-snapshots/round-32/S049.txt` + `corpus/source-snapshots/round-32/S050.txt`; receipts `.ufo/waves/round-33/wave1/ExecCaptureBinding.md` §4, `.ufo/waves/round-33/wave1/ExecManifest32.md` §1, `.ufo/waves/round-33/wave1/ExecManifestUpgrade.md`.

Known limits (measured; attack list `.ufo/waves/round-33/wave1/CritC1Kill.md`): registry-text identity only, never page content — that is `corpus/instruments/source-recheck.py`'s sha256+quote job; siblings it does not replace: `corpus/instruments/recheck-audit.py`, `corpus/instruments/anchorcheck.py`, `corpus/instruments/frontier-recheck-count.py`, `corpus/instruments/limb-mutation-check.py` over `corpus/instruments/limb-ledger.json`.

A 0-byte or deleted capture still scores `bound=40`; `fetched_utc` is presence, not RFC3339 (`"pending"` binds); the walk is one level (a nested snapshot dir is invisible); two records with one id print `records=41 bound=41`; a record binds to a `rejected` row.

Re-verify: `cd <lane> && sha256sum corpus/instruments/capture-binding-check.py` (target `b4182665…`) then the two commands above; `bound` below `records` is a real unbound record, and exit 1 with only `no-row`/`url-mismatch` on a `round-32` dir means the registry rows landed after the manifest.
[round-34 correction, appended 2026-10-26, end-of-file append per R6] The `capture-binding-check.py` row above pins digest `b4182665…`, 492 lines and `selftest cases=11 failures=0` as measured on 2026-10-26 (round 33). Round 34 hardened the same file: it re-measures at `sha256sum` `3d9e5e0d…` (892 lines) and `--selftest` prints `selftest cases=23 failures=0` (exit 0), the nine cases named in the round-34 C1 predicate being per-file-orphan-detected, per-file-orphan-listed, nested-snapshot-dir, fetched-utc-pending-rejected, fetched-utc-local-offset-rejected, dup-record-in-manifest, double-https-row, rejected-row-anchor and summary-only-selftest-rejected. The row's digest and case count are the round-33 measurement, not a target: re-verify with `sha256sum` (target `3d9e5e0d…`) and the row's two commands.

## Round-35 Gates & probes registry addition (appended 2026-10-26)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r-defect-closure.sh | gate\|probe | `bash corpus/instruments/r-defect-closure.sh [--root DIR]`; the root defaults to this script's lane and every check honours `--root`, so the base-tree control is `bash corpus/instruments/r-defect-closure.sh --root <base-extraction>` | plain run: one `R# check=<desc> open=0\|1` line per check R1–R9, then `closed=K/9 exit=0\|1`; exit 0 only for K=9, exit 1 while any check is open or when the suite's self-report judgement fails (`suite problem=self-report plain-lines=N expected=9`), exit 2 on harness error (`suite UNAVAILABLE reason=root-argument-missing\|root-missing\|scratch-argument-missing\|unknown-argument`). Each check exits 0 when its round-33 defect is CLOSED and non-zero while it is still OPEN, so a summary-only printer cannot read `closed=9/9` on defect-bearing bytes | `bash corpus/instruments/r-defect-closure.sh --selftest [--scratch DIR]` -> per check one `selftest case=R# live=pass fixture=rejected control=pass\|absent verdict=pass` line (or `verdict=fail problems=...`), then `selftest judge=forged-summary rejected=1`, `selftest judge=short-report rejected=1`, `selftest judge=complete-report accepted=1`, then `selftest cases=9 failures=0`; exit 0 only when all nine live runs pass, every defect fixture is rejected and the complete report is accepted, exit 1 on any case failure or `selftest problem=self-report ...`, exit 2 on `selftest UNAVAILABLE reason=scratch-missing\|scratch-create-failed` | the pinned expected values are the check literals inside `corpus/instruments/r-defect-closure.sh` (R1 `7963976e`/`014ee2d`; R2 `0 or 2+`, `multi_row_url`, `dup-id`, R22 satisfiability; R3 `R20`/`exactly one`/superseded; R4 kill-rule prose plus one `selftest case=` line; R5 no `url-matching-two-rows`; R6 `S040-live.txt`; R7 `19->31`, `23->22`, `corpus/source-snapshots/round-32/S050.txt:70`; R8 the `Z`/`+00:00`/fractional accept set; R9 the nine capture-binding case names plus frontier rule A mirror/reverse), measured against the committed files they read (`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-33.md`, `corpus/source-snapshots/round-26/manifest.json`, `corpus/source-snapshots/round-32/manifest.json`); the frozen before-state they discriminate is `.ufo/waves/round-34/c1-controls/before.txt` | read-only on the lane: every check only reads files under the root; the only writes are its own scratch fixtures under `--selftest` (scratch base = `--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`, else `/tmp`), removed on exit; no git command is run and nothing outside the scratch directory is written | kasegi-shokunin |
| kill-rule-check.py | gate\|probe | `cd <lane> && python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH] [--root DIR] [--scratch DIR] [--row-file PATH] [--json PATH]` (the default root derives from the script path, so the `cd` is canonical rather than required; default instrument `corpus/instruments/capture-binding-check.py`) | header `KILL-RULE instrument=... sha256=... bytes=... lines=... floor=19 counter_sha256=...`; one `probe <name> pristine=pass\|fail exit=...` per probe (`selftest-shape` plus the eight fixture lanes); per row `mutant-patch ... status=ok\|invalid:<reason>`, `mutant-bytes`, one `mutant-probe ... pristine=pass mutant=pass\|fail`, `mutant=<name> killed=0\|1`, `mutant-invalid`; `control=CTL-{noop,nocompile,equivalent,fake-killrule} verdict=... expect=... ok=0\|1`; `controls=4 rejected=K`; `GATE ok\|fail name=<named-rows\|pristine-selftest\|pristine-fixtures\|pristine-determinism\|rows-valid\|controls\|survivors-zero>`; `mutants=3 killed=K survivors=K invalid=K`; `gates=7 failed=K`; final `survivors=K`. Exit 0 iff `survivors=0` AND `invalid=0` AND `failed=0`; exit 1 on any survivor, any invalid row, or any failed gate (the CTL-equivalent witness deliberately prints `survivors=1`, exit 1); exit 2 on `UNAVAILABLE reason=instrument\|row-file`. `invalid:` reasons are `find-count`, `noop`, `nocompile`, `anchor-mismatch`, `nondeterministic`, `inconsistent-kill` — an invalid row is never relabelled killed and never counted as a survivor | `python3 corpus/instruments/kill-rule-check.py --selftest` -> three arithmetic scenarios, each `selftest case=<name> got=<(killed,survivors,invalid,exit)> want=<...> verdict=pass\|fail`, then `selftest cases=3 failures=0`; exit 0 iff `failures=0`, else 1; it runs no instrument and no subprocess | `corpus/instruments/kill-rule-check.py` itself: the three `MUTANTS` patches, their `ROW_PINS` `find` and `find\0replace` sha256 literals, `CASE_FLOOR = 19`, and the CTL patch anchors; the do-nothing fake control is the newest `.ufo/waves/round-*/c1-controls/fake-killrule.py` (round 35 carries none, so round-34's file binds; `--fake PATH` overrides) | read-only on the lane: reads the instrument under test and writes only scratch fixture lanes, mutant copies and their `pyc` under its scratch root (`--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`), removed on exit; `--json PATH` writes only that path | kasegi-shokunin |

These two rows close spotcheck defect **D3** (`corpus/lessons/round-34-verifier-spotcheck.md:177`: "gates unregistered at the registry home"; before the append `grep -c 'r-defect-closure' SKILL.md` → 0 and `grep -c 'kill-rule-check' SKILL.md` → 0). They are registration, not a live-green claim: the parent runs both instruments post-integration.

Measured at append time (working tree, 2026-10-26): `r-defect-closure.sh` sha256 `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d` (832 lines, nine checks R1–R9, `CHECK_IDS=(R1 … R9)`); `kill-rule-check.py` sha256 `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` (881 lines, three `MUTANTS`, nine `PROBES`, three patch-shape controls plus the fake, seven gates); instrument under test `capture-binding-check.py` at `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (892 lines). The round-34 receipts on those behaviours: `.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md:505-507` (live suite `closed=9/9 exit=0`, `selftest cases=9 failures=0`, exit 0) and `.ufo/waves/round-34/wave1/MutSelftestSummary.md:332` (`mutants=3 killed=3 survivors=0 invalid=0`, `survivors=0`, exit 0 — that receipt records the then-current `gates=6`; the committed source now lists seven gates, so read `gates=7 failed=0`, not the receipt's count).

Re-verify: `sha256sum corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py` (targets `809aaf90…` / `c279d952…`) then `bash corpus/instruments/r-defect-closure.sh --selftest` → `selftest cases=9 failures=0` exit 0, and `python3 corpus/instruments/kill-rule-check.py --selftest` → `selftest cases=3 failures=0` exit 0. The plain runs' expected values are `closed=9/9 exit=0` and `survivors=0` exit 0; this row records the contract read from the committed source and the round-34 receipts — it is not a round-35 run, so the parent's post-integration gate is what turns those two into measured values. A digest move is not a verdict move: re-read the row against the bytes, and if the case set or gate list changed, append a correction (R6) instead of editing this row.

## Round-36 Gates & probes registry addition (appended 2026-10-26)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r35-defect-closure.sh | gate\|probe | `bash corpus/instruments/r35-defect-closure.sh [--root DIR]` | plain run prints one `D# …` line per check D1–D7 then `closed=K/7 exit=0\|1`; exit 0 only for K=7; `--selftest` prints `cases=7 failures=0` | `bash corpus/instruments/r35-defect-closure.sh --selftest` -> `selftest cases=7 failures=0` exit 0 | base export `3266c993` -> `closed=0/7 exit=1` | read-only | kasegi (round 35; exact-basename registration round 36) |
| r36-closure.sh | gate\|probe | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2) | one `E<n> payload=… closed=0\|1` line per check E1–E9, then `closed=K/9 exit=0\|1`; exit 0 only for K=9 | `bash corpus/instruments/r36-closure.sh --selftest` -> `selftest cases=9 failures=0` exit 0 | r35 base export `3266c993` -> `closed=0/9 exit=1`; r35 judged head `0aee0ef` -> `closed<9/9 exit=1` | read-only (export to a scratch work dir) | kasegi (round 36) |
