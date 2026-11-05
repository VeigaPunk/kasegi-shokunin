# CVE-2023-38545 libcurl SOCKS5 heap buffer overflow (claim-package trial)

Program: curl (project curl / libcurl)
Official advisory URL: https://curl.se/docs/CVE-2023-38545.html
Package kind: end-to-end trial (round-74 SHONEN box 2; considerthese/2026-10-26.md
proposal 2) built from the vendor's published advisory for an already-disclosed,
already-fixed issue. It records no new discovery, claims no unpublished finding,
performs no testing against any target, and names only people the vendor credited.

## Scope excerpt

Source URL: https://curl.se/dev/vuln-disclosure.html (curl Vulnerability Disclosure Policy)
observed_at: 2026-11-05T08:55:15Z
content sha256: 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102
  (evidence/policy-capture.txt; the disclosed advisory capture is
  evidence/disclosure-capture.txt, sha256 327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b, observed_at 2026-11-05T08:54:46Z)

Verbatim policy text, policy capture lines 43, 49 and 93:

> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities. (policy L43)
> The person discovering the issue, the reporter, reports the vulnerability on HackerOne. Issues filed there reach a handful of selected and trusted people. (policy L49)
> The curl project's security team rates security problems using four severity levels depending on how serious we consider the problem to be. We use Low, Medium, High and Critical. (policy L93; the sentence wraps at L94 "vulnerabilities.")

The advisory's own scope block is excerpted byte-for-byte in
evidence/source-excerpt.txt (sha256 c6579512a8615420a077e3f068db29ae8c95147d0c8b1983302ae39bd9ef8d8e): severity CWE-122 "Severity: High"
(L100-L101), the recorded reward "Bug bounty: 4660 USD" (L108), the affected
range libcurl 7.69.0 to and including 8.3.0 (L112) and the disclosure timeline
(L126-L129).

## Vulnerability class

CWE-122: Heap-based Buffer Overflow (advisory L100). When curl passes the
hostname to a SOCKS5 proxy for remote resolution, a slow handshake can flip a
state-machine variable so curl copies the too-long hostname (up to 65535 bytes
are accepted) into the 16 kB download buffer instead of the resolved address.

## Reproduction (isolated lab only)

1. Build an affected libcurl (7.69.0 through 8.3.0) with sanitizers; do not set
   CURLOPT_BUFFERSIZE, or set it below 65541 (advisory L87).
2. Point curl at a socks5h:// proxy (CURLOPT_PROXYTYPE CURLPROXY_SOCKS5_HOSTNAME,
   --socks5-hostname, or a socks5h:// proxy environment variable; advisory L89-L95)
   whose handshake is slowed so the state-machine bug triggers.
3. Request a URL whose hostname is longer than the download buffer.
4. The handshake copies the oversized hostname into the heap buffer; an ASan
   build reports the heap-based overflow (advisory L85, L100).

No credential material, no live third-party target and no exploit payload is
recorded in this package.

## Impact

The advisory rates the issue "Severity: High" (L101). Under the program's own
policy language that is the third of four levels: High is "a serious problem
with real world impact" whose exploitation "is not hard" (policy L105), below a
Critical that requires arbitrary code execution on a common configuration
(policy L107). The advisory demonstrates memory corruption, not demonstrated
code execution, so its own rating sits at the policy's High band, not Critical.
On reward: the policy states the project pays nothing (policy L43), while the
advisory records a platform-side "Bug bounty: 4660 USD" (L108) for the original
HackerOne report (L102) - the reward came through the intake platform, not the
project's own policy.

## Affected asset

libcurl 7.69.0 to and including 8.3.0; not affected below 7.69.0 and from 8.4.0
(advisory L112-L113). The curl tool itself is only vulnerable when the download
buffer is set below 65541 bytes, e.g. via --limit-rate (advisory L87).

## Suggested fix

Upgrade to curl 8.4.0 (advisory RECOMMENDATIONS A) or apply the vendor fix
commit fb4415d8aee6c1 (advisory "Fixed-in"); the vendor also advises not using
CURLPROXY_SOCKS5_HOSTNAME proxies or socks5h:// environment variables as
workarounds (RECOMMENDATIONS C and D).

## Disclosure timeline (vendor)

- 2023-09-30 reported to the curl project (advisory L126)
- 2023-10-03 distros@openwall contacted (advisory L126)
- 2023-10-11 libcurl 8.4.0 released, coordinated with the advisory publication (advisory L127)
- 2026-11-05 advisory and policy pages captured for this trial (TRIAL1, TRIAL1-POLICY)

## Evidence

- evidence/disclosure-capture.txt sha256 327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b polarity: positive
- evidence/policy-capture.txt sha256 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102 polarity: positive
- evidence/source-excerpt.txt sha256 c6579512a8615420a077e3f068db29ae8c95147d0c8b1983302ae39bd9ef8d8e polarity: positive

## Submission

No submission performed.
