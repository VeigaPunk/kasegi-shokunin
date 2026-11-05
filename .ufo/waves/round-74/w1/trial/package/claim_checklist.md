# Submission checklist - curl (claim-package trial)

Program intake, as the captured policy page states:

- HIGH or CRITICAL findings stay private on HackerOne until a fixed release
  ships (policy L65, L72); LOW and MEDIUM are redirected to the public GitHub
  issue tracker or a pull-request (policy L50).
- The reporter reports on HackerOne (policy L49); email intake is refused by
  the policy.
- curl is a CVE Numbering Authority and assigns its own CVE ids.
- All handled reports, valid or not, are disclosed publicly (policy L91).
- The project itself pays no bounty (policy L43); advisory-recorded rewards such
  as the 4660 USD of CVE-2023-38545 flow through the HackerOne intake platform.

## Submission steps (operator only)

1. OPERATOR-GATED - this lane holds no authorized engagement with the curl
   project or any intake platform; nothing here is submitted.
2. If an operator later authorizes a program engagement: file on the program's
   HackerOne intake with the advisory-style field set (title, affected versions,
   severity band, repro conditions, suggested fix), then follow the program's
   own disclosure clock.
3. After handling, expect the report itself to be published per policy L91.

## Residual gates

- OPERATOR-GATED: operator program engagement (the only path to a claimable
  package; the authorization hard gate fails today by design).
- OPERATOR-GATED: duplicate/prior-submission check against the intake platform.
- Independent reviewer: this trial's reviewer is a distinct identity but the
  same single seat; a second-party review is owed before any claimable flip.
