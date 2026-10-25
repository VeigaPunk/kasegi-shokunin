# Program quirks observed

Source: `[lost-tree] claims/cantina-pendle/ingestion-20260915/`,
`docs/claim-ready-index.md`, `docs/claim-runbook.md`, autopsies, Cantina
sibling status.json files. Read 2026-09-28. Quirks belong in each package's
`claim_checklist.md`; this file lists patterns to check for.

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

### Cantina siblings sampled round 3 (ingestion-20260914/15)

- `cantina-dydx`: BLOCKED `positive-blocked-live-precondition` — same
  live-precondition pattern as Pendle; reward table critical max $1M.
- `cantina-morpho`: BLOCKED `honest-zero-no-claimable-finding`
  (totalRewardPot $2.5M headline; WebApps crit max $200k).
- `cantina-euler`, `cantina-uniswap`, `cantina-reserve-protocol`: PARKED
  `honest-zero-local-source-review` — local source review bounded out.
- Takeaway: on Cantina, ingestion-seeded packages resolve either to
  positive-blocked-on-live-precondition or honest-zero; the $100 fee gate is
  Pendle-specific so far — do not assume every Cantina program charges.
  Reward ladders vary per program ($1M–$15.5M crit ceilings).

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

## Provenance (round-22 correction, appended)

source: [lost-tree] claims/cantina-pendle/ingestion-20260915/, docs/claim-ready-index.md, docs/claim-runbook.md, docs/autopsies/, and sibling status.json files.
verified-at: 2026-09-28
recheck: on-restoration — test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/program-quirks.md (fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15)
