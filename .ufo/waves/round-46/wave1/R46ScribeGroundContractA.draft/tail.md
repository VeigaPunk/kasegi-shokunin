
## Re-ground (round 46)

The rows below are this entry's only CURRENT claims: each names a committed instrument (the round-43 gate `corpus/instruments/claim-package-check.py`, or an exemplar file under `corpus/instruments/fixtures/claim-package/exemplar/`) that still carries the rule quoted, and a row counts only when its token is in those committed lines. Every other line of this entry, including the round-13 boundary note on the lost `ops/claim-check.mjs` (l.19-27), the status census values (l.31-51), the Validation command (l.58-62) and the Provenance block (l.64-67), is a recorded observation of a lost tree ([lost-tree]/[lost-base]), no longer re-verifiable, and must never be read as a current claim. Left historical and not re-grounded: the lost checker's parity and its prose "no submission" regex (l.19-27); the `state`, `verdict`, `claimable`-census and `claimability_blocker` census lines (l.31-51); the requirement that the scope excerpt be verbatim policy text with observed_at (l.11, where the gate checks only the heading, the https URL, the literal marker and the cited digests); and `redactions:[]` being "never claim-ready" beyond the gate's refusal (G6 covers the refusal only).

| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | l.7 and table l.9-16: a claim-ready package "contains" report.md, claim_checklist.md, evidence/manifest.json, custodian-receipts.json, provenance.json, status.json; the gate's SIX_FILES tuple names all six | `corpus/instruments/claim-package-check.py:101-108` | `'custodian-receipts.json',` |
| G2 | l.13: `schema_version: "evidence-manifest/v1"`; the gate's R-MANIFEST refuses any other schema_version | `corpus/instruments/claim-package-check.py:305` | `!= 'evidence-manifest/v1'` |
| G3 | l.13: `polarity` is in {positive, negative}; any other polarity is refused | `corpus/instruments/claim-package-check.py:332-335` | `elif artifact.get('polarity') != 'negative':` |
| G4 | l.13: "≥1 positive required" | `corpus/instruments/claim-package-check.py:354-355` | `if positive < 1:` |
| G5 | l.13: `redactions[]`: "one same-digest receipt per artifact with nonempty, distinct producer/verifier identities" | `corpus/instruments/claim-package-check.py:413-415` | `producer.strip().casefold() == verifier.strip().casefold()` |
| G6 | l.13: "`redactions:[]` is never claim-ready" — committed half only: R-REDACT refuses an empty list; a WELL-FORMED verdict is not claim-readiness | `corpus/instruments/claim-package-check.py:366-367` | `raise _GateFail('redactions=empty')` |
| G7 | l.13: "Artifact paths are relative to `evidence/`" | `corpus/instruments/claim-package-check.py:336` | `inspect_path(pkg.root, 'evidence/' + rel)` |
| G8 | l.13: "no symlink traversal" — each path component is lstat-checked and a symlink is refused | `corpus/instruments/claim-package-check.py:181-182` | `return None, 'symlink'` |
| G9 | l.14: "Every action: nonempty `matched_grant_id` AND `scope_signal` exactly \"NO_SCOPE_OBJECTION\"" | `corpus/instruments/claim-package-check.py:457-461` | `decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'` |
| G10 | l.14: "`head_sha256` == final decision digest == `manifest.expected_head_sha256`" — the head-to-manifest leg | `corpus/instruments/claim-package-check.py:469-472` | `if head.lower() != head_expected.lower():` |
| G11 | l.15: "`external_effects_performed: []`" | `corpus/instruments/claim-package-check.py:527-529` | `effects = document.get('external_effects_performed')` |
| G12 | l.15: "`external_effects_performed: []`" — exemplar instance | `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` | `"external_effects_performed": []` |
| G13 | l.16: "`manifest_sha256` binds status to manifest bytes" | `corpus/instruments/claim-package-check.py:585-589` | `if recorded.lower() != actual:` |
| G14 | l.16: "`claim_review` holds ... `reviewer` (distinct identity ...)" — the reviewer identity must differ from every manifest producer and verifier | `corpus/instruments/claim-package-check.py:607-608` | `if identity.strip().casefold() in _identities(manifest):` |
| G15 | l.52: "`claim_review.hard_gates`: `written_scope`, `authorization`, `evidence_integrity`, `no_duplicate_or_prior_submission`" | `corpus/instruments/claim-package-check.py:123-128` | `'no_duplicate_or_prior_submission',` |
| G16 | l.54: "`claim_review.subchecks`: `no_secrets`, `operator_attribution`" | `corpus/instruments/claim-package-check.py:129` | `SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')` |
| G17 | l.42: "`claimable`: bool" | `corpus/instruments/claim-package-check.py:609-611` | `if not isinstance(claimable, bool):` |
| G18 | l.45: "`finding_count`: positive integer when claimable" | `corpus/instruments/claim-package-check.py:617-619` | `not isinstance(count, int) or count < 1:` |
| G19 | l.11: literal marker "No submission performed" | `corpus/instruments/claim-package-check.py:121` | `NO_SUBMISSION = 'No submission performed'` |
| G20 | l.11: literal marker "No submission performed" — exemplar instance | `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` | `No submission performed.` |
| G21 | l.13: `schema_version: "evidence-manifest/v1"` — exemplar instance | `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` | `"schema_version": "evidence-manifest/v1"` |
| G22 | l.16: `manifest_sha256` binds status to manifest bytes — exemplar instance, the digest equals the exemplar manifest's bytes | `corpus/instruments/fixtures/claim-package/exemplar/status.json:3` | `"manifest_sha256": "5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834"` |
