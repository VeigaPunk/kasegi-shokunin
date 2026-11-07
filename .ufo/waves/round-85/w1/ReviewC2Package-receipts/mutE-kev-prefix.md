# CVE-2023-28319 curl SSH sha256 fingerprint check use-after-free (retrospective practice package)

Program: curl
Official program URL: https://hackerone.com/curl
Official advisory URL: https://curl.se/docs/CVE-2023-28319.html
Package kind: retrospective practice package for an already-disclosed,
already-fixed issue. It is a training artefact built from public captures;
it makes no claim on any bounty, invents no new finding, and records no
contact with any target. Evidence digests: S119 9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105, S120 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690,
S121 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102.

## Scope excerpt

Source URL: https://curl.se/dev/vuln-disclosure.html (curl vulnerability-disclosure policy, captured 2026-11-07T00:26:30Z)
observed_at: 2026-11-07T00:26:30Z
content sha256: 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102

The HackerOne record's structured_scope names the in-scope asset
verbatim:

> structured_scope asset_identifier: https://github.com/curl/curl
> structured_scope asset_type: SOURCE_CODE
> structured_scope max_severity: critical

The curl program's own policy wording (S121):

> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.
> Information
> All known and public curl or libcurl related vulnerabilities are listed on the curl website security page.

The advisory's scope-relevant lines (S120):

> Area: SSH
> Original report: https://hackerone.com/reports/1913733
> AFFECTED VERSIONS

## Vulnerability class

CWE-416: Use After Free. The advisory's VULNERABILITY text says libcurl offers a feature to
verify an SSH server's public key using a SHA 256 hash; when the check
fails, libcurl freed the memory for the fingerprint before returning an
error message containing the now-freed hash, risking insertion of
sensitive heap-based data into the error message. The HackerOne record
lists weakness "Use After Free" and cve_ids CVE-2023-28319.

## Affected asset

Affected versions: curl 7.81.0 to and including 8.0.1 The advisory also states that curl < 7.81.0 and curl >= 8.1.0
are not affected, and the issue was introduced in commit
3467e89bb97e6c87c7. The structured_scope asset is the curl source
repository (https://github.com/curl/curl, SOURCE_CODE).

## Impact

The vendor rates the issue Severity: Medium and the HackerOne record's
severity_rating is medium. Under the curl policy's own severity ladder,
the vendor defines Medium as:

> This is a security problem that is less hard than Low to exploit or trigger. Less strict timing, wider platform availability or involving more widely used options or protocols. A problem that usually needs something else to also happen to become serious. Past example

That definition requires something else to also happen before the
problem becomes serious, which matches the advisory's own INFO text: the
flaw only applies to users of the CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256
option on libcurl builds using libssh2, and either CURLOPT_VERBOSE or
CURLOPT_ERRORBUFFER must also be set; the time window between the free
and the use is extremely short, and the largest possible info leak per
trigger is 186 bytes (CURL_ERROR_SIZE minus the 69-byte prefix), ending
at the first null byte within those bytes. The HackerOne report's own
reproduction note is the code-reader observation that the
fingerprint_b64 pointer is passed as a parameter for failure logging
after it is freed (curl/lib/vssh/libssh2.c).

## Reproduction (isolated lab only)

Isolated-lab outline reconstructed from the advisory's own description
(S120). No exploit payload is included in this package, and no live
target was contacted or tested.

1. In an isolated lab, build an affected libcurl (7.81.0 through 8.0.1,
   per Affected versions: curl 7.81.0 to and including 8.0.1) with libssh2 support and sanitizers enabled.
2. Configure a local SSH server endpoint on loopback and point the lab
   build at it with CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256 set, plus
   CURLOPT_VERBOSE or CURLOPT_ERRORBUFFER, as the advisory's INFO text
   requires.
3. Make the server's public key differ from the configured SHA 256 hash
   so the fingerprint check fails.
4. Observe the free-before-use of the fingerprint buffer in the failure
   logging path; a sanitizer build reports the use-after-free.

No credential material, no cookie value and no key material is recorded
in this package.

## Suggested fix

Advisory SOLUTION and RECOMMENDATIONS (S120):

> Fixed-in: https://github.com/curl/curl/commit/8e21b1a05f3c0ee098dbcb6c
> A - Upgrade curl to version 8.1.0
> B - Apply the patch to your local version
> C - Do not use CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256

Upgrading to curl 8.1.0 is the vendor's first recommendation; the fix
commit is the one named above. The lab outline should re-run against
8.1.0 and observe the free-before-use no longer occurring.

## Disclosure timeline (vendor, S120 TIMELINE)

> This issue was reported to the curl project on March 21 2023. We contacted distros@openwall on May 9, 2023.
> curl 8.1.0 was released on May 17 2023, coordinated with the publication of this advisory.

The advisory is dated May 17 2023; the HackerOne record shows the
report as Closed/resolved with disclosed_at 2023-05-24T08:25:54.715Z.
The vendor credits Wei Chong Tan (reporter) and Daniel Stenberg
(patcher).

## Evidence

- evidence/S119.txt sha256 9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105 polarity: positive
- evidence/S120.txt sha256 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690 polarity: positive
- evidence/S121.txt sha256 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102 polarity: positive

## Pricing

price-program: curl
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: false
price-reward-current-policy: none
price-cvss: not-set-by-vendor
price-kev: not-listed-anything
price-cve: CVE-2023-28319

> CWE-416: Use After Free
> Bug bounty: 2400 USD
> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.
> We do not support CVSS as a method to grade security vulnerabilities, so we do not set them for CVE records published by the curl project. We believe CVSS is a broken system that often does not properly evaluate to suitable severity levels that reflect all dimensions and factors involved. Other

Pricing derivation (all values re-derived from the captured records, not
from the package author's memory).

- price-frequency check — the HackerOne record (S119) says
  severity_rating medium, matching the advisory's `Severity: Medium`; the
  comparison is case-insensitive, and the counter enforces that both
  records agree before accepting the value.
- price-reward-at-disclosure — the advisory (S120) records its own line
  `Bug bounty: 2400 USD`, so the disclosed report earned 2400 USD as recorded by the
  vendor at the time.
- price-platform-bounty-flag — the HackerOne team record (S119) says
  has_bounty? false. That flag describes the platform team's current
  bounty configuration; it does not by itself mean this report was
  unpaid. The advisory (S120) separately records a 2400 USD bounty for
  this specific report, so the report was paid while the platform flag
  reads false — the two records measure different things and the
  counter keeps them as separate fields.
- price-reward-current-policy — the current curl disclosure policy
  (S121) opens with `There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.`, so a new curl finding submitted today would
  price at no reward under the current policy. That statement governs
  new findings; it does not retroactively erase the 2400 USD recorded
  for this one in 2023.
- price-cvss — the current policy (S121) says `We do not support CVSS as a method to grade security vulnerabilities, so we do not set them for CVE records published by the curl project. We believe CVSS is a broken system that often does not properly evaluate to suitable severity levels that reflect all dimensions and factors involved. Other` (the rest of that
  sentence continues in the capture; the leading clause is the exact
  vendor wording). The vendor sets no CVSS for its CVE records, so the
  package records not-set-by-vendor rather than a numeric score.
- price-kev — CVE-2023-28319 occurs 0 times in the round-35 KEV capture
  (S052, catalogVersion 2026.10.23), so the value is not-listed with
  that catalogVersion recorded beside it.
- price-cve — the HackerOne record (S119) lists cve_ids CVE-2023-28319,
  the same identifier the advisory (S120) assigns to the issue.

## Submission

No submission performed.
