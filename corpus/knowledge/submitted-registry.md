# Submitted-state registry — the do-not-refile set

Read 2026-09-28 from `/home/vgpnk/Projects/bounties`; verified by the round-9
L2 wave. No consolidated do-not-submit list exists in `docs/`; submission
truth is scattered across `claims/*/*/status.json` (inconsistent field
spellings), `ledger/missions.jsonl`, `fleets/run/portal-reconciliation-
2026-09-11.json`, `.ufo/claim-recovery/final-audit.json`, `vdp-disclosures/`,
stale git tags, archive-era mission reports, the root snapshot zips — AND
the live sibling tree `~/Projects/origin-work/open-bug-bounties/
claim-packages/` (the true home of `submission-review/` receipts). This is
the merged table.

## Verified submissions (receipt-bound)

| Report | Program/pkg | Submitted | Outcome | Sources |
|---|---|---|---|---|
| H1 `4002776` | `claims/mozilla-security-bounties/lando-diff-warning-missing-authz` | 2026-09-06T00:24:57Z | `closed_duplicate` of 3721615 | `status.json` SUBMITTED; ledger SUBMITTED (claimer-l1); `submit/receipt.md`; portal-reconciliation; commit `9dc20e64` |
| H1 `4002810` | `claims/hackerone-spotify/exported-loginactivity-cross-app-oauth-relay` | 2026-09-06T00:55:38Z | `closed_duplicate` of 3892215 | `status.json` SUBMITTED; ledger; portal-reconciliation; `duplicate_of` fields; commit `b01f9de4` |
| H1 `4002789` | `claims/hackerone-airtable/airtable-js-record-id-path-traversal` | 2026-09-06T00:55:38Z | `not_established` — report + 3 attachments exist, no triage decision observed | `status.json` BLOCKED + `submission_state:"SUBMITTED"` + `submitted_url` + `submitted_at`; ledger; portal-reconciliation; commit `b01f9de4` |

## Archive-era submissions (receipts now live in the sibling tree)

**The receipt-bearing packages are not gone — they moved to the sibling
tree.** `~/Projects/origin-work/open-bug-bounties/claim-packages/` is a
LIVE, separate claim corpus (~26 package dirs incl. all six old slugs,
`CONNECTOR.md`, `_schema.json`, `submission-review/`). Its
`submission-review/submission-receipts.csv` (verified live):

```
canonical_id,company,platform,report_id,report_url,submitted_at,status
k8s-nodebound-token-impersonation → H1 4028846 submitted
ld-node-stream-tls-bypass → Bugcrowd a169f309-… Pending
mattermost-jira-oauth2-state-csrf → Bugcrowd e4f41218-… New (pending triage)
```

The same three appear in `fleets/ufo-archive-2026/missions/claim-web2/
{INDEX.md,report.json}` and inside `ALL-claim-ready-packages-2026-09-15.zip`
under `A-open-bug-bounties/<slug>/` (a copy of this tree). Verified: no
receipt ID appears anywhere under `bounties/claims/`. Do-not-refile rules
still apply — a re-hunt that reproduces these findings must not file a
second report. And the blind spot is bigger than VDP: **no bounties-repo
tool (`claim-check`, `claim-index`) reads `origin-work/` at all** — the
entire second claim corpus is outside every scan.

| Report | Program/pkg (old name) | Submitted | State |
|---|---|---|---|
| H1 `4028846` | kubernetes — `k8s-nodebound-token-impersonation` | 2026-09-14 | submitted; triage monitoring only |
| Bugcrowd `a169f309-1365-4bf1-b858-9d8452a22cb3` | launchdarkly — `ld-node-stream-tls-bypass` | 2026-09-14 | Pending |
| Bugcrowd `e4f41218-6036-4bcf-80f1-1e2b6bf86d4e` | mattermost — `mattermost-jira-oauth2-state-csrf` (owning mission: claim-web1) | 2026-09-14 | New/pending triage; receipt UUID matches a pre-existing draft ID — strongest corroboration among archive receipts |

Current `claims/` cousins carry zero receipt linkage:
`claims/hackerone-kubernetes/honest-zero-git-sync` (PARKED honest-zero),
`claims/bugcrowd-launchdarkly-mbb-og/ingestion-20260914` (ingestion stub),
`claims/bugcrowd-mattermost-mbb-public/ingestion-20260914` (stub, parked
auth-walled per `docs/continuation-notes.md`).

## Probable submissions (unverified — login-wall)

`claim-elastic` analysis (`report.json`): revenger+connector lean
REAL-SUBMISSION ~65–70% — paired mtimes with the attested 4028846 write
pattern, sequential same-session H1 ID block, no local receipt template.
Public check = login-wall 403 (existence unverifiable, not absence).
`submission-review/receipts/CONTRADICTION.md` (in the origin-work tree,
mission claim-elastic 2026-09-14) is the additive warning file: each orphan
receipt conflicts with admin records (`submission-receipts.csv` no row,
`queue.json` `submitted:false`, `claims/*.json` `submitted:false`,
`run.json` `external_submissions:0`) — while paired `attachment-manifest.json`
files self-contradictorily carry `uploaded:true` + `platform_report_id` —
each also names the pkg under `esapi-*`/`aiven-karapace-acl-prefix`.
Operator action pending: authenticated H1/Bugcrowd inbox check; if real,
reconcile and do NOT refile; if absent, mark receipts void. Receipts left
untouched — editing either direction fabricates submission state.

Secondary stores the table cross-checks against:
`fleets/run/_claimer.status.json` carries `submitted[3]` (the three H1 IDs)
+ `disclosed[1]` (anthropic VDP "confirmed received");
`.ufo/bounty-fleet/reports/claim-claim-*.md` (8 reconcile reports — lando
SUBMITTED-reconciled with `provider_receipt_verified` blocked by login);
`evidence/*/status.json` (275 files: DONE 21 / PARKED 254 — zero
submission-bearing rows, only gate fields).

| Report | Program | Note |
|---|---|---|
| H1 `4028904`, H1 `4028953` | elastic | sequential ID block with 4028846 |
| Bugcrowd `4ecbaf46-9548-4033-967c-e44df73dedde` | aiven — `aiven-karapace-acl-prefix` | orphan receipt; conflicts with admin records `submitted:false`; unresolved possible-duplicate (claim-google-aiven) |

## Free disclosures (VDP — no payout, but still a filing)

`vdp-disclosures/anthropic-plugin-dev-cmd-injection/SUBMITTED.md`:
2026-09-06T01:19:04Z via Anthropic VDP embedded form (security.txt contact →
H1 `embedded_submissions` route), attributed vgpnk1337@gmail.com. Free by
operator decree. `ledger/missions.jsonl` carries the matching
`DISCLOSED_FREE` row at the byte-identical timestamp.

## Live hazard — cross-tree double-filing gap (verified by live run)

**Queue row 4** (`claims/hackerone-anthropic/plugin-dev-test-hook-command-injection`,
state DONE, `claimable:true`, in `docs/claim-ready-index.md`) is the SAME
finding as the VDP: identical title, commit `d7dbd9a`, file
`test-hook.sh`, source sha256 `ded642e8…69393`, CWE-78 — and the claim
package contains zero references to `vdp`/`anthropic-plugin-dev-cmd-injection`
(no cross-reference exists in either direction). Filing it double-files the
operator's own free disclosure.

Root cause verified against source: `[lost-tree] ops/claim-check.mjs:174-199`
tests prior submission only via `submitted_url` / `submission_performed===true`
/ `submission_state`==`SUBMITTED` — round-15 anchor note: those lines are past
the EOF of the surviving mirror's 83-line `ops/claim-check.mjs`
(sha256 `93679ea1d29b`), which has no prior-submission, duplicate-scan or
nested-readiness gate at all (19 `err(` sites vs the live file's 48). The
behaviour described here is a lost-tree fact
(`corpus/knowledge/source-tree-loss-2026-09-28.md` §4.1), not a mirror one.
It tests prior submission only via `submitted_url` /
`submission_performed===true` / `submission_state`==`SUBMITTED`, and its
sibling-package scan enumerates only
`claims/*/*/status.json` (`claimRoot` = two levels up, same-slug-or-same-title
match, ≥16-char titles). `vdp-disclosures/` and archive receipts are outside
the tree. Runtime proof: `node ops/claim-check.mjs
claims/hackerone-anthropic/plugin-dev-test-hook-command-injection` → `OK`
despite the VDP receipt. `claim-index.mjs` builds the queue from the same
package set — no separate VDP/archive scan.

**The gap is wider than VDP:** the entire `origin-work/.../claim-packages/`
corpus (~26 packages, 6 receipt JSONs, `submission-receipts.csv`,
`queue.json`) is outside every bounties-repo scan — `claim-check`,
`claim-index`, and every status-glob see only `~/Projects/bounties/claims/`.
A re-staged finding from the origin-work tree collides with nothing the
checker reads.

Advisory upstream fix (bounties-repo owned, not kasegi): extend the
duplicate predicate to consume `vdp-disclosures/*/SUBMITTED.md` (receipt) +
sibling `report.md` (identity: commit+file+sha256+CWE, not title alone) and
an archive-receipt index; `claim-index.mjs` then inherits the exclusion via
claim-check. Add a regression case for this pair.

## Field-semantics traps (verified against `claim-check.mjs` source)

- `submitted_url` = the filed-report URL (`/reports/<id>`); `submission_url`
  / `submission_uri` / `submission_email` = the *destination endpoint*, not
  proof of filing (e.g. `https://hackerone.com/anthropic/reports/new`,
  `mailto:vulnerability-report@doit.com`).
- `submission_performed` = this runtime submitted (expect `false` always —
  no fleet submission exists). It is NOT the do-not-refile signal:
  airtable carries `submission_performed:false` AND a real `submitted_url`.
- Census (sentinel): `submission_performed===true` occurs **zero times**
  corpus-wide — that checker leg is vacuous today. Inverse polarity trap:
  mozilla carries `no_submission_performed:false` (filing WAS performed —
  double negative). A scanner keying either boolean alone misclassifies
  both directions. Other fields observed: `provider_receipt_verified`,
  `receipt_verification_state` (VERIFIED_CLOSED_DUPLICATE /
  VERIFIED_EXISTS_OUTCOME_NOT_ESTABLISHED / BLOCKED_LOGIN_REQUIRED),
  `submission_bundle`, `submission_channel`, `submission_access_checked_at`,
  nested `submission` object (intel), nested `claim_wave.*`/`claim_attempt.*`
  histories — none are read by claim-check's duplicate gate.
- Spelling inventory in `status.json`: `no_submission_performed`,
  `new_submission_performed_this_wave`, `submission_record_basis`,
  `do_not_submit`, `submission_state`, `submitted_url`, `submitted_at`,
  `canonical_submitted_url`, `canonical_submitted_at`, `duplicate_of`,
  `superseded_by`, `no_duplicate_or_prior_submission` (hard-gate name, 26
  packages). The trustworthy do-not-refile triple: `submitted_url` containing
  `/reports/` OR `submit/receipt.md` present OR `submission_state` SUBMITTED —
  always cross-checked against ledger SUBMITTED/DISCLOSED_FREE rows.
- `submission_state` values beyond SUBMITTED: `"DUPLICATE_OF_SUBMITTED"`
  (structured alias marker) and `STAGED` variants — `"STAGED — operator-gated
  (Gate 1.5 takeover proof recommended)"` on `bugcrowd-spacex-starlink/
  ingestion-20260914/status.json`, plain `STAGED` on intigriti-yahoo,
  `submit_state:"STAGED — operator-gated"` on 8x8/anthropic/airtable/crypto/
  superhuman. A staged payload is not a filing.
- Aliases ARE machine-readable when used: `claims/hackerone-mozilla/
  lando-diff-warning-missing-authz/status.json` carries `duplicate_of` →
  `claims/mozilla-security-bounties/lando-diff-warning-missing-authz/`,
  `submission_state:"DUPLICATE_OF_SUBMITTED"`, `canonical_submitted_*`,
  `do_not_submit:true`. `duplicate_of` has 3 sites; both H1-target sites
  record **3892215** (round-12 correction: 3721615 — mozilla's closed-dup
  target — appears only in `fleets/run/portal-reconciliation-2026-09-11.json`,
  never in a `duplicate_of` field); `superseded_by` appears once —
  amazonvrp `history.superseded_by` narrative (a precondition finding, NOT a
  submission alias). The anti-pattern table's `claim.json alias_of`
  convention is unused repo-wide (0 hits, any file) — alias truth lives in
  `status.json`.
- Git tags: 3 `claim-ready/*` (mozilla/spotify/airtable — all peel to
  pre-submission commit `b3b1b7e3`; every tagged path has later SUBMITTED
  commits) and 9 `claim-hold/*` (incl. anthropic; telemetry shows its
  `claim-ready` tag was pushed then superseded by `claim-hold` — yet the
  generated index still queues it as row 4). Tags are provenance, never
  authority: `claim-index.mjs` re-validates current bytes.

## Status-less claim dirs (15 of 295 — not real packages)

All invisible to the `status.json` scan (deliberate — nothing to gate).
Three sub-classes (L2-verified file census):

- `ingestion-seeded` stubs (13, all named `ingestion-20260914`): `INGESTION.md`
  + `claim.json` (`stage:"ingestion-seeded"`, `submit:false`, hypothesis
  backlog inside INGESTION.md) + optional `evidence/`. A real pre-contract
  stage from the hunt2-deferred seeding wave (2026-09-14/15). Two are not
  bare: `discord-bug-bounty` carries 8 recon artifacts under `evidence/`;
  `microsoft-bounty-family` carries `evidence/falsification-ledger.md`.
- `bugcrowd-stiltsoft/honest-zero`: `report.md` + `custodian-receipts.json` +
  empty `evidence/`,`submit/` — partial package, no status.
- `bugcrowd-t-mobile/honest-zero`: `BLOCKED.md` only (81 bytes).

Status histogram over the 280 real packages: PARKED 248, BLOCKED 15,
DONE 15, SUBMITTED 2 (= 280; round-12 correction: BLOCKED was 16 and a
5th "OPERATOR_GATED 1" component was double-counted — OPERATOR_GATED is
intel's *nested* `submission.state`, its top-level state is DONE).
(A 281st `status.json` exists at
`claims/bugcrowd-seek/honest-zero/evidence/status.json` — depth-4 evidence
copy, correctly outside the scan.)

## Dated operator-facing bundles (root, not live state — verified)

- `claim-ready-packages-2026-09-15.zip` — 468 files, 9.1 MB; numbered
  top-level package dirs (`00-submitted-poc-remediation/airtable-…`,
  `01-spacex-starlink-…` … `07-intel-…`) + CLAIM-READY-INDEX (round-13
  correction: the `B-bounty-fleet/` grouping is NOT in this zip — 0 hits;
  it exists only in the ALL-zip below, 469 members).
- `ALL-claim-ready-packages-2026-09-15.zip` — 831 files, 10.8 MB; adds
  `A-open-bug-bounties/<slug>/` package trees (this is where the archive-era
  receipt IDs also appear) + `00-MASTER-INDEX.md` + `00-CHATGPT-TASK.md`.
Both frozen ≤2026-09-15 09:45; the live tree contains files dated
2026-09-15 21:40–21:45 and 2026-09-16 09:32 absent from both zips, and the
zip layout exists nowhere in the working tree. Never treat as authority.
