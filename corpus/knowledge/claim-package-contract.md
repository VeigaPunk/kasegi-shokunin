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
`~/Projects/the-bounty-hunter/ops/claim-check.mjs` never reads the manifest `schema_version`, the provenance
`pin`/`policy_sha256`/`external_effects_performed`, `status.severity`, or
`status.reward` — the tokens do not occur in the file (the entire provenance
gate is the :96-97 non-emptiness check). Those fields are
contract-by-convention (reviewer/runbook-checked), not machine gates. The
report.md "no submission" gate is a PROSE regex
(`/no submission (performed|made)/i`, :29), distinct from the JSON
`no_submission_performed` field. Canonical derivation:
`corpus/knowledge/triage-thresholds.md` §4.

## status.json semantics (observed values)

- `state`: `DONE` | `BLOCKED` | `SUBMITTED` | `PARKED` — round-14
  correction: PARKED was missing from this enum but is 248/280 = 88.6% of
  packages (`corpus/knowledge/claim-anatomy-sample.md` D11). `DONE` requires reviewer
  `APPROVED` with `claim_ready:true`; producer never self-approves.
- `verdict`: free-form but observed patterns: `positive`,
  `positive-blocked-<precondition>`, `honest-zero-<reason>`. Round-14
  census: 249 distinct values / 280 packages (88.9% singletons);
  `honest-zero-*` = 256 incl. two undocumented dominant suffixes
  `-identity` (121) and `-host-binding` (69); `positive-blocked-*` = 2;
  4 verdicts are full prose sentences
  (`[lost-tree] claims/bugcrowd-auth0-okta/ingestion-20260914/status.json:3`).
- `claimable`: bool — the queue bit for `docs/claim-ready-index.md`.
  Round-14 census: absent in 241/280 (exactly the b1k-* keeper cohort,
  232/233); `claimable:true` only 12/280 (`corpus/knowledge/claim-anatomy-sample.md` D1).
- `finding_count`: positive integer when claimable.
- `do_not_submit` / `no_submission_performed`: redundant external-effect guards.
- `claimability_blocker` + `resume_condition`: what reopens a BLOCKED
  package. Round-14 note: in the sampled BLOCKED packages
  `claimability_blocker` occurs 0×; hyatt uses `blocked_reason`
  (`[lost-tree] claims/hackerone-hyatt/ingestion-20260914/status.json:14`) — blocker
  naming drifts (`corpus/knowledge/claim-anatomy-sample.md` D9).
- `claim_review.hard_gates`: `written_scope`, `authorization`,
  `evidence_integrity`, `no_duplicate_or_prior_submission`.
- `claim_review.subchecks`: `no_secrets`, `operator_attribution`.

## Validation

`node ops/claim-check.mjs claims/<program>/<slug>` — fail-closed. `DONE` alone
is insufficient: needs `claimable:true`, positive `finding_count`, artifact,
status↔manifest digest match, manifest↔custodian-head binding, redaction
receipts, reviewer distinctness, secret + attribution subchecks
(`docs/claim-runbook.md` §A.2).

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/fleets/mission-template.md, deliverable contract section; verified against claims/cantina-pendle/ingestion-20260915/ and claims/bugcrowd-seek/honest-zero/.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md
restoration-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15

## Re-ground (round 46)

The current claims of this entry are exactly rows G1-G21 below; each one is re-located every time its recheck line runs, by `corpus/instruments/r46-c1-gate.py`, in the committed bytes named in its anchor (`corpus/instruments/claim-package-check.py` or a fixture under `corpus/instruments/fixtures/claim-package/`). Every other line of this entry (the source header, the round-13 boundary note, the status.json census and its state/verdict/claimable semantics, the lost-checker validation command and the provenance block) is a recorded observation of a lost tree ([lost-tree] `~/Projects/bounties`, and [lost-base] where a base export is cited), no longer re-verifiable, and never to be read as a current claim. Left historical and not re-grounded: the boundary note's statements about which fields the lost `ops/claim-check.mjs` reads (lines 18-27, including the prose regex at line 26), the DONE/APPROVED and claimable requirements and the status census (lines 29-54), the lost checker's validation command (lines 56-62), and the `OPERATOR-GATED` checklist marker (line 12), which no committed gate checks.

| id | current claim | committed anchor | token |
| --- | --- | --- | --- |
| G1 | Entry l.7 and table l.11-16: a claim-ready package contains the six files `report.md`, `claim_checklist.md`, `evidence/manifest.json`, `custodian-receipts.json`, `provenance.json`, `status.json` | `corpus/instruments/claim-package-check.py:101-108` | `'report.md', 'claim_checklist.md', 'evidence/manifest.json', 'custodian-receipts.json', 'provenance.json', 'status.json'` |
| G2 | Entry l.13: `schema_version: "evidence-manifest/v1"` is the manifest schema the gate requires | `corpus/instruments/claim-package-check.py:305` | `manifest.get('schema_version') != 'evidence-manifest/v1'` |
| G3 | Entry l.13: each artifact `polarity` is in {positive, negative} | `corpus/instruments/claim-package-check.py:334` | `elif artifact.get('polarity') != 'negative':` |
| G4 | Entry l.13: at least one artifact is positive (>=1 positive required) | `corpus/instruments/claim-package-check.py:354` | `if positive < 1:` |
| G5 | Entry l.13: `redactions[]` receipts carry nonempty producer and verifier identities that are distinct | `corpus/instruments/claim-package-check.py:413-415` | `producer.strip().casefold() == verifier.strip().casefold()` |
| G6 | Entry l.13: each receipt's `artifact_sha256` and `scanned_artifact_sha256` equal the manifest digest of its artifact | `corpus/instruments/claim-package-check.py:407-409` | `first.lower() == second.lower() == recorded.lower()` |
| G7 | Entry l.14: every custodian action carries `scope_signal` exactly `"NO_SCOPE_OBJECTION"` | `corpus/instruments/claim-package-check.py:460` | `decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'` |
| G8 | Entry l.14: every custodian action carries a nonempty `matched_grant_id` | `corpus/instruments/claim-package-check.py:457-458` | `grant = decision.get('matched_grant_id')` |
| G9 | Entry l.14: `head_sha256` equals the final decision digest | `corpus/instruments/claim-package-check.py:467` | `head.lower() != final_digest.lower()` |
| G10 | Entry l.14: `head_sha256` equals `manifest.expected_head_sha256` | `corpus/instruments/claim-package-check.py:471` | `if head.lower() != head_expected.lower():` |
| G11 | Entry l.15: agents carry requested and resolved models per transition | `corpus/instruments/claim-package-check.py:497` | `for key in ('transition', 'requested_model', 'resolved_model'):` |
| G12 | Entry l.15: a `pin` object is present in provenance.json (presence only; the gate also needs a nonempty remote and a 7-64-hex commit, lines 518-523) | `corpus/instruments/claim-package-check.py:515-516` | `pin = document.get('pin')` |
| G13 | Entry l.15: `policy_sha256` is read from provenance.json and must be 64-hex (line 525) | `corpus/instruments/claim-package-check.py:524-525` | `policy = document.get('policy_sha256')` |
| G14 | Entry l.15: `external_effects_performed` is `[]`; any entry fails | `corpus/instruments/claim-package-check.py:527-528` | `if not isinstance(effects, list) or effects:` |
| G15 | Entry l.16: `manifest_sha256` in status.json binds status to the manifest bytes | `corpus/instruments/claim-package-check.py:585-588` | `actual = hashlib.sha256(manifest_bytes).hexdigest()` |
| G16 | Entry l.16: the `claim_review` reviewer has a distinct identity; the gate checks it only against the manifest's producer and verifier names, case-insensitively | `corpus/instruments/claim-package-check.py:607` | `if identity.strip().casefold() in _identities(manifest):` |
| G17 | Entry l.11: report.md carries the literal marker "No submission performed" | `corpus/instruments/claim-package-check.py:636-637` | `if NO_SUBMISSION not in text:` |
| G18 | Entry l.11: report.md carries a "Scope excerpt" heading (case-insensitive); the gate does not check the excerpt's composition | `corpus/instruments/claim-package-check.py:634-635` | `if not SCOPE_EXCERPT.search(text):` |
| G19 | Entry l.13 (conforming instance): the exemplar manifest carries `schema_version` `evidence-manifest/v1` | `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | `"schema_version": "evidence-manifest/v1"` |
| G20 | Entry l.15 (conforming instance): the exemplar provenance has `external_effects_performed` set to an empty list | `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` | `"external_effects_performed": [],` |
| G21 | Entry l.11 (conforming instance): the exemplar report carries the literal marker "No submission performed." | `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` | `No submission performed.` |
