# Claim-anatomy sample — round-14 sampling push (10 → 30 of 280 = 10.7%)

Source: 20 NEW full `claims/*/*/status.json` reads, 2026-09-28 (round 14),
chosen by a deterministic stratified rule. Selection script preserved at
`/tmp/kasegi-r14/select20.sh` (byte-identical across the scout's 3 re-runs;
L1 re-ran it: `universe=280 eligible=263 selected=20`, PARKED 16 / BLOCKED 2
/ DONE 2, SIG 4). Full working table + raw dump:
`/tmp/kasegi-r14/scout-anatomy-20.md`, `/tmp/kasegi-r14/raw20-dump.txt`
(588 lines, 20 files). Closes the "~3.6% sampled" Known-gap to 10.7%; the
full census stays a future coverage sub-axis candidate.

## Selection rule (reproducible)

- Universe: `find claims -mindepth 3 -maxdepth 3 -name status.json` = **280**
  (the 281st `status.json` is the depth-5 evidence copy
  `claims/bugcrowd-seek/honest-zero/evidence/status.json` — excluded by
  construction, matching `corpus/knowledge/submitted-registry.md:207-209`).
- Exclusion set: 17 already-deeply-read paths (SKILL/corpus exemplars: seek
  honest-zero, pendle, dydx, 3cx, anthropic plugin-dev, both mozilla lando
  packages, airtable ×2, spotify ×2, wordpress ×2, intel pqos, doit amp,
  github-bounty nines, 8x8 jibri) → **263 eligible**.
- Strata = disjoint state × submission-signal cells (SIG =
  `submitted_url|submission_url|claim_url` non-null or
  `submission_performed==true`): s0 SUBMITTED n=0 q=0 (both SUBMITTED
  packages sit in the exclusion set — SUBMITTED-adjacency taken from SIG
  instead); s1 BLOCKED n=10 q=2; s2 DONE n=8 (all SIG) q=2; s3 PARKED-SIG
  n=5 q=2; s4 PARKED-PLAIN n=240 q=14. Within stratum: `LC_ALL=C` sort +
  evenly-spaced indices `idx=floor(i*L/n)+1`.
- DONE/BLOCKED deliberately over-sampled (2× proportional): they are the
  only states carrying `claim_review` blocks and submission URLs — highest
  schema-deviation information per read. PARKED stays the majority (16/20).

## The 20 packages (each read `path:1-N`, N = line count)

| # | path (`claims/…`) | N | state | verdict (abbrev.) | run/class | deviations |
|---|---|---|---|---|---|---|
| 1 | `bugcrowd-auth0-okta/ingestion-20260914` | 77 | PARKED | prose sentence | — | D9, D10 |
| 2 | `bugcrowd-northwestern-mutual-mbb-og/honest-zero` | 16 | PARKED | `honest-zero-participation-gated` | — | D4, D6, D7, D9 |
| 3 | `bugcrowd-opus-guard-market/honest-zero` | 59 | BLOCKED | `honest-zero-scope-unverifiable` | — | D4 (polarity) |
| 4 | `bugcrowd-spacex-starlink/ingestion-20260914` | 40 | DONE | `positive` | — | D12 |
| 5 | `cantina-reserve-protocol/ingestion-20260914` | 50 | PARKED | `honest-zero-local-source-review` | — | D2, D9 |
| 6 | `hackenproof-adi-foundation-zkvm-verification/honest-zero-adi-stack-contracts-state-transition` | 16 | PARKED | `…-state-transition` | b1k-131 | D1 |
| 7 | `hackenproof-enkrypt-wallet/honest-zero-enkrypt-local` | 15 | PARKED | `…-local-host-binding` | b1k-085 | D1 |
| 8 | `hackenproof-near-smart-contracts-1/honest-zero-lockup` | 16 | PARKED | `…-lockup-host-binding` | b1k-102 | D1 |
| 9 | `hackerone-automattic/honest-zero-jetpack` | 15 | PARKED | `…-jetpack-host-binding` | b1k-050 | D1, D5 |
| 10 | `hackerone-github/honest-zero-github-cli` | 15 | PARKED | `…-github-cli-host-binding` | b1k-058 | D1, D5 |
| 11 | `hackerone-hyatt/ingestion-20260914` | 66 | BLOCKED | `honest-zero-no-claimable-finding` | — | D3, D5 (null), D6, D7, D8 |
| 12 | `hackerone-notion/honest-zero-sdk-js` | 16 | PARKED | `…-sdk-js-host-binding` | b1k-056 | D1 |
| 13 | `hackerone-vercel-open-source/honest-zero-flags` | 15 | PARKED | `…-flags-discovery-and-override` | b1k-005 | D1, D5 |
| 14 | `hackerone-x/ingestion-20260914` | 40 | DONE | `positive` | — | D12 |
| 15 | `immunefi-balancer/honest-zero-vault-identity` | 15 | PARKED | `…-vault-identity` | b1k-146 | D1 |
| 16 | `immunefi-etherfi/honest-zero-liquidity-pool` | 16 | PARKED | `…-liquidity-pool-identity` | b1k-144 | D1 |
| 17 | `immunefi-kast/honest-zero-solana-m-extensions` | 15 | PARKED | `…-solana-m-extensions-identity` | b1k-231 | D1 |
| 18 | `immunefi-openzeppelin/honest-zero-openzeppelin-contracts` | 16 | PARKED | `…-openzeppelin-contracts-identity` | b1k-139 | D1 |
| 19 | `immunefi-silofinance-v2/honest-zero-silo-sol` | 15 | PARKED | `…-silo-sol-identity` | b1k-152 | D1 |
| 20 | `immunefi-xterio/honest-zero-xt-contracts` | 15 | PARKED | `…-xt-contracts-identity` | b1k-212 | D1 |

b1k-* cohort key set (13 keys, rows 6-10, 12-13, 15-20): `state, verdict,
title, mission_id, program_id, run_id, finding_count,
no_submission_performed, pin, scope_file, [reports], deliverable,
updated_at` — no `claimable`, no `claim_review`, no `do_not_submit`;
`scope_file`/`reports` point into `.ufo/bounty-fleet/` (out-of-package
evidence locations).

## Deviation classes D1-D13 (each with file:line)

- **D1** `claimable` absent 13/20 sample, **241/280** tree-wide — exactly the
  b1k-* producer cohort (13/13 sample, 232/233 tree-wide; exemplar
  `[lost-tree] claims/hackerone-automattic/honest-zero-jetpack/status.json:1-15`, 13
  keys, none `claimable`). `claimable:true` only **12/280**.
- **D2** `claim_review` absent 15/20, **254/280** tree-wide; present only
  26/280. Sample holders: auth0-okta `:41`, opus-guard `:16`, spacex `:15`,
  hyatt `:15`, x `:14`.
- **D3** `claim_review` present but lacking `hard_gates`+`subchecks`: hyatt
  `:15-31` (keys = `blocker_codes, claim_ready, outcome, producer_identity,
  reviewer`); 6/280 tree-wide.
- **D4** submit guards: `do_not_submit` absent 14/20;
  northwestern-mutual `:1-16` has NEITHER guard; polarity inversion
  opus-guard `:15` `do_not_submit:false` on `state:"BLOCKED"` `:2` +
  `claimable:false` `:10` (cf. the opposite-direction mozilla trap at
  `corpus/knowledge/submitted-registry.md:146-148`).
- **D5** `manifest_sha256` absent (automattic / github / vercel-open-source,
  each `:1-15`; last field `updated_at:14` — the binding is not merely null,
  it is unrepresentable) or null (hyatt `:7`); **84/280** tree-wide (71
  absent + 13 null).
- **D6** `deliverable` escapes the package root: northwestern-mutual `:7` =
  `[lost-tree] evidence/bugcrowd-northwestern-mutual-mbb-og/`; hyatt `:8` =
  `[lost-tree] evidence/hackerone-hyatt/`. Other 18/20 all start with `claims/`.
- **D7** six-file anatomy not met: hyatt dir holds only `BLOCKED.md,
  INGESTION.md, claim.json, status.json` (1/6 canonical);
  northwestern-mutual only `status.json` + `submit/` (1/6). Other **18/20**
  hold the full six-file set.
- **D8** `updated_at` absent: hyatt (uses `blocked_at:32`); 14/280 tree-wide.
- **D9** non-canonical keys / naming drift: auth0-okta `round_summary:18`,
  `credentialed_backlog:33`, `evidence_dir:74`, `lane_outputs:75` (absolute
  out-of-tree path into `origin-work/ufo-fsd-alpha/.ufo/missions/…`);
  cantina-reserve date-suffixed `review_20260915:17` (with
  `artifacts_present:false` `:21` — a self-declared dangling artifact) +
  `polish_20260915:26` + `finding:7` alias; northwestern-mutual
  `positive_finding:10`, `target_interaction_performed:11`,
  `parked_at_transition:13`, `verdict_correction:14`; hyatt
  `blocked_reason:14` where the canonical `claimability_blocker` occurs 0×
  in the sample (`resume_condition` at auth0-okta `:73`, opus-guard `:57`).
- **D10** `verdict` is a free-form per-package slug, not an enum: 19
  distinct/20, **249 distinct/280** (88.9% singletons); `honest-zero-*` =
  256 (91%) with two undocumented dominant suffixes `-identity` (**121**)
  and `-host-binding` (**69**); 4 prose-sentence verdicts (auth0-okta `:3`);
  `positive-blocked-*` = **2/280** (consistent with r13 U5); 0/20 in sample.
- **D11** the documented `state` enum omitted PARKED (**248/280** = 88.6%) —
  repaired round-14 in `corpus/knowledge/claim-package-contract.md:31`.
- **D12** DONE ≠ filed: spacex-starlink `:9` `claimable:true`, `:7`
  `submitted_url:null`, `:12` `submission_state:"STAGED — operator-gated…"`;
  x `:9`/`:7` same shape, no `submission_state`. Both DONE packages'
  `submission_url` values are destination endpoints — exactly the
  `corpus/knowledge/submitted-registry.md:138-141` trap. Tree-wide: `submission_performed
  ===true` occurs **0/280**; any-SIG = 29/280 (8/8 eligible DONE, 5/245
  PARKED, 4/10 BLOCKED).
- **D13** deviation burden: **16/20** sample and **260/280 (92.9%)**
  tree-wide fail the canonical required-key test (missing `claimable` |
  missing `claim_review` | `claim_review` lacking `hard_gates`/`subchecks` |
  `manifest_sha256` absent/null | neither submit guard). +1 semantic-only
  (opus-guard polarity) = 17/20 carry some deviation. Conformant: 20/280.
  Type surprises (non-bool `claimable`, non-int `finding_count`, non-str
  `state`): **none**.

## Sample histograms (n=20)

- Field presence: `claimable` absent 13 (true 2 / false 5); `claim_review`
  absent 15 (5 dicts); `do_not_submit` absent 14 (true 3 / false 3);
  `no_submission_performed` absent 4 (true 16); `submission_performed`
  absent 13 (false 7, **true 0**); `manifest_sha256` absent 3 / null 1 /
  str 16; `updated_at` absent 1; `submitted_url` absent 15 / null 5;
  `submission_url` + `claim_url` present 2 each; `program_id` absent 4;
  `state`/`verdict`/`title`/`mission_id`/`deliverable` present 20/20.
- `claim_review.outcome`: APPROVED 2 / BLOCKED 2 / NOT_APPROVED 1 / absent 15.
- `finding_count`: 0 ×18, 1 ×2, absent 0.

## Consequences for the skill layer (applied round 14)

- `SKILL.md` Evidence-package anatomy `status.json` row now carries the
  attestation strength (full contract 20/280; cohort counts) instead of
  presenting `claimable`/`claim_review` as universal.
- `corpus/knowledge/claim-package-contract.md` state enum + verdict patterns + `claimable`
  absence + blocker-naming drift annotated.
- The six-file contract line names the two 1/6 packages as sampled reality.
- Verdict-suffix vocabulary (`-identity`, `-host-binding`) is now documented;
  any future consumer keying on `verdict` prefixes must treat it as free text.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/claims/*/*/status.json; 20 full status.json reads selected by the round-14 stratified sample.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-anatomy-sample.md
