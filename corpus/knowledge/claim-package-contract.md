# Claim-package contract (six files)

Source: `~/Projects/bounties/fleets/mission-template.md` (deliverable contract
section) verified against `claims/cantina-pendle/ingestion-20260915/` and
`claims/bugcrowd-seek/honest-zero/`. Read 2026-09-28.

A claim-ready package lives at `claims/<program>/<slug>/` and contains:

| File | Binding rules |
|---|---|
| `report.md` | Title; program + official URL; "Scope excerpt" = verbatim policy text + URL + observed_at + content sha256; vuln class; repro steps without secrets; impact tied to the policy's own severity/reward language; affected asset; suggested fix; disclosure timeline; literal marker "No submission performed". |
| `claim_checklist.md` | Per-program submission steps (portal route, fields, quirks); carries "OPERATOR-GATED"; names residual gates. |
| `evidence/manifest.json` | `schema_version: "evidence-manifest/v1"`. Per-artifact sha256 + `polarity` ∈ {positive, negative}; ≥1 positive required. `redactions[]`: one same-digest receipt per artifact with nonempty, distinct producer/verifier identities. `redactions:[]` is never claim-ready. Artifact paths are relative to `evidence/`, must stay inside the package, no symlink traversal. |
| `custodian-receipts.json` | Non-empty decision chain `{action, input_sha256, decision_sha256, matched_grant_id, scope_signal}`. Every action: nonempty `matched_grant_id` AND `scope_signal` exactly `"NO_SCOPE_OBJECTION"`. `head_sha256` == final decision digest == `manifest.expected_head_sha256`. |
| `provenance.json` | Agents + requested/resolved models per transition, commands + exit codes, pin (remote + commit), `policy_sha256`, `external_effects_performed: []`, secrets attestation. |
| `status.json` | `manifest_sha256` binds status to manifest bytes. `claim_review` holds `hard_gates` + `subchecks` + `reviewer` (distinct identity, requested/resolved model, fallback flag). |

Round-13 boundary note — not every row above is gate-enforced:
`claim-check.mjs` never reads the manifest `schema_version`, the provenance
`pin`/`policy_sha256`/`external_effects_performed`, `status.severity`, or
`status.reward` — the tokens do not occur in the file (the entire provenance
gate is the :96-97 non-emptiness check). Those fields are
contract-by-convention (reviewer/runbook-checked), not machine gates. The
report.md "no submission" gate is a PROSE regex
(`/no submission (performed|made)/i`, :29), distinct from the JSON
`no_submission_performed` field. Canonical derivation:
`triage-thresholds.md` §4.

## status.json semantics (observed values)

- `state`: `DONE` | `BLOCKED` | `SUBMITTED`. `DONE` requires reviewer `APPROVED`
  with `claim_ready:true`; producer never self-approves.
- `verdict`: free-form but observed patterns: `positive`,
  `positive-blocked-<precondition>`, `honest-zero-<reason>`.
- `claimable`: bool — the queue bit for `docs/claim-ready-index.md`.
- `finding_count`: positive integer when claimable.
- `do_not_submit` / `no_submission_performed`: redundant external-effect guards.
- `claimability_blocker` + `resume_condition`: what reopens a BLOCKED package.
- `claim_review.hard_gates`: `written_scope`, `authorization`,
  `evidence_integrity`, `no_duplicate_or_prior_submission`.
- `claim_review.subchecks`: `no_secrets`, `operator_attribution`.

## Validation

`node ops/claim-check.mjs claims/<program>/<slug>` — fail-closed. `DONE` alone
is insufficient: needs `claimable:true`, positive `finding_count`, artifact,
status↔manifest digest match, manifest↔custodian-head binding, redaction
receipts, reviewer distinctness, secret + attribution subchecks
(`docs/claim-runbook.md` §A.2).
