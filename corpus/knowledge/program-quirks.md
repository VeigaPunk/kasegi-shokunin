# Program quirks observed

Source: `~/Projects/bounties/claims/cantina-pendle/ingestion-20260915/`,
`docs/claim-ready-index.md`, `docs/claim-runbook.md`, autopsies. Read
2026-09-28. Quirks belong in each package's `claim_checklist.md`; this file
lists patterns to check for.

## Cantina (pendle exemplar)

- **$100 submission deposit** — the claimability gate is a read-only
  live-balance check before paying; submitting on dust buys a likely-
  informational verdict. Checklist §1 makes the operator run it.
- **Vulnerable-pattern OOS** — findings valid only with executable impact on a
  live market; malicious-trusted-role preconditions OOS. Frame as
  permissionless, not hypothetical.
- **AI-assist disclosure required** — include it.
- **SEAL Whitehat Safe Harbor = active exploits only** — no safe-harbor credit
  for routine findings.
- `kycRequired: false` at submission.
- Scope attribution trick: in-scope contract addresses enumerated in
  `deployments/<chain>-core.json` keys (`pendleSwap`, router facets); whitelist
  membership dynamic → source-review-only under no-chain-contact boundary.

## HackerOne

- Portal fields are React-controlled: native value setter + input/change
  events; attachments via dropzone's hidden `input[type=file]`
  (`fleets/claimer-mission.md`).
- Submit route `/<program>/reports/new`; severity = portal language (High +
  CVSS vector), not internal verdict strings.
- Attribution: operator identity `vgpnk1337`; payout needs payout method + tax
  form before first claim.
- GraphQL `team(handle)` gives policy/scope unauthenticated.

## Intigriti

- Operator identity `veigapunk`; KYC for payouts.
- Some programs self-assign severity (Intel: `Unscored — Intel assigns CVSS
  v4.0`) — do not submit an internal score.

## Bugcrowd

- Researcher identity `@bugcrowdninja.com` required by some programs (SEEK) —
  unprovisioned credential → `credentialed testing` not granted.
- Some programs forbid all automated tooling explicitly (SEEK prohibition
  verbatim).
- AI-content rejection clauses exist verbatim (SEEK: "low-effort or
  AI-generated content … will be rejected").
