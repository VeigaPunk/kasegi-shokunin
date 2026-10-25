# ufo-archive-2026 — pre-consolidation claim-hardening wave

Source: `[lost-tree] fleets/ufo-archive-2026/` (frozen 2026-09-17;
read in full 2026-09-28). A snapshot of the 2026-09-06→14 bounty fleet *before*
the current `fleets/missions|run|leases` layout: 20 `claim-*` L1 hardening
missions over real `claims/` packages, plus the keeper/whipper substrate that
generated the `b1k-NNN` run_ids still referenced by `ledger/candidates.jsonl`.

## Layout

- `missions/claim-*/` — 20 hardening missions (round-13 correction: this
  line stayed at 19 after r12 fixed :5 — `ls -d claim-* | wc -l` = 20, 20
  `report.json`). Each has `report.json` (L1's
  structured self-report); richer ones keep the full multi-seat artifact set:
  `wwkd-plan-r1.md`, `planner-r1.md`, `scout-r1.md`, `security-audit-r1.md`,
  `reviewer-correctness-r1.md`, `claim-reviewer-r1.md`, `gatekeeper-r1.md`,
  `connector-r1.md`, `dedupe-r1.md`, `custodian-*-r1.json` — i.e. the
  planner→scout→sentinel→reviewer→gatekeeper→connector loop was executed and
  archived per package.
- `report.json` schema (varies per mission): `packages_assigned`, per-package
  `before`/`after`, `lane_topology`, `route_failures`+`reroutes` (lane-identity
  reroute telemetry), `staged_drafts` (artifact→sha256), `remaining_gaps`,
  `residual_uncertainty`, `dedupe_decisions`, `decision`, and
  `no_submission_performed`/`submission_performed` flags.
- `programs/<id>/` — earlier per-program evidence shape: `authority/
  operator-boundary.json`, `custodian/input-NNN.json`, `scope/` +
  `scope-snapshots/` or `captures/` (nextcloud), `lanes/round0-*.json`,
  `state-ledger.jsonl`, `run-manifest.json` (sole-L1 model resolution,
  frozen axes).
- `bounty-keeper/` — `[lost-tree] fleets/ufo-archive-2026/bounty-keeper/keeper.mjs`: saturated a 16-pane wall, `LAUNCH_CAP 384`,
  12 h night budget, spawned `b1k-NNN` runs via `~/Projects/ufo-fsd-alpha/scripts/ufo-sighting.mjs` (recorded as `origin-work/ufo-fsd-alpha` at census time; the tree relocated to `~/Projects/ufo-fsd-alpha` 2026-10-12, file survives at HEAD `964f443e`). State:
  launched 265, halted `night_budget` 2026-09-11T09:37Z. **This is the
  producer of the `b1k-NNN` run_ids** in `ledger/candidates.jsonl` and
  `evidence/<program>/b1k-NNN/` dirs.
- `bounty-whipper{-state.json,.jsonl}` — hourly nudge tracker over
  bounty01..N missions: `lastActivityAtMs`/`lastObservedAtMs`/`terminalClaim`,
  openai_usage reset-credit polling.
- `inquiries/bounty-fleet-2026-09-06/` — 16 per-program L0 mission briefs: the
  original full-loop charter (DISCOVERED→…→LEARNED), hard-boundary text
  ("prepare — NEVER submit"), L2 lane mix with operator-dated route overrides
  (`@fleet_l2`→grok-4.5:low decree, kimi executor/connector seats,
  daybreak-blue claim-reviewer), sparks disabled.
- `sighting/handoffs/l1-*-r*.json` — schema-v1 resume handoffs
  (`continuity:"resumed-exact"`).
- `sessions/bountyA0912/` + `studies/` — the bountyA0912 read-only
  control-plane study (`bounty-visible-report.json`: explicit
  `non_execution` manifest — read files/jq only, nothing authorized).

## Naming drift

Archive paths `claim-packages/<slug>` (coinbase, metamask mm01, mongodb-mcp)
no longer exist — those packages were folded into `claims/<platform>-<program>/<slug>/`
(`claims/hackerone-coinbase`, `hackerone-metamask`, `hackerone-mongodb`
verified present 2026-09-28). Treat `claim-packages/*` references in archived
docs as the old tree name, not a parallel store.

## Reconciliation evidence chain (receipt drift → verified)

The `prior_submission_resolution` answer in `missions/claim-spotify-oauth/
report.json` names the chain to reuse when a package may already be filed:

1. `ledger/missions.jsonl` — SUBMITTED transition (fleet batch-record ts, not
   provider-issued).
2. `fleets/run/portal-reconciliation-2026-09-11.json` — authenticated portal
   read (`submission_verified:true`, `closed_duplicate`, `duplicate_of`).
3. `.ufo/claim-recovery/final-audit.json` — cites the reconciliation file.
4. `ledger/candidates.jsonl` + `.ufo/bounty-fleet/plan-round0.md` — "do not
   re-hunt" records.
5. git commit evidence.

## Hardening-wave outcome vocabulary

- `REFINED → DONE claim-ready` — gates pass on final bytes; submission stays
  operator-gated (intel, anthropic, wordpress).
- `HOLD` — package completes to a gate-consistent hold record with named
  blockers (claim-web3: hold-evidence-gap ×2; google-aiven
  `hold-prior-filing-conflict`; superhuman apikey scope questions).
- `NOT-SUBMITTABLE` — gamma-deposit: vuln proven by local-EVM PoC but it is a
  published audit finding AND the deployed in-scope asset was verified
  FIRST-HAND fixed (blockscout source fetch, sha256-cited). Proven vuln ≠
  claimable.
- `falsified-by-execution` — elastic EPR-STOR-1: re-opener test run through
  real `mux.NewRouter().StrictSlash(true)` confirmed falsification →
  submission-draft.md staged as *exclusion notice*, not a report.
- `reconcile-only` — airtable: H1 #4002789 verified prior submission of the
  same finding → `NOT_CLAIMABLE_AS_NEW`.
- `stop — frontier saturated` — web1/web3/3cx/8x8/spacex: every reachable
  in-package defect fixed; remainders are human gates or out-of-package writes.

## Observed defect taxonomy (what claim packages actually got wrong)

Ordered by recurrence across the 19 missions. This is the empirical superset
of `ops/claim-check.mjs` — the wave fixed what the gates catch *and* what they
don't.

**Gate-binding (checker-visible):**
1. `custodian-receipts.json` missing `head_sha256` (3cx, 8x8 — used
   `expected_head_sha256` as the receipt field name, github-nines bare
   array, anthropic, wordpress, doit-amp) — or bound the terminal
   `event_sha256` instead of the terminal `decision_sha256` (3cx).
2. `manifest.expected_head_sha256` bound to a stale pre-chain digest
   (8x8 `e593ff7d` vs chain `ba990856`; github-nines `57f02637`).
3. Manifest artifacts without same-digest redaction receipts
   (anthropic 9/…; wordpress 22/27 — 12 reusable receipts existed in
   `evidence/hackerone-wordpress/redaction-scan-authorization.json` but were
   never copied into `manifest.redactions`; intel 9).
4. Orphan receipts binding non-manifest digests — receipts for stale digests
   of package-root files (doit-amp ×5). Receipts must bind *current* manifest
   digests.
5. `status.json` defects: missing `claimable`/`finding_count`/`claim_review`
   (nearly every BLOCKED package); stale `manifest_sha256` after manifest
   repair (doit-amp); `pushed_ref` citing a withdrawn claim-ready tag
   (github-nines).
6. `submit-payload.json` drift: sha256 vs manifest mismatch (anthropic —
   file restaged, manifest stale), duplicate attachment + self-inclusion +
   absolute local paths (anthropic, spotify 31→32 errors), non-allowlisted
   attachments, broken payload binding (intel), malformed repro steps
   (superhuman step 2 missing extraction command, step 4 placeholder).
7. `submit/BLOCKED.md` present while state DONE (anthropic, wordpress, intel).

**Submission-draft staging (checker-invisible):**
8. `submission-draft.md` absent in-package — the dominant defect: nearly
   every `claim-ready` package (coinbase, elastic ×2, google-aiven ×4,
   metamask ×3, mongodb ×2, web1 ×4, web2 ×4, web3 ×3, 3cx, superhuman).
9. Stale `submission-review/packets/` administrative drafts contradicting
   in-package state (elastic: a `go.mod`-replace method that no longer
   exists; aiven stale+inconsistent; web1 buddypress *materially wrong* —
   concluded dev-trunk-only, omitting the vulnerable stable v1 endpoint).
   Fix: `DO-NOT-USE` banner on stale packets; the in-package draft is
   canonical.
10. Draft must carry verbatim scope excerpt + clone prerequisite + prior-art/
    dedupe disclosure + per-version behavior (mongodb PR-1525, coinbase
    clone pin, bughunters mandatory-disclosures list).

**Duplicate-submission hazard (checker catches some; global scan is the net):**
11. Package reading pre-submission while a receipt exists — web2
    k8s (H1 4028846), ld-node (Bugcrowd a169f309 Pending), web1 mattermost.
    Fix: `RECEIPT EXISTS — DO NOT RESUBMIT` banner + manifest-status note +
    reconcile every packet/admin file to submitted-state.
12. Program-id namespace collision in payload: `github-bounty` vs canonical
    `github-bug-bounty` (github-nines; found by connector lane — reason to
    keep cross-lane review).

**Narrative/evidence drift:**
13. Stale file:line citations — the single most common narrative defect
    (metamask :161→:162, elastic :604→:605 check + api.search.go range,
    aiven README.rst:706 misattribution + stale witnesses, web3 cite ranges
    narrower than function extents, superhuman steps, web1 READY.md
    systematically stale line numbers).
14. Claims marked "verified" but never executed (coinbase vectors 3-4 +
    path-form boundary); overclaims contradicted by the package's own
    evidence (spacex "both resolvers" — DoH only; "unlimited requests" —
    superhuman; "filed by Elastic" unevidenced; "documented multi-tenant
    isolation" — code-comment only; "no live host contacted" class).
15. Evidence age un-bound: no fresh re-verification artifact in the
    manifest/custodian chain (spacex one-shot window, superhuman,
    wordpress probes 9 days old — re-run and re-bind).
16. Missing prerequisites/caveats: clone prerequisite (metamask ×3,
    coinbase, web3 clone recipe), CVSS vector absent (web3 ×3), severity
    field missing → inherited junk verdict (superhuman `positive` as
    severity).
17. Mislabeled/mis-partitioned artifacts: `*.cname.cf.json` artifacts
    labeled negative despite positive CNAME answers (spacex ×3); absolute
    `/home/vgpnk` paths embedded in evidence.json + regenerated every run
    → custodian HARD_STOP (snapchat); regenerable self-signed `key.pem` +
    RUN_LOG absolute paths → exclude-from-attachments (web2).

**Alias/dedupe:**
18. Canonical/alias packages indistinguishable: alias had `claim-ready`
    status + no `alias_of` + own contradictory severity (coinbase-agentkit);
    alias self-nominated as survivor (metamask mm-sdk-channel-inject).
    Fix: `status:"claim-ready-alias"`, `claim.json alias_of`, alias draft =
    evidence-handoff stub, `DO-NOT-ATTACH` flag, self-nomination demoted.
19. Dedupe resolved by **public diff**: sensei 4.5.1→4.5.2 SVN diff showed
    reply-path-only fix → adjacent-sink/incomplete-fix, NOT a duplicate;
    unresolved conflicts must reconcile manifest (`claim-ready` →
    `hold-prior-filing-conflict` preserving `prior_status`).

**Verdict/manifest consistency:**
20. `UNRESOLVED CONFLICT` flagged in REPORT.md while manifest still said
    `claim-ready` (aiven) — the manifest is the gate-visible state; report
    and manifest must agree.
21. `queue.json`/`claims/*.json` hold_reason narrower than package state
    (web2 do-agent "eligibility unresolved" though exclusions resolved).
22. Status-vocabulary precision: `claim-ready` / `claim-ready-alias` /
    `hold-*` / `informational` are distinct enumerations, not prose.

## Multi-seat review value (observed)

Connector lane caught what single-L1 passes missed: the program-id namespace
collision (github-nines), the `pushed_ref`→withdrawn-tag cite, the
planner-vs-sentinel curl dispute resolved to the conditioned-accept path
(spacex). Gatekeeper independently re-verified 32/32 manifest digests +
same-digest receipts + producer≠verifier. Claim-reviewer replayed the PoC
live (31/31 PASS, drift = timestamp only). Per-package multi-seat artifacts
are preserved under `missions/claim-*/` — that is the review-evidence format
the current `ops/claim-check.mjs` `claim_review` block codifies.

## What this archive is NOT

Not live state: statuses, model routes, and mission files are the 2026-09-06
fleet, superseded by `fleets/missions|run|leases` + `ops/fleet-dispatch.mjs`.
Mine it for defect patterns and contract ancestors; do not cite it as
current authority.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/fleets/ufo-archive-2026/ snapshot, frozen 2026-09-17 and read in full 2026-09-28.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -e corpus/knowledge/ufo-archive-2026.md
