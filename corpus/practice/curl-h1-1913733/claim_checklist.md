# Claim checklist — curl / HackerOne 1913733 (retrospective practice package)

OPERATOR-GATED: every step below is an operator action. This package has been
submitted nowhere, no external effect has been performed, and the finding
it describes is already public and fixed upstream; it is not claimable.

## Program

- Program: curl (project curl / libcurl)
- Official program URL: https://hackerone.com/curl
- Official advisory URL: https://curl.se/docs/CVE-2023-28319.html
- Original report: https://hackerone.com/reports/1913733

## Submission steps (operator only)

1. Treat this package as training material only. Its blocker is in
   status.json: the issue is already disclosed and fixed upstream
   (CVE-2023-28319, curl 8.1.0); any submission would duplicate
   HackerOne report 1913733. Do not submit.
2. If an operator ever reuses the lab outline in report.md, run it only
   against a local build in an isolated lab. This lane refuses
   live-target testing (PROVINCE.md): no probe, scan, login or submission
   to any target.
3. Attach evidence/S120.txt (sha256 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690) and the other
   two evidence artifacts with the digests printed in report.md, only
   for reviewer inspection.
4. Copy the scope, impact and timeline fields from report.md; do not
   restate the vendor text in stronger terms than the advisory's own
   Severity: Medium, and do not price a new curl finding above the
   current policy (no bounty; cvss not-set-by-vendor).
5. Keep external_effects_performed empty in provenance.json until a
   submission receipt exists outside this package.

## Residual gates

- OPERATOR-GATED operator submission gate — no agent may submit, message a
  vendor, or create a portal record. This package is PARKED and
  do_not_submit is true.
- OPERATOR-GATED prior-submission check — the report is public, credited
  to Wei Chong Tan and fixed in curl 8.1.0; duplicates are certain.
- OPERATOR-GATED reviewer distinctness — status.json carries reviewer
  identity "ReviewC2Package" (verdict CHANGES-REQUESTED on the
  candidate, fixes applied at integration, re-review not recorded); an
  independent reviewer distinct from the producer (ExecC2Package) and
  verifier (KasegiR85) identities must approve before claimable may
  flip to true.

No credential material, token, cookie value or private key is stored in this
package. No submission performed.
