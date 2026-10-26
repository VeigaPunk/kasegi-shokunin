# Claim checklist — Sky on Immunefi (`claims/immunefi-sky/2026-10-26-public-disclosure-reprice/`)

**OPERATOR-GATED.** Nothing in this checklist has been executed. Submission requires the operator's explicit go-ahead in the session that files it; this package was built to price a public disclosure, and its own status is PARKED, `claimable: false`.

## Do not submit this package

The priced finding is a prior public submission, paid in 2023 (`evidence/sky-rce-bugfix-review.txt:39-40`). Re-filing it, or filing a variant of it, is a duplicate against the program and against Immunefi's own rules. The only use of this package is rubric calibration: it shows what the platform ladder and the program ladder produce for a disclosed finding whose actual payout is known.

## Portal route (as printed on the program page)

| Step | What the page says | Where |
|---|---|---|
| 1 | open the program page, press "Submit a Bug" | `evidence/sky-program-scope-rewards.txt:79` |
| 2 | pick the asset from the program's in-scope inventory — "Total Assets in Scope 255" | `:1017` |
| 3 | attach a working PoC — "Proof of concept is always required for all severities." | `:993` |
| 4 | no KYC step is required to be paid | `:989` |
| 5 | disclosure of the report is gated — "Category 3: Approval Required" | `:995` |

Reward attribution is by impact, from the Impacts in Scope table: "Rewards are distributed according to the impact the vulnerability could otherwise cause based on the Impacts in Scope table further below." (`:112-113`).

## Field-by-field quirks a filer would hit

- **The asset row for the affected host is not machine-readable from the capture.** The page states "Total Assets in Scope 255" (`:1017`) but the asset inventory is client-rendered: the 554144-byte HTML carries no per-asset records, and the only occurrence of the vote host is the scope sentence at `:175`. A filer must resolve the exact asset row live, in an authenticated session, and re-capture it.
- **This host accepts Critical only.** "All Medium and High level bug reports are not in-scope for the https://vote.sky.money/ asset. Only Critical severity reports are in-scope for this asset." (`:175`). A self-rating below Critical on this asset is not merely low, it is out of scope.
- **The polling clause is a decoy for this class.** USD 10,000 attaches to poll-outcome manipulation (`:171`), not to command execution on the polling application. Price against `:116`.
- **Testing route is constrained.** "Any testing on mainnet or public testnet deployed code; all testing should be done on local-forks of either public testnet or mainnet" (`:998`). The published 2023 PoC route itself queried a public-testnet endpoint (`evidence/sky-rce-bugfix-review.txt:57`); a re-execution would breach the current prohibited-activities list.
- **Payment is in tokens, not USD.** "payouts are done in DAI or USDS … assuming a full 1:1 ratio with the USD" (`:195`), with "a delay of up to 1 calendar month after the date of validation of the bug report" (`:196`).

## Residual gates (all unmet here)

1. **Authorization** — no authorized testing; `PROVINCE.md:52` refuses live-target testing, and the program's prohibited activities independently forbid the published route. Recorded in `evidence/no-live-testing.txt`.
2. **Duplicate / prior submission** — the finding is public and paid; the program also lists "Public Disclosure of Known Issues" as ineligible (`:133`).
3. **Reviewer distinctness** — the contract requires a non-author reviewer with a resolved model and an approval; none is attached to this wave-1 item, so `state: DONE` is unreachable.
4. **Asset-row capture** — the specific in-scope asset record must be captured live from the authenticated inventory before any filing; the capture in this package cannot supply it.
5. **PoC** — a filing needs a PoC the program accepts; this package deliberately contains none, because building one requires testing the refusal in gate 1 forbids.

## If the operator ever reverses gate 1

Order of work: capture the asset row live → write the PoC against a local fork (never a public testnet) → re-price against `:116` → attach the six-file package → obtain a distinct reviewer → file. Until gate 1 reverses, this remains a calibration artifact and nothing more.
