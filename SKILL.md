---
name: kasegi-shokunin
description: Domain specialist — bounty & security research — scopes ~/Projects/bounties, program rules, claim packages. Rank: shonen.
---

# kasegi-shokunin — bounty & security research craft

Grounded in `/home/vgpnk/Projects/bounties` (UFO fleet HQ): 275 claim packages
under `claims/`, 1088 program records under `bounty-map/programs/`, a 486-line
verdict ledger at `docs/review-verdicts.jsonl`, and the operator-facing queue
at `docs/claim-ready-index.md`. Every rule below cites a file you can open.

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
(`claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json`):

- [ ] `url`, `fetched_at`, `content_sha256` of the official policy page
- [ ] `in_scope_assets[]` — exact asset names. Generic prose ("we invite you
      to test our web applications") is NOT an asset.
- [ ] `out_of_scope[]` + `prohibitions_verbatim[]` — copy the text, do not
      paraphrase (SEEK's: no automated tooling, customer instances forbidden,
      @bugcrowdninja.com identity required, AI-generated reports rejected)
- [ ] `testing_grant_verbatim[]` — the sentence that grants testing, verbatim
- [ ] `safe_harbor` — record `null` when absent; distinguish SEAL Whitehat
      (active exploits only) from a routine-research safe harbor
      (`claims/cantina-pendle/ingestion-20260915/INGESTION.md`)
- [ ] `reward_table_url`, reward band, currency
- [ ] `coverage.status` — `incomplete` when the fetch is a login shell;
      `coverage.missing[]` names exactly what was absent

Program quirks to check before planning work:
submission fee (Cantina Pendle: $100 — `claim_checklist.md` §1 makes a
live-balance check the claimability gate), KYC requirement, AI-disclosure
requirement, evidence-source parity (deployed bytecode ↔ repo commit pin —
`provenance.json.pin`).

### Policy access playbook (fleet-learned)

| Platform | Reality | Move |
|---|---|---|
| HackerOne | HTML is a JS shell | Public GraphQL `team(handle)` query — policy/scope/structured_scopes, no auth |
| Bugcrowd | Auth-walled SPA for anonymous fetches | Try public brief/changelog JSON once; else park at SCOPED, don't burn budget |
| Immunefi/Cantina/HackenProof | Public bounty pages with contract scope | Capture page HTML into `evidence/`; hash it (`policy_sha256` in provenance) |
| RFC 9116 security.txt | A stub is not a scope | No assets + no grant → park |
| Terms-gated policy (SIX Group) | Reading requires accepting Program Rules | Terms acceptance is a forbidden external effect → autopsy + retire |

## Finding-triage decision table

Terminal classes observed across 486 non-claim-ready missions
(`docs/continuation-notes.md`) and the claim queue:

| Condition | Class | Package state | Evidence |
|---|---|---|---|
| In-scope finding, reproducible locally, reviewer APPROVED, all gates PASS | Claimable | `status.json state:"DONE", claimable:true` | `docs/claim-ready-index.md` (12 queued) |

| Defect proven, live precondition unverified (e.g. needs read-only chain/state check) | Positive-blocked | `state:"BLOCKED", verdict:"positive-blocked-*", claimable:false`, `resume_condition` set | `claims/cantina-pendle/ingestion-20260915/status.json` |
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

## Mission ledger & audit store

`ledger/missions.jsonl` is the append-only hunter-contract state machine
(writer: `ops/shared.mjs::appendLedger`, 3500-byte line cap for O_APPEND
atomicity). Transition census (718 lines / 260 missions):
`SCOPED` 232 → `PLANNED` 219 → `LEARNED` 244 dominates;
`SCOPED→PLANNED→LEARNED` alone is 207 missions. Deep path
`EXECUTED→EVIDENCED→VERIFIED→SUBMISSION_PREPARED` is rare; `SUBMITTED` (3)
and `DISCLOSED_FREE` are operator-attributed ledger facts, never fleet
actions. `ledger/telemetry.jsonl` (7218 lines) is the dispatcher heartbeat
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


## VDP disclosure packages (sibling format)

`vdp-disclosures/<slug>/` is a distinct, lighter contract: `ROUTE.md` (channel
+ attribution decree — observed: free + fully attributed via the vendor's
security.txt Contact route, e.g. an H1 `embedded_submissions` URL), a
`cover-note.md`, the same-craft `report.md` ("Disclosed freely by", pinned
commit/file/sha256, CWE, CVSS, verbatim scope excerpt), and `SUBMITTED.md`
(timestamp + verbatim platform confirmation). Operator personally sends; the
fleet stages, never sends. Parked VDP-adjacent programs show up as two-file
honest-zero claims (`report.md` + `status.json`, e.g.
`claims/hackerone-ruby/honest-zero-vdp-no-payout/`). Details:
`corpus/knowledge/vdp-disclosure-packages.md`.

## Evidence-package anatomy

`claims/<program>/<slug>/` — six files, per `fleets/mission-template.md` and
verified in `claims/cantina-pendle/ingestion-20260915/`:

| File | Contract |
|---|---|
| `report.md` | title; program + official URL; verbatim "Scope excerpt" + URL + observed_at + sha256; vuln class; repro steps (no secrets); impact tied to the policy's severity/reward language; affected asset; suggested fix; disclosure timeline; explicit "No submission performed" |
| `claim_checklist.md` | exact per-program submission steps; portal quirks; marked OPERATOR-GATED; names residual gates (fees, VM captures) |
| `evidence/manifest.json` | `evidence-manifest/v1`: sha256 per artifact, `polarity` (≥1 positive), `redactions[]` — same-digest receipt per artifact with distinct producer/verifier; `redactions:[]` is never claim-ready |
| `custodian-receipts.json` | decision chain {action, input_sha256, decision_sha256, matched_grant_id, scope_signal}; every action needs nonempty grant + `scope_signal:"NO_SCOPE_OBJECTION"` exactly; `head_sha256` == manifest `expected_head_sha256` |
| `provenance.json` | agents + requested/resolved models per transition, commands + exit codes, commit pin, policy_sha256, `external_effects_performed: []`, secrets sweep attestation |
| `status.json` | state machine; `manifest_sha256` binds status to manifest bytes; `claim_review` block with hard_gates + subchecks |

`status.json` field semantics (from real packages):
`claimable` — the operator-queue bit. `do_not_submit` / `no_submission_performed`
— belt+braces on the external-effect gate. `claim_review.hard_gates` —
`written_scope`, `authorization`, `evidence_integrity`,
`no_duplicate_or_prior_submission`. `claim_review.subchecks` — `no_secrets`,
`operator_attribution`. Reviewer must be distinct from producer, with
requested/resolved model + fallback recorded. Any failed/unknown gate →
`state:"BLOCKED"`, `claimable:false`, never a silent downgrade to "DONE-ish".

## Disclosure anti-patterns (all observed in fleet wrap review)

From `docs/wrap-report.md` — 7 canonical packages, 0 clean GO; every fix is a
disclosure defect, not a code defect:

1. **Internal verdict strings as portal severity** — payloads carried
   `positive_finding` / `positive` instead of the platform's severity language
   (H1 `High` + CVSS, Intigriti `Unscored` when the program self-assigns).
2. **Severity hedging below evidence, and inflation above it** — decree
   2026-09-05: claim at full supported strength; strip "Low-to-Medium ceiling"
   phrasing where Medium is proven; keep descoped language where precondition
   isn't proven (Intel: direct OOB write only, no code-exec claim).
3. **Absolute statements falsified by the package's own provenance** — Mozilla
   report said "no live host was contacted" while provenance recorded earlier
   GET/HEAD recon; corrected to "no live host contacted *to verify this
   finding*".
4. **Internal orchestration artifacts in attachments** — authorization/scope
   records, duplicate checklists, internal tags submitted alongside the report.
   Attach only triage-useful proof (Airtable: `poc.js`, `poc-output.json`,
   `proof.json` — nothing else).
5. **Stale `claim-ready/*` tag treated as current authority** — a historical
   tag never overrides current bytes; `claim-check.mjs` re-validates what is on
   disk. Several tags excluded from the queue for exactly this.
6. **Overclaiming the negative** — an empty `in_scope_assets` means "not
   observed in this response", never "the program has no scope"
   (`claims/bugcrowd-seek/honest-zero/submit/BLOCKED.md`).
7. **Claiming safe harbor the program doesn't grant** — SEAL Whitehat covers
   active exploits only; routine findings get no safe-harbor credit (Cantina).
8. **Manufactured findings** — I8: honest-zero is a first-class deliverable.
   438/486 non-claim-ready missions terminate as LEARNED honest-zero.
9. **Precondition laundering** — a local PoC proves the defect, not live
   impact. Package stays BLOCKED until the named precondition check runs
   (Pendle resident-balance check; 3CX uid=0 capture; WordPress pinned-checkout
   rerun).
10. **Treating "DONE" as claimable** — `DONE` alone is insufficient:
    claimable requires `claimable:true`, positive `finding_count`,
    status↔manifest digest, custodian head binding, redaction receipts,
    reviewer distinctness, secret + attribution subchecks
    (`docs/claim-runbook.md` §A.2).

## Triage economics

`ops/ev-report.mjs` computes the hunter-contract EV per program record
(`bounty-map/programs/<id>.json` → `ev_inputs`):

```
p_success    = p_in_scope × p_reproducible × p_unique × p_accepted
gross_value  = p_success × expected_reward
total_cost   = effort_hours × opportunity_rate + direct_cost + delay_cost
               + expected_risk_cost
adjusted_ev  = gross_value − total_cost
```

Missing inputs print `UNKNOWN`, never default to 0/1; verdict degrades to
`unknown` — fail-closed like everything else. `docs/claim-runbook.md` is the
operator-side contract for what only a human may do (vault unlock, MFA, KYC,
the Submit click, payout rails).

## Cited paths (all verified 2026-09-28)

- `~/Projects/bounties/fleets/mission-template.md` — L1 mission contract, six-file deliverable spec
- `~/Projects/bounties/docs/claim-runbook.md` — preflight + operator-only actions
- `~/Projects/bounties/docs/claim-ready-index.md` — generated operator queue + blocked-package table
- `~/Projects/bounties/docs/continuation-notes.md` — 486-mission class partition
- `~/Projects/bounties/docs/wrap-report.md` — GO/GO-WITH-FIX/NO-GO review evidence
- `~/Projects/bounties/docs/review-verdicts.jsonl` — drop/continue/leave ledger
- `~/Projects/bounties/docs/autopsies/` — 30 structural-failure writeups
- `~/Projects/bounties/ops/{claim-check,claim-index,prepare-claims,ev-report}.mjs` — fail-closed gates
- `~/Projects/bounties/claims/cantina-pendle/ingestion-20260915/` — complete positive-blocked exemplar
- `~/Projects/bounties/claims/bugcrowd-seek/honest-zero/` — complete honest-zero exemplar
- `~/Projects/bounties/bounty-map/schema.json` — program record schema (draft-07, fail-closed `additionalProperties:false`)
