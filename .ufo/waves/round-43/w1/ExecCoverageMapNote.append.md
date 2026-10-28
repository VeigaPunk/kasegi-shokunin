
## Round-43 note — the claim-package contract gains an instrumented surface (appended 2026-10-28)

The coverage map above and the frontier table are not edited in place (R6). The map's
`Claim-package contract` row has so far been documentation-only — one entry,
`knowledge/claim-package-contract.md`, describing gates whose `ops/claim-check.mjs` went with
`~/Projects/bounties` — and this round the contract gains an executable surface:
`instruments/claim-package-check.py` (eight rules, one `RULE <id> verdict=` line each) over the
committed exemplar `instruments/fixtures/claim-package/exemplar/` and nine one-delta fixtures
`instruments/fixtures/claim-package/defect-1-missing-file` through `defect-9-secret`, documented by
the new entry `knowledge/claim-package-gate.md`. NO frontier row (F01-F25) changes and the measured
ratio is unchanged: 25/25 admitted, still 0 of 18 lost-domain surfaces present.
