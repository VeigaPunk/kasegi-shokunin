# HackerOne 1997312 (IBB) — CVE-2023-28319 payer record (retrospective practice package)

Program: ibb (Internet Bug Bounty team on HackerOne)
Record: https://hackerone.com/reports/1997312
Original report: https://hackerone.com/reports/1913733
Package kind: retrospective practice package for an already-disclosed,
already-fixed issue. It is a training artefact built from public captures;
it makes no claim on any bounty, invents no new finding, and records no
contact with any target. Evidence digests: S120 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690, S121 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102,
S122 ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1, S123 22a7d5bed4d4081db7e94e4c788a5aaf12ed8dc8f7607536ef4ad36828de4ab5.

What this package prices: the IBB team's HackerOne record 1997312 for
CVE-2023-28319, which the round-85 package
(corpus/practice/curl-h1-1913733/) left open with "No captured record shows
who paid it". This package resolves the payer from the IBB record itself
and the curl maintainer's 2026-01-26 post, without merging the 2023
vendor record into the payout. All priced values come from the four
captures below; nothing is priced from memory.

## Scope excerpt

HackerOne JSON record of report 1997312 (S122, one-line JSON snapshot).
Source URL: https://hackerone.com/reports/1997312.json
observed_at: captured 2026-11-07T00:58:29Z (cross-checked 2026-11-07)
content sha256: ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1

The record's identity lines, verbatim JSON fragments from S122:

> "title":"CVE-2023-28319: UAF in SSH sha256 fingerprint check"
> "severity_rating":"medium"
> "has_bounty?":true
> "cve_ids":["CVE-2023-28319"]
> "handle":"ibb"
> "offers_bounties":true
> "name":"Internet Bug Bounty"
> The original submission can be found here: https://hackerone.com/reports/1913733

`max_severity: critical` in the IBB record's structured_scope is the
asset's ceiling on the team, not this report's rating; the report's own
rating is `severity_rating: medium`, and the advisory agrees (see Pricing).

Curl's current disclosure policy (S121, reused from round 85):

> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.

The maintainer's end-of-bounty post (S123, 2026-01-26):

> There is no longer a curl bug-bounty program. It officially stops on January 31, 2026.
> I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years.

## Vulnerability class

CWE-416: Use After Free. S122 lists weakness "Use After Free"; the
advisory (S120) states CWE-416 and the CVE-2023-28319 assignment. The
flaw: libcurl's SSH sha256 fingerprint check freed the fingerprint
memory before returning an error message containing the now-freed hash.

## Affected asset

Affected versions: curl 7.81.0 to and including 8.0.1. curl < 7.81.0
and curl >= 8.1.0 are not affected, per S120 and repeated in S122's
vulnerability_information. The structured_scope asset is the curl
source repository (https://github.com/curl/curl, SOURCE_CODE).

## Impact

Vendor and platform ratings agree on medium (S120 `Severity: Medium`;
S122 `"severity_rating":"medium"`). Under curl's own four-level ladder
(S121), Medium is "less hard than Low to exploit or trigger" and
"usually needs something else to also happen to become serious". The
advisory's INFO text matches that rung: the flaw requires
CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256 on a libcurl build with libssh2,
plus CURLOPT_VERBOSE or CURLOPT_ERRORBUFFER; the free-to-use window
is extremely short and the largest possible leak per trigger is 186
bytes. No larger impact is claimed here.

## Reproduction (isolated lab only)

Isolated-lab outline reconstructed from the advisory's description
(S120). No exploit payload is included in this package, and no live
target was contacted or tested.

1. In an isolated lab, build an affected libcurl (7.81.0 through 8.0.1)
   with libssh2 support and sanitizers enabled.
2. Configure a local SSH server endpoint on loopback and point the lab
   build at it with CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256 set, plus
   CURLOPT_VERBOSE or CURLOPT_ERRORBUFFER, as the advisory requires.
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

Upgrading to curl 8.1.0 is the vendor's first recommendation. The lab
outline should re-run against 8.1.0 and observe the free-before-use no
longer occurring.

## Disclosure timeline

> This issue was reported to the curl project on March 21 2023. We contacted distros@openwall on May 9, 2023.
> curl 8.1.0 was released on May 17 2023, coordinated with the publication of this advisory.

S122 records the report as Closed/resolved, submitted 2023-05-23,
disclosed 2023-06-25. The vendor credits Wei Chong Tan (reporter) and
Daniel Stenberg (patcher), per S120 CREDITS. The IBB record 1997312 is
dated 2023-05-23 and names 1913733 as the original submission; the
package does not assert the mechanics of how the IBB team record was
raised.

## Evidence

- evidence/S120.txt sha256 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690 polarity: positive
- evidence/S121.txt sha256 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102 polarity: positive
- evidence/S122.txt sha256 ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1 polarity: positive
- evidence/S123.txt sha256 22a7d5bed4d4081db7e94e4c788a5aaf12ed8dc8f7607536ef4ad36828de4ab5 polarity: positive

Note on S122 and the secret-shaped-token scan: the byte-identical S122
artifact is bound to the round-86 manifest digest. The source JSON
contains an S3-style presigned `profile_picture_urls` entry whose
`X-Amz-Security-Token` query value matches the gate's generic
`credential` shape (`token=...`, 105 bytes, twice). That value is an
expired presigned-URL session token inside a public profile-picture
URL, not a program credential; the round-85 sibling record (S119) did
not carry one. The gate's R-NOSECRET rule is documented to be
unreachable on this capture; the candidate still carries the
byte-identical artifact so the evidence binding (E2) holds, and the
overlap is recorded here rather than silently redacting the evidence.
The 64-hex tokens cited above are each a manifest artifact digest.

## Pricing

price-program: ibb
price-payer: internet-bug-bounty
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: true
price-original-report: 1913733
price-reward-current-policy: ended 2026-01-31
price-kev: not-listed catalogVersion 2026.10.23
price-cve: CVE-2023-28319

> I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years.
> There is no longer a curl bug-bounty program. It officially stops on January 31, 2026.
> Bug bounty: 2400 USD
> We no longer offer any monetary rewards for security reports – no matter which severity.
> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.
> 87 confirmed vulnerabilities and over 100,000 USD paid as rewards to researchers.

Pricing derivation (all values re-derived from the captured records, not
from the package author's memory).

- price-program — the S122 team handle is `ibb` (the Internet Bug Bounty
  team's HackerOne programme record). Not `curl`: the round-85 package
  already prices `curl` from the 1913733 record; this package prices the
  IBB record.
- price-payer — the IBB record supplies the payer question the r85
  package left open. S122's team is `ibb` with `offers_bounties: true`,
  and S123 says the "Internet Bug Bounty project, which has paid the
  bounties for us" (full sentence quoted above). The payer is therefore
  `internet-bug-bounty`. This is a statement about who paid the
  bounties for curl, not a claim that the 2400 USD in the vendor record
  was disbursed by any specific party on a specific date.
- price-severity — agreement check: S122 `severity_rating` medium and
  S120 `Severity: Medium` agree (case-insensitive); the counter enforces
  agreement before accepting the value. `max_severity: critical` is
  rejected: it is the asset's ceiling, not the report's rating.
- price-reward-at-disclosure — the advisory (S120) records `Bug bounty:
  2400 USD`; that 2023 vendor record is the only amount captured.
  S122's `bounty_amount` is null, so the amount comes only from S120;
  the 2400 USD is the vendor-recorded figure, not a disbursement
  receipt.
- price-platform-bounty-flag — S122 `has_bounty?: true` (the IBB record
  once carried a bounty). Note the contrast with S119's false in
  round 85: the two records describe different teams, so their flags
  differ; the package keeps each flag with its own record.
- price-original-report — S122's vulnerability_information names the
  original submission 1913733; S120 carries the matching
  `Original report: https://hackerone.com/reports/1913733` line. Both
  records agree on 1913733.
- price-reward-current-policy — S123: "It officially stops on January
  31, 2026." and S121: "There is no bug bounty...". Combined value:
  `ended 2026-01-31`. This describes today's policy (no rewards offered
  going forward); it does not retroactively erase the 2400 USD recorded
  for this 2023 report. S123 also quotes the program totals:
  "87 confirmed vulnerabilities and over 100,000 USD paid as rewards
  to researchers" (retrospective program totals, not this report's
  amount).
- price-kev — CVE-2023-28319 occurs 0 times in the round-35 KEV capture
  (S052, catalogVersion 2026.10.23, captured 2026-10-26 in round 35 and
  not re-fetched for this package), so the value is `not-listed` as of
  that catalog only.
- price-cve — S122 `cve_ids[0]` is CVE-2023-28319, the same identifier
  the advisory assigns to the issue.

What no captured record shows: no capture states the split of the
2400 USD between the reporter and the project, or between any other
parties, and no capture is a payment receipt showing a disbursement
was made. S120 records a bounty amount; S123 names the payer in
general terms. The package prices the recorded amount under the
vendor record, names the payer as `internet-bug-bounty`, and does
not assert a per-party split it cannot source.

## Submission

No submission performed.
