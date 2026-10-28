# libcurl SOCKS5 heap buffer overflow (CVE-2023-38545) — claim-package exemplar

Program: curl (project curl / libcurl)
Official advisory URL: https://curl.se/docs/CVE-2023-38545.html
Original public report: https://hackerone.com/reports/2187833

This is the round-43 worked exemplar for the six-file claim-package contract. It is
built from one public, already-disclosed vendor advisory; it records no new
finding and no customer data. `status.json` keeps `claimable` false, and
`claim_checklist.md` lists the operator-gated steps. No submission was made for
this package.

## Scope excerpt

Source URL: https://curl.se/docs/CVE-2023-38545.html (Project curl Security Advisory, October 11 2023)
observed_at: 2026-10-28T16:39:59Z
content sha256: 9103704c553579828d1313ca7b9eaedba270a0160e39484e280001629d037cc8
  (evidence/source-excerpt.txt: capture lines 100-114 with a three-line provenance
  header; the full captured document is evidence/source-capture.txt, sha256
  327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b, 6446 bytes,
  131 lines)

Verbatim lines from the capture, read at 2026-10-28T16:39:59Z: the flaw statement
is capture line 71, carried by the full capture artifact; the scope, severity and
reward lines are capture lines 100, 101, 108, 112 and 113, which lie inside the
excerpt artifact above.

```
This flaw makes curl overflow a heap based buffer in the SOCKS5 proxy handshake.
CWE-122: Heap-based Buffer Overflow
Severity: High
Bug bounty: 4660 USD
Affected versions: libcurl 7.69.0 to and including 8.3.0
Not affected versions: libcurl < 7.69.0 and >= 8.4.0
```

The first line is the discloser's flaw statement. The remaining lines are its own
classification, severity and reward language and its affected-version
determination, which is the scope authority this package quotes. Every line above
was copied from the captured bytes at the line number given; nothing is retyped
from memory.

## Vulnerability class

CWE-122: Heap-based Buffer Overflow in the SOCKS5 proxy handshake. The local
variable that chooses whether the proxy resolves the hostname can take the wrong
value during a slow handshake, and a hostname longer than the download buffer is
then copied into that heap buffer instead of only the resolved address.

## Reproduction (isolated lab only)

The advisory gives the conditions, not a weaponised payload: a client built from
libcurl 7.69.0 through 8.3.0, SOCKS5 with remote hostname resolution
(`CURLPROXY_SOCKS5_HOSTNAME`, a `socks5h://` proxy URL, or the matching proxy
environment variable), a download buffer of 65540 bytes or less, and a handshake
slow enough for the state-machine bug to fire.

1. Build an affected release (libcurl 8.3.0) with sanitizers in a disposable tree.
2. Run a SOCKS5 listener on loopback only, with an artificial handshake delay.
3. Point the build at that listener through `socks5h://` and request a hostname
   longer than the configured download buffer.
4. Read the sanitizer report on the heap-based download buffer.

No external host is contacted and no account material is used. Producing this
package did not execute these steps: the captured advisory is the evidence, and
the package is a format fixture.

## Impact

The discloser's own language: "Severity: High", "CWE-122: Heap-based Buffer
Overflow", Area: SOCKS5, and "Bug bounty: 4660 USD". The overflow writes
attacker-influenced hostname bytes past a heap download buffer. The advisory's
follow-up variant lets a crafted hostname complete the handshake so that the
SOCKS server connects and carries data on the client's connection; the discloser
limits that variant because curl does not allow control characters or null in the
hostname.

## Affected asset

libcurl, and the curl tool where its download buffer is under 65541 bytes:
versions 7.69.0 through 8.3.0 inclusive. The bug was introduced by
https://github.com/curl/curl/commit/4a4b63daaa and fixed in 8.4.0 by
https://github.com/curl/curl/commit/fb4415d8aee6c1.

## Suggested fix

Upgrade to curl 8.4.0, which returns an error for a too-long name instead of
switching to local resolve mode, or apply the fixed-in patch to the local
version. Interim mitigations from the advisory: do not use
`CURLPROXY_SOCKS5_HOSTNAME` proxies, and do not set a proxy environment variable
to `socks5h://`.

## Disclosure timeline

- 2023-09-30 — reported to the curl project.
- 2023-10-03 — distros@openwall contacted.
- 2023-10-11 — libcurl 8.4.0 released, coordinated with this advisory.
- 2026-10-25 11:18:20 GMT — advisory page Last-Modified at capture time.
- 2026-10-28T16:39:59Z — advisory captured for this package.

No submission performed
