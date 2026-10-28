# CVE-2025-9086 curl cookie path out-of-bounds read (claim-package exemplar)

Program: curl (project curl / libcurl)
Official advisory URL: https://curl.se/docs/CVE-2025-9086.html
Package kind: worked exemplar built from the vendor's published advisory for an
already-disclosed, already-fixed issue. It records no new discovery, claims no
unpublished finding, and names no person beyond the credits the vendor printed.

## Scope excerpt

Source URL: https://curl.se/docs/CVE-2025-9086.html (Project curl Security Advisory, September 10 2025)
observed_at: 2026-10-28T16:46:34Z
content sha256: 9b81dd48db37b26303360334229c630f3e8ff32767b0ed68dd32a98e1d69e543
  (evidence/source-excerpt.txt; the full captured document is
  evidence/source-capture.txt, sha256 7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b)

Verbatim scope, severity and affected-version lines from capture lines 82-91:

> CWE-125: Out-of-bounds Read
> Severity: Low
> Bug bounty: 505 USD
> Area: cookies
> Original report: https://hackerone.com/reports/3294999
> AFFECTED VERSIONS
> Affected versions: curl 8.13.0 to and including 8.15.0
> Not affected versions: curl < 8.13.0 and >= 8.16.0
> Not affected versions: curl >= 8.14.2 in the 8.14.X branch
> Introduced-in: https://github.com/curl/curl/commit/1aea05a6c2699e80c7593

## Vulnerability class

CWE-125: out-of-bounds read in the cookie path comparison. A cookie set with the
secure keyword on an https:// host is later compared against a cookie of the same
name set on the clear-text http:// host with only a slash as its path; the path
comparison reads past the single-byte heap allocation that holds the path.

## Affected asset

curl 8.13.0 through 8.15.0, with the 8.14.X branch fixed from 8.14.2 (vendor
AFFECTED VERSIONS text above). The vendor states the flaw does not affect the
curl command line tool; the library path is the affected asset.

## Impact

The vendor rates the issue Severity: Low and records a Bug bounty: 505 USD for
the original report. The read either crashes the process or makes the comparison
reach the wrong conclusion, letting the clear-text site override the contents of
the secure cookie depending on the heap bytes after the allocation. The vendor
calls the operation fragile and notes the attacker needs control of the http://
site using the same name, or MITM capability.

## Reproduction (isolated lab only)

1. Build an affected curl (8.13.0 through 8.15.0) with sanitizers enabled.
2. Against a local loopback listener, set a cookie with the secure keyword for an
   https:// host name.
3. Redirect to http:// on the same host name and set a cookie of the same name
   with path set to a single slash.
4. Observe the path comparison reading past the one-byte path allocation; an ASan
   build reports a heap out-of-bounds read.

No credential material, no live third-party target and no exploit payload is
recorded in this package.

## Suggested fix

Upgrade to curl 8.16.0 (vendor RECOMMENDATION A) or apply the vendor fix commit
c6ae07c6a541e0e96d0040afb6 (Fixed-in); alternatively avoid http:// for cookies
(vendor RECOMMENDATION C).

## Disclosure timeline (vendor)

- 2025-08-11 reported to the curl project
- 2025-09-05 distros@openwall contacted
- 2025-09-10 curl 8.16.0 released around 06:00 UTC, coordinated with the advisory
- vendor states no active exploits were known at publication
- 2026-10-28 advisory captured as S067 for this exemplar

## Evidence

- evidence/source-capture.txt sha256 7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b polarity: positive
- evidence/source-excerpt.txt sha256 9b81dd48db37b26303360334229c630f3e8ff32767b0ed68dd32a98e1d69e543 polarity: positive
- evidence/solution-fixed-in.txt sha256 8e3d1b43a01a06397fe6141bfc9321cf695679e40d7260664ec23abaa1c3fc8b polarity: negative
- evidence/disclosure-timeline.txt sha256 8bececb6b37ba63f5c9fd32dd1b8b9f2cc08cb75ec443ffe81777ec6ed52bb8f polarity: positive

## Submission

No filing has been made..
