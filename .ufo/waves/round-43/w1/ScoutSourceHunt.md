# ScoutSourceHunt — round 43 disclosed-report candidates

Axes: depth:verifiability (every candidate below was fetched), coverage (six public documents a six-file claim package might be built around). No live target was requested. No tool was installed. Registry grep for `S067` and `S068` in `corpus/SOURCES.md` returned no rows. None of the URLs below appear in that registry.

## Recommend for ExecSourceCapture (S067)

Capture this URL and no other:

https://curl.se/docs/CVE-2025-9086.html

Project curl Security Advisory for CVE-2025-9086, "Out of bounds read for cookie path". First-party vendor advisory (tier A, kind docs). Fetch 2026-10-28T16:40:33Z, HTTP 200, 10455 bytes, `text/html`, 0 redirects, effective URL unchanged, sha256 `58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd`.

Publication date on the page: September 10 2025. Timeline on the page: reported to the curl project on August 11, 2025; distros@openwall contacted September 5, 2025; curl 8.16.0 released September 10 2025 around 06:00 UTC with this advisory.

Grounding, from this fetch:

- Scope text in this document: no. The word scope does not occur. Do not merge another URL into this capture.
- Severity language: yes. Served lines include `Severity: Low` and `CWE-125: Out-of-bounds Read`.
- Reward figure: the advisory records `Bug bounty: 505 USD`. That is an award on this advisory, not a standing reward ladder. See the policy contradiction below.
- Affected asset: curl / libcurl, affected versions 8.13.0 through 8.15.0, area cookies. The flaw is stated not to affect the curl command-line tool.
- Fix: yes. `Fixed-in:` links to `https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6`. The HTML does not contain the full 40-character hash. The JSON sibling does (below); do not splice it into the HTML snapshot.
- Suggested fix on the page: upgrade to 8.16.0, or apply the patch.
- Disclosure timeline: yes, the TIMELINE section.
- Repro: a four-step description is present. It uses the placeholder host `target`. It is not a live target and this seat did not request one.
- Customer data, login wall, paywall, embargo: none. The page is public HTML.

Local HTML-to-text of this saved body (same tag-strip and whitespace collapse as `capture-source.py`, not a second network fetch) is 109 lines, 3822 bytes, sha256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`. Quotes below are unique in that text and are at least 12 characters. ExecSourceCapture must re-pin line numbers on its own snapshot; a later fetch can move them.

- L82 `CWE-125: Out-of-bounds Read`
- L83 `Severity: Low`
- L84 `Bug bounty: 505 USD`
- L88 `Affected versions: curl 8.13.0 to and including 8.15.0`
- L97 `Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6`
- L103 starts `This issue was reported to the curl project on August 11, 2025.`

Use `--kind html`. The exemplar stays `claimable: false` and must carry `No submission performed`. Do not treat the 505 USD line as the program's reward policy.

Policy contradiction, separate document, not part of S067: `https://curl.se/dev/vuln-disclosure.html` fetched 2026-10-28T16:42:47Z, HTTP 200, 26500 bytes, 0 redirects, sha256 `91462d3511134e869e9afbe243d4dce564f5b373cd4a03066082702206df8a42`. Served line 68 reads: `There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.` The same page defines Low, Medium, High and Critical and says low or medium reports restricted to releases older than three years are out of scope (served line 209). No publication date was visible in that body. The advisory's relative disclosure link is `/dev/vuln-disclosure.html`. The guessed `/docs/vuln-disclosure.html` returned HTTP 404, 8017 bytes, at 2026-10-28T16:41:50Z.

JSON sibling, same advisory, do not capture as S067: `https://curl.se/docs/CVE-2025-9086.json` fetched 2026-10-28T16:42:47Z, HTTP 200, 2468 bytes, `application/json`, sha256 `b69b88d2bc821e16d186f968f59b2612c183e14c7825416dba778da8cd99da76`. It records `published` `2025-09-10T08:00:00.00Z`, `severity` `Low`, award `505` `USD`, and the full fix commit `c6ae07c6a541e0e96d0040afb62b45dd37711300` (the HTML hash is a prefix of this one). It has no timeline prose. `modified` is `2026-10-24T23:17:46.00Z`, so the JSON moves independently of the HTML permalink.

## Reject for S068

https://github.com/advisories/GHSA-v676-f8gm-92r9

GitHub Advisory Database page for the same CVE. Fetch 2026-10-28T16:41:46Z, HTTP 200, 141796 bytes, `text/html; charset=utf-8`, 0 redirects, sha256 `f238e2fe9492194947bb3ecca7130d83661de1b4030b4dab9ad282adf524b497`.

Publication dates on the page: published to the GitHub Advisory Database `2025-09-12T06:30:26Z` (served line 388); a separate "Published by the National Vulnerability Database" stamp at `2025-09-12T06:15:44Z` (served line 475). Updated `2026-06-02T15:32:54Z` (served line 392).

Located quote: `No package listed` is contiguous on served line 408.

Reason: this is an Unreviewed advisory (served lines 372 and 384) that republishes NVD's view of CVE-2025-9086. It labels the issue High severity (served line 380) with score 7.5 (served line 510) and vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` (served line 632). Affected versions and patched versions are both `Unknown` (served lines 417 and 423). A search of the body for the vendor fix prefix `c6ae07c6` returned no match. The page is not curl's advisory; it links to the curl page as a reference. A claim package grounded on it would contradict the vendor severity and could not name a fixed version or a fix commit.

Flip: re-open only if this GHSA is marked reviewed, names the curl package, and records severity Low plus fixed version 8.16.0 or commit c6ae07c6a541e0e96d0040afb62b45dd37711300.

No login wall and no paywall. The disqualifier is the document, not access. Do not capture it as a lane snapshot.

## Other screened candidates

### ZDI-26-811

https://www.zerodayinitiative.com/advisories/ZDI-26-811/

Trend Micro Zero Day Initiative advisory, MailEnable `parseObjectResponse` XML external entity information disclosure. Fetch 2026-10-28T16:40:34Z, HTTP 200, 26851 bytes, `text/html; charset=utf-8`, 0 redirects, sha256 `30403b48a88c0621a21219b47cb77b2d0773459b77cd642c05fc21155e71d7f8`.

Published 2026-10-27 (reported to vendor 2026-09-18; coordinated public release 2026-10-27; advisory updated 2026-10-27). CVE-2026-114552. CVSS 6.5, vector `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`. Affected product MailEnable. Additional details say fixed in version 10.60 and link a vendor release-notes file. This seat did not fetch that vendor host.

Scope text: no. Severity language: yes (CVSS). Fix commit: no, only a version. Reward language: no. Vulnerability details are the coordinator template (authentication required, XXE, service-account disclosure), not a program scope excerpt. Usable as a coordinator bulletin, weaker than the curl advisory for a claim package that needs a fix commit and the project's own severity sentence. Not paywalled, not a login wall, no customer data.

### OSS-Fuzz OSV-2025-17

https://raw.githubusercontent.com/google/oss-fuzz-vulns/main/vulns/opencv/OSV-2025-17.yaml

First-party Google OSS-Fuzz vulnerability record for OpenCV. Fetch 2026-10-28T16:41:46Z, HTTP 200, 1078 bytes, `text/plain; charset=utf-8`, 0 redirects, sha256 `f9dd060ed2d79b2640b3db70193618540df0fa56a35f04a4e170a8e5cee19490`.

`published` and `modified` `2025-01-08T00:14:02Z`. `summary` Heap-buffer-overflow in `cv::PngDecoder::readHeader`. `ecosystem_specific.severity` MEDIUM. Package `opencv`, ecosystem OSS-Fuzz. Introduced commit `d39aae6bdfc1a45553e1426334a9c72848354261`. Fixed commit `f00814e38db556ad7a31e6dee203e41eea48e7a6`. Version named `4.11.0`. The details name crash type and crash state and point at a Chromium OSS-Fuzz issue id. This seat did not fetch the issue tracker.

Scope text: no. Reward language: no. Severity language: the single token MEDIUM, not a program ladder. Fix commit: yes. Clean to capture, but a claim package cannot take a scope excerpt or a reward sentence from it. Also adjacent to rejected registry row S065, which rejected the OSV schema; this file is one OSV record, not that schema, and it should not be the mined row while that rejection stands. Not paywalled, not a login wall, no customer data.

### HackerOne report 3294999

https://hackerone.com/reports/3294999

The curl advisory calls this the original report. Fetch 2026-10-28T16:41:45Z, HTTP 200, 3829 bytes, `text/html; charset=utf-8`, 0 redirects, sha256 `82b9c983a724ef5fd46dfe94282555abda956249d0ff6eb0398d29b144dbb892`.

The body is a signed-out application shell (`class` contains `signed-out`; the root element is empty). A noscript block says JavaScript is required. The report text is not in the response. `og:title` says the report is disclosed and names CVE-2025-9086. `og:description` is a truncated snippet only. No publication date is in the fetched body. No severity field, no asset field, no timeline, and no fix commit are in the fetched body.

A second disclosed-report URL, `https://hackerone.com/reports/3176981`, fetched 2026-10-28T16:41:46Z, returned the same shell: HTTP 200, 3779 bytes, sha256 `799fa18648892b669486abf5acfffe777c499f91d2d6414b42a57ff0d6c18189`. Same disqualifier, so HackerOne disclosed-report URLs are not capturable with the instrument user agent.

Disqualifiers: the disclosed report is not in the bytes; a capture would bind a JavaScript shell and a session token, not the report. Not a paywall in the sense of a payment page. No customer data was present. No live target was fetched.

### Intigriti Dashlane program page

https://app.intigriti.com/programs/dashlane/dashlanevulnerabilitydisclosureprogram

Fetch 2026-10-28T16:41:47Z. First hop HTTP 302 to `/programs/dashlane/dashlanevulnerabilitydisclosureprogram/detail`, then HTTP 200, 462202 bytes, `text/html;charset=UTF-8`, sha256 `513f740238c038a4d076187b2007f94bcc70bbf9c84ab4c3f17c399f10f4ad49`.

This is a program description, not a disclosed finding. The body invites researchers to report vulnerabilities in Dashlane-owned services and names live production hosts. This seat did not request any of those hosts. No CVE, no fix commit, no severity of a finding, and no finding publication date.

Disqualifiers: not a disclosed report; building a claim from it would require a live target; the page is a large application shell around a program policy. Scope prose is present, which is why it was screened, and that is also why it loses: scope without a disclosed finding cannot be the exemplar's report.

## Search log

Question: which one public first-party disclosed report can ground a six-file claim package, and which screened candidate is the reject.

Where: curl.se advisory, its JSON sibling, and its disclosure policy; one ZDI advisory; the GitHub Advisory Database page for the same CVE; two HackerOne report URLs; one raw file in `google/oss-fuzz-vulns`; one Intigriti program page.

Date: 2026-10-28. Identified 6 candidate documents, screened 6, included 1 (the curl HTML advisory), excluded 5. Supporting fetches that are not candidates: the JSON sibling, the disclosure policy, a 404 on the wrong disclosure path, and the second HackerOne shell. The ZDI published-advisory index was fetched only to confirm the advisory URL (HTTP 200, 2551868 bytes) and is not a candidate.

Exclusion reasons: ZDI-26-811 has no fix commit and no scope or reward sentence; OSV-2025-17 has no scope or reward sentence and sits next to rejected S065; GHSA-v676-f8gm-92r9 is the designated reject; HackerOne 3294999 does not contain the report; the Intigriti page is a program policy that names live hosts.

Stop: the curl HTML advisory is small, first-party, and already carries severity, an award figure, affected versions, a fix URL, and a timeline. No other page put a scope excerpt inside that same document.

## Receipt

Disk guard before the fetches, 2026-10-28T16:40:08Z: `/fast/scratch/hyaku` 25% used, 605.0G free. Scratch was `/fast/scratch/hyaku/kasegi-r43/ScoutSourceHunt` and was removed after this file was written.

User agent on every fetch: `kasegi-shokunin/1.0`. Command shape: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`.

```
name=curl9086 utc=2026-10-28T16:40:33Z http=200 bytes=10455 ctype=text/html redir=0 url_effective=https://curl.se/docs/CVE-2025-9086.html time=0.438749
name=zdi811 utc=2026-10-28T16:40:34Z http=200 bytes=26851 ctype=text/html; charset=utf-8 redir=0 url_effective=https://www.zerodayinitiative.com/advisories/ZDI-26-811/ time=1.746017
name=zdiindex utc=2026-10-28T16:40:35Z http=200 bytes=2551868 ctype=text/html; charset=utf-8 redir=0 url_effective=https://www.zerodayinitiative.com/advisories/published/ time=2.927607
name=h1curl utc=2026-10-28T16:41:45Z http=200 bytes=3829 ctype=text/html; charset=utf-8 redir=0 url_effective=https://hackerone.com/reports/3294999 time=0.283204
name=h1mainwp utc=2026-10-28T16:41:46Z http=200 bytes=3779 ctype=text/html; charset=utf-8 redir=0 url_effective=https://hackerone.com/reports/3176981 time=0.306157
name=ghsa utc=2026-10-28T16:41:46Z http=200 bytes=141796 ctype=text/html; charset=utf-8 redir=0 url_effective=https://github.com/advisories/GHSA-v676-f8gm-92r9 time=0.405890
name=ossfuzz utc=2026-10-28T16:41:46Z http=200 bytes=1078 ctype=text/plain; charset=utf-8 redir=0 url_effective=https://raw.githubusercontent.com/google/oss-fuzz-vulns/main/vulns/opencv/OSV-2025-17.yaml time=0.298847
name=intigriti utc=2026-10-28T16:41:47Z http=200 bytes=462202 ctype=text/html;charset=UTF-8 redir=1 url_effective=https://app.intigriti.com/programs/dashlane/dashlanevulnerabilitydisclosureprogram/detail time=3.723888
name=curldisc utc=2026-10-28T16:41:50Z http=404 bytes=8017 ctype=text/html redir=0 url_effective=https://curl.se/docs/vuln-disclosure.html time=0.452768
name=curlbounty utc=2026-10-28T16:42:47Z http=200 bytes=26500 ctype=text/html redir=0 url_effective=https://curl.se/dev/vuln-disclosure.html
name=curljson utc=2026-10-28T16:42:47Z http=200 bytes=2468 ctype=application/json redir=0 url_effective=https://curl.se/docs/CVE-2025-9086.json
```

Intigriti first status line was `HTTP/2 302` with `location: /programs/dashlane/dashlanevulnerabilitydisclosureprogram/detail`, then `HTTP/2 200`. Every other response status line was HTTP 200 except `curldisc`, which was `HTTP/2 404`.

Body sha256:

```
58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd  curl9086.body
30403b48a88c0621a21219b47cb77b2d0773459b77cd642c05fc21155e71d7f8  zdi811.body
172bde7fc65f99064b2fdad7978588af04de188bf06692a3cee68fb8b72eb2be  zdiindex.body
82b9c983a724ef5fd46dfe94282555abda956249d0ff6eb0398d29b144dbb892  h1curl.body
799fa18648892b669486abf5acfffe777c499f91d2d6414b42a57ff0d6c18189  h1mainwp.body
f238e2fe9492194947bb3ecca7130d83661de1b4030b4dab9ad282adf524b497  ghsa.body
f9dd060ed2d79b2640b3db70193618540df0fa56a35f04a4e170a8e5cee19490  ossfuzz.body
513f740238c038a4d076187b2007f94bcc70bbf9c84ab4c3f17c399f10f4ad49  intigriti.body
f028f4849d6e35cff7cc6e1d8abb54663c0418ca8d6736e826a51efdcadaf296  curldisc.body
91462d3511134e869e9afbe243d4dce564f5b373cd4a03066082702206df8a42  curlbounty.body
b69b88d2bc821e16d186f968f59b2612c183e14c7825416dba778da8cd99da76  curljson.body
```

`capture-source.py` was not run, because it would have fetched again under a different user agent. The 109-line normalization above was applied to the saved curl HTML only.

## Reconciliation (appended)

ExecSourceCapture's landed snapshot now matches this recommendation. Re-read after their overwrite notice: `ExecSourceCapture.manifest.json` url is `https://curl.se/docs/CVE-2025-9086.html`, fetched 2026-10-28T16:46:34Z, raw sha256 `58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd` (10455 bytes), normalized sha256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, 109 lines, 3822 bytes. Q2-Q6 anchors are L82, L84, L88, L97, L103, the same lines as the local normalization above. Their earlier CVE-2023-38545 draft was discarded by them.

`ExecRegistryRows.rows.txt` was rewritten after that re-read. A later read shows S067 is CVE-2025-9086 with capture sha256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, and S068 is GHSA-v676-f8gm-92r9, not MFSA 2026-99. Their GHSA fetch was not byte-stable (141795 and 141796 raw bytes), so their row pins the normalized text (191 lines, sha256 `530cbcf9925b082f9effea7bbc5e96650949794d80893d7ac8ec5e289b4c97e6`) where `No package listed` is L75. The served-line 408 quote above is this seat's 141796-byte raw HTML, the same phrase, not a second document. This seat did not edit their file.
