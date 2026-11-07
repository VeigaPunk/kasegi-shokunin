# Claim checklist — curl / CVE-2025-9086 (worked exemplar)

OPERATOR-GATED: every step below is an operator action. This package has been
submitted nowhere, and no external effect has been performed.

## Program

- Program: curl (project curl / libcurl)
- Official advisory URL: https://curl.se/docs/CVE-2025-9086.html
- Channel the advisory names: HackerOne report https://hackerone.com/reports/3294999

## Submission steps (operator only)

1. Open the program's own submission form on the portal. The captured advisory
   names a HackerOne report as the original channel; it does not state the
   program's submission-form URL, so the operator confirms the form address on
   the program page before any other step.
2. Search the program for an existing report of CVE-2025-9086 before composing
   anything. The advisory CREDITS name Google Big Sleep as reporter and Daniel
   Stenberg as patcher, so this disclosed issue must be treated as already
   reported until the search proves otherwise.
3. Attach evidence/source-capture.txt (sha256 7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b) and the three excerpt
   artifacts, with the digests printed in report.md.
4. Copy the scope, impact and timeline fields from report.md; do not restate the
   vendor text in stronger terms than "Severity: Low".
5. Keep external_effects_performed empty in provenance.json until a submission
   receipt exists; record that receipt outside this package.

## Residual gates

- OPERATOR-GATED operator submission gate — no agent may submit, message a
  vendor, or create a portal record.
- OPERATOR-GATED prior-submission check — the finding is public and credited;
  only the operator can confirm on the portal that no duplicate exists.
- OPERATOR-GATED reviewer distinctness — status.json carries the fixture
  reviewer identity "exemplar-reviewer"; an independent reviewer distinct from
  the producer and verifier identities must sign claim_review before claimable
  may flip to true.

No credential material, token, cookie value or private key is stored in this
package.
