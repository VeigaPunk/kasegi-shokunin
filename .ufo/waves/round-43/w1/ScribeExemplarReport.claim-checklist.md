# Claim checklist — curl / CVE-2023-38545 (worked exemplar)

OPERATOR-GATED: every step below is an operator action. This package has been
submitted nowhere and performed no external effect. It carries no credential
material of any kind.

## Program

- Program: curl (project curl / libcurl)
- Official advisory URL: https://curl.se/docs/CVE-2023-38545.html
- Channel the advisory names: HackerOne report https://hackerone.com/reports/2187833

## Submission steps (operator only)

1. **Operator submission gate.** The operator confirms the program's current
   scope page and decides whether a report is submitted. No agent submits,
   messages a vendor, or creates a portal record; this package performs no
   submission.
2. **Prior-submission check.** The issue was reported to the curl project on
   2023-09-30, credited to Jay Satiro, and is public at
   https://hackerone.com/reports/2187833 and
   https://curl.se/docs/CVE-2023-38545.html. The operator confirms on the
   program page that no duplicate exists before treating the finding as new.
3. **Reviewer distinctness.** The reviewer identity in `status.json` must differ
   from every producer and verifier identity in `evidence/manifest.json`; the
   producer never self-approves. The fixture reviewer identity is a role, not an
   independent review, so this gate stays open until a distinct reviewer signs
   `claim_review`.
4. **Portal route and fields (per program).** The advisory names a HackerOne
   report as the original channel and does not state the program's submission
   form. The operator confirms the live program page, its required fields and its
   own disclosure rules; no URL beyond the captured ones is asserted here.
5. **Quirks.** The advisory is first-party at curl.se and the flaw was fixed in
   8.4.0, so any submission must quote the program's current policy, not this
   2023 advisory, as the scope authority, and must not restate the vendor text
   more strongly than "Severity: High".
6. **Evidence hand-off.** Attach `evidence/source-capture.txt` and the three
   excerpt artifacts, with the digests printed in `report.md`. Keep
   `external_effects_performed` empty in `provenance.json` until a submission
   receipt exists, and record that receipt outside this package.

## Residual gates

- OPERATOR-GATED operator submission — not performed
- OPERATOR-GATED prior-submission / duplicate check — open
- OPERATOR-GATED reviewer distinctness — open until a reviewer distinct from
  every producer and verifier identity signs `claim_review`
- `claimable: false` — the package does not enter the claim-ready queue
