# Claim checklist — ibb / HackerOne 1997312 (retrospective practice package)

OPERATOR-GATED: every step below is an operator action. This package has been
submitted nowhere, no external effect has been performed, and the finding
it describes is already public and fixed upstream; it is not claimable.

## Program

- Program: ibb (Internet Bug Bounty, HackerOne team)
- Official record URL: https://hackerone.com/reports/1997312
- Original report: https://hackerone.com/reports/1913733
- Advisory URL: https://curl.se/docs/CVE-2023-28319.html (reused round-85
  evidence S120; the IBB record covers the same issue)

## Submission steps (operator only)

1. Treat this package as training material only. Its blocker is in
   status.json: the issue is already disclosed and fixed upstream
   (CVE-2023-28319, curl 8.1.0); any submission would duplicate HackerOne
   report 1997312 (and 1913733). Do not submit.
2. If an operator ever reuses the lab outline in report.md, run it only
   against a local build in an isolated lab. This lane refuses
   live-target testing (PROVINCE.md): no probe, scan, login or submission
   to any target.
3. Attach evidence/S122.txt (sha256 ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1),
   evidence/S123.txt (sha256 22a7d5bed4d4081db7e94e4c788a5aaf12ed8dc8f7607536ef4ad36828de4ab5)
   and the other two evidence artifacts with the digests printed in
   report.md, only for reviewer inspection. Note: S122 carries a
   presigned-URL token matching the gate's credential shape twice; the
   byte-identical artifact is kept for evidence binding and the overlap
   is documented in report.md §Evidence rather than redacted away.
4. Copy the scope, impact and timeline fields from report.md; do not
   restate the vendor text in stronger terms than the advisory's own
   Severity: Medium, and do not price a new curl finding above the
   current policy (no rewards; program ended 2026-01-31).
5. Keep external_effects_performed empty in provenance.json until a
   submission receipt exists outside this package.

## Residual gates

- OPERATOR-GATED operator submission gate — no agent may submit, message a
  vendor, or create a portal record. This package is PARKED and
  do_not_submit is true.
- OPERATOR-GATED prior-submission check — the reports are public, credited
  to Wei Chong Tan and fixed in curl 8.1.0; duplicates are certain.
- OPERATOR-GATED reviewer distinctness — status.json carries reviewer
  identity "ReviewC2Package" (CHANGES-REQUESTED; fixes applied by the L1, no re-pass); an independent reviewer
  distinct from the producer (ExecC2Package) and verifier (KasegiR86)
  identities must approve before claimable may flip to true.

No usable credential, token, cookie value or private key is stored in this
package (the S122 presigned query strings were removed at integration). No submission performed.
