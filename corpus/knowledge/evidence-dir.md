# `evidence/<program-id>/` — the per-program audit store

Source: `find`/`ls` census of `[lost-tree] ~/Projects/bounties/evidence/` (592 program
dirs), exemplars `evidence/bugcrowd-seek/` and `evidence/sherlock-8/`,
`ops/fleet-dispatch.mjs`, `docs/plan-round0.md`. Counted 2026-09-28.

## It is NOT the same tree as `claims/*/*/evidence/`

| | `evidence/<program>/` (top-level) | `claims/<program>/<slug>/evidence/` |
|---|---|---|
| Scope | one dir per **program** (592) | one dir per **package** |
| Written by | missions, dispatchers, custodian, hunts | package wrap only |
| Contract | schema-versioned records, heterogeneous | `manifest.json` (evidence-manifest/v1) — strict |
| Validated by | nothing structural; missions append freely | `ops/claim-check.mjs` (fail-closed) |
| Lifespan | whole mission history incl. retries/supersession | frozen at wrap; manifest-bound |

`ops/fleet-dispatch.mjs` `SYNC_PATHS` lists `evidence` as a synced path —
the store is part of the repo's committed state, not scratch.

## Canonical files (frequency across 592 dirs)

| Count | File | Role |
|---|---|---|
| 583 | `scope-snapshot.json` | the AR14 bounded policy read (mission step 1) |
| 580 | `authorization-envelope.json` | grant scope derived from snapshot bytes |
| 532 | `provenance.json` | agents/models/commands/hashes per transition |
| 514 | `custodian-receipts.json` | program-level custodian decision chain |
| 407 | `manifest.json` | artifact manifest |
| 346 | `honest-zero-record.json` | schema `honest-zero/v1` terminal record |
| 275 | `status.json` | per-program terminal state (PARKED etc.) |
| 195 | `redaction-policy.json` | what may leave the repo |
| 191 | `negative-findings.json` | bounded negative result inventory |
| 146 | `mission-axes.json` | mission classification axes |
| 99  | `redaction-verification.json` | redaction sweep receipts |
| 77  | `honest-zero.json` | earlier honest-zero schema variant |
| 71  | `negative-auth-walled.json` | auth-walled negative class |
| 54  | `normalized-scope.json` | normalized scope model |
| 53  | `custodian-input.json` | custodian request input |

Beyond these the tail is ~free-form per-program artifacts (apk manifests,
probe outputs, `audit-*.json`, `*.sha256` files). The store tolerates
heterogeneity — the *claim package* is where the strict contract applies.

## Common subdirs

`raw/` (244 dirs) — unprocessed fetched bytes: `policy-page.html`,
`policy-text.txt`, `platform-rules.md`, `validity-criteria.html`.
`history/` (154) — superseded versions, e.g.
`authorization-envelope.v1.json` beside a `scope-supersession.json`.
`custodian/` (27) — paired `input.<action>.json` / `decision.<action>.json`,
with `.hard-stop` suffix on denied actions; `custodian-inputs/` +
`custodian-decisions/` is an alternate pair naming.
`runs/`, `round-N/` (e.g. `hackerone-1password/round-1`,
`hackerone-dyson/rounds/round-1..3`) — per-attempt isolation (round-13
correction: the earlier `raw-rN/` dir naming does not exist; raw bytes live
in `raw/`, 244 dirs above).
`source/`/`src/`/`repos/` — cloned target repos for local hunts.
`specialists/` — L2 verdict JSONs (`round-1-scout.json`…).
`b1k-NNN/` under ~30 program dirs — per-run output keyed to the
`the-bounty-hunter` run_ids in `ledger/candidates.jsonl`.

## `honest-zero-record.json` (schema `honest-zero/v1`)

Fields: `mission_id`, `program_id`, `verdict` (e.g.
`honest-zero-scope-unverifiable`), `title`, `state:"PARKED"`,
`stopped_at_transition`, `basis[]` (verbatim evidence reasons incl.
custodian HARD_STOP decision hashes), `finding:null`,
`claim_deliverable:null`, `effort{started_at, stopped_at, elapsed_minutes,
policy_fetch_attempts, follow_up_network_requests, active_test_attempts,
submission_attempts}`, `ev{as_of, expected_reward, p_success, adjusted_ev,
basis}` with `unknown` values not coerced, `no_submission_performed:true`.

`evidence/<program>/status.json` mirrors it: `{state:"PARKED", verdict,
title, mission_id, manifest_sha256, deliverable:null, evidence_path,
stopped_at_transition, reason, no_submission_performed:true}`.

## Adjacent unwalked dirs (status this round)

- `vgn-bounty-lab/` — `git init`'d 2026-09-04, **zero commits, no files**.
  Empty scratch; gap closed as "nothing to learn".
- `george/` — 49G comma.ai bounty research workspace (`calibration/`,
  `controls/`, `commavq/`, `bounty-*/`, 2405 txt files, `.sessions/` L2
  transcripts). **Zero claims dirs reference it** — parked as out-of-skill
  research substrate; revisit only if a claim package ever cites it.
- `pendle-core-v2-public/` — vendored target repo for the Pendle claim.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/evidence/ census (592 program directories), ops/fleet-dispatch.mjs, docs/plan-round0.md, and evidence exemplars.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/evidence-dir.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
