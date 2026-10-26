# ExecCsafStatus — round-38 receipt

Seat: ExecCsafStatus (leaf, no subagent dispatch). Round: kasegi-shokunin 38, milestone round-38.
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only writes: this receipt under the wave dir; all other work in scratch).
Base commit: `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`. Observed lane HEAD at read time: `700153593eb586c70a6499c8ca225ee4d673bc9b` (`git -C … rev-parse HEAD`, read-only).
Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecCsafStatus` (removed before yield).
Tools installed/upgraded: none (curl, python3, and the lane's own `corpus/instruments/capture-source.py` sufficed).
Fetches used `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; the lane instrument uses its own capture UA (recorded below). All times UTC, 2026-10-26.

## 1. Fetch ledger

| # | URL | HTTP | bytes | fetched UTC | sha256 of fetched body |
|---|---|---|---|---|---|
| 1 | https://docs.oasis-open.org/csaf/csaf/ | 200 | 392 | 18:27:16Z | `64a9419639f60bd14d22b233b63743ef1ce81a9d70a1f5a875195a5c486ec94b` |
| 2 | https://www.oasis-open.org/committees/csaf/ | 200 | 145837 | 18:27:17Z | `0e238087fac71a0955be393b89d331f4f1ed871b83746945ad37d27eddb6145c` |
| 3 | https://github.com/oasis-tcs/csaf | 200 | 296154 | 18:27:19Z | `c38cbefdcfb9ca21afbfbe4df86b1fbb0fc5270c79e096b68b69eda5bab09e72` |
| 4 | https://docs.oasis-open.org/csaf/csaf/v2.0/ | 200 | 1704 | 18:27:28Z | `afdfdb1ca202d6ba0a900b821af8270789ab8eb665684d1821ab1ec5ea5be3aa` |
| 5 | https://docs.oasis-open.org/csaf/csaf/v2.1/ | 200 | 1097 | 18:27:29Z | `5e59949c479ca03097be81259cb5bf168a857562991c73be3c826e7822f03775` |
| 6 | https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html | 200 | 1231332 | 18:27:41Z | `fdb4bf015c75f01269c1ba346912fd558e8a168b607279b951b1fe5335f366b0` |
| 7 | https://docs.oasis-open.org/csaf/csaf/v2.1/csd04/ | 200 | 1220 | 18:27:41Z | `749f9beef04b3a884f828fb7268859ceccf5c3418fd8f4cd0b2ae24d0046f161` |
| 8 | https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html | 200 | 25631 | 18:27:48Z | `05ce174dec889a785a8dce287d66cd0f757910336193d0b71453b5143b9f51de` |
| 9 | https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/ | 200 | 817 | 18:27:48Z | `f45e8200fc6fa07a4a5f479b598a79be1e19ad3216fc5b41160e6eb46c09337a` |
| 10 | https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/os/csaf-v2.0-errata01-os.html | 200 | 25631 | 18:29:02Z | `05ce174dec889a785a8dce287d66cd0f757910336193d0b71453b5143b9f51de` |
| 11 | https://docs.oasis-open.org/csaf/csaf/v2.1/cs/ | 404 | 41334 | 18:29:02Z | error page (no CS artifact) |
| 12 | https://docs.oasis-open.org/csaf/csaf/v2.1/os/ | 404 | 41334 | 18:29:03Z | error page (no OS artifact) |
| 13 | https://api.github.com/repos/oasis-tcs/csaf/tags | 200 | 8121 | 18:28:19Z | `00f8543956d30a8ce509fe049d41cb6d552c1046a56040acb0b23c3a99e9f0e2` |
| 14 | https://raw.githubusercontent.com/oasis-tcs/csaf/master/README.md | 200 | 3935 | 18:28:19Z | `8a68565657d109f24cb10007b448ef12a6a80c9f862d5d9ffca67d66c0e7abf7` |
| 15 | https://docs.oasis-open.org/csaf/csaf/v2.1/csd04/csaf-v2.1-csd04-public-review-metadata.html | 200 | 9477 | 18:30:18Z | `b97c5c896dfa037e569d5cb955f303c403a88571f7ff464cf0dbeac500d1be3b` |
| 16 | https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html (curl) | 200 | 414858 | 18:27:20Z | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| 17 | same URL, `capture-source.py` run 1 | 200 | fetched_bytes=415225; snapshot 272441 | 18:29:19Z | snapshot `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` |
| 18 | same URL, `capture-source.py` run 2 | 200 | fetched_bytes=415225; snapshot 272441 | 18:29:29Z | snapshot `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` |

Command actually run for rows 1–16 (loop, one URL per row; output printed status/bytes/time):

```
for pair in "listing|https://docs.oasis-open.org/csaf/csaf/" ... ; do
  code=$(curl -sS -L --max-time 90 -A "$UA" -o "$name.html" -w '%{http_code}' "$url")
  echo "$name $url status=$code bytes=$(stat -c%s "$name.html") fetched_utc=$ts"
done
```

Rows 17–18:

```
$ TMPDIR=$S python3 corpus/instruments/capture-source.py --id S055 \
    --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html \
    --out "$S/S055-capture-equivalent.txt"
S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:29:19Z out=/fast/scratch/hyaku/kasegi-r38/ExecCsafStatus/S055-capture-equivalent.txt
S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:29:29Z out=/fast/scratch/hyaku/kasegi-r38/ExecCsafStatus/S055-capture-run2.txt
```

Raw-body variance note: the curl fetch (row 16) and the instrument fetches (rows 17–18) differ by 367 bytes; `cmp` locates the first difference at byte 414841, where the instrument body carries a Cloudflare-injected `<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/...">` tag that the curl body lacks. `capture-source.py` strips `<script>`/`<style>` before converting, so the normalized snapshot is byte-stable across two fetches (both `63c8ad…`). The S055 manifest must bind the snapshot digest (`63c8ad…`), not a raw-body digest.

Normalization: `capture-source.py`'s `html_to_text` (script/style removal, newline at block closes and `<br>`, tag strip, entity decode, whitespace collapse, blank-line drop). That snapshot is 5,146 non-empty lines. An independent normalizer used for the first pass also produced 5,146 lines and the same line numbers for every quote below; the instrument output is authoritative for capture text.

## 2. Fact F1 — CSAF v2.0 is an OASIS Standard dated 18 November 2022

Located quotes from the S055 URL (`https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`), lines in the `63c8ad…` snapshot:

```
L1  Common Security Advisory Framework Version 2.0
L2  Common Security Advisory Framework Version 2.0
L3  OASIS Standard
L4  18 November 2022
```

```
L43 Status:
L44 This document was last revised or approved by the membership of OASIS on the above date. The level of approval is also listed above. Check the "Latest stage" location noted above for possible later revisions of this document. Any other numbered Versions and other technical work produced by the Technical Committee (TC) are listed at https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=csaf#technical.
```

```
L48 Citation format:
L49 When referencing this specification the following citation format should be used:
L50 [csaf-v2.0]
L51 Common Security Advisory Framework Version 2.0. Edited by Langley Rock, Stefan Hagen, and Thomas Schmidt. 18 November 2022. OASIS Standard. https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html.
```

Corroboration on the TC page (`https://www.oasis-open.org/committees/csaf/`, normalized 149 lines):

```
L51 Common Security Advisory Framework Version 2.0 OASIS Standard is now published. For details, see the announcement.
L81 Common Security Advisory Framework Version 2.0. Edited by Langley Rock, Stefan Hagen, and Thomas Schmidt. 18 November 2022. OASIS Standard. https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html.
```

Directory corroboration (`https://docs.oasis-open.org/csaf/csaf/v2.0/`):

```
<a href="os/">os/</a>   18-Nov-2022 17:00   -
```

GitHub tag corroboration (row 13): `csaf-2.0-os` is present in the tag list.

Conclusion F1: the S055 artifact is the OASIS Standard document of CSAF v2.0, document date 18 November 2022. The approval date is the document date the header and the TC citation both print; the TC's press-release announcement is a separate, later news item (page line 52; press coverage line 102 dated 21 November 2022) and is not the standard's date.

## 3. Fact F2 — the v2.0 OS document is not the last v2.0 artifact; Errata 01 (26 January 2024) is separate

The OS header's own "Latest stage" block points away from the OS text:

```
L13 Latest stage:
L14 https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.md (Authoritative)
L15 https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html
L16 https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.pdf
```

Fetching that Latest-stage URL (row 8) returns bytes byte-identical (sha256 `05ce174d…`) to the Errata 01 OS document (row 10), whose normalized head is:

```
L1 Common Security Advisory Framework Version 2.0 Errata 01
L2 Common
L3 Security Advisory Framework Version 2.0 Errata 01
L4 OASIS Approved Errata
L5 26 January 2024
```

Directory evidence (`https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/`): `os/` 26-Jan-2024 17:00 and `csd01/` 12-Feb-2024 20:42. TC page citation:

```
L80 Common Security Advisory Framework Version 2.0 Errata 01. Edited by Langley Rock, Stefan Hagen, and Thomas Schmidt. 26 January 2024. OASIS Approved Errata. https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/os/csaf-v2.0-errata01-os.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/csaf-v2.0-errata01.html.
```

Errata text scope check: `grep -c -i -E 'product_status|justification|flags|VEX'` over the 359-line Errata 01 text returns `0`, so Errata 01 does not restate the VEX section or the flag labels the F21 entry cites; scoping the row to the OS document loses no VEX text from that errata.

Conclusion F2: the OS document (18 November 2022) is the artifact at the S055 URL, but OASIS's "Latest stage" link for v2.0 serves the Approved Errata 01 text (26 January 2024). A scope cell must therefore bind to `csaf-v2.0-os.html` and must not say "latest"/"current" or imply the errata is included.

## 4. Fact F3 — CSAF v2.1 exists as Committee Specification Draft 04 (21 October 2026), in public review; no CS and no OS as of 2026-10-26

Directory listing (`https://docs.oasis-open.org/csaf/csaf/v2.1/`, normalized):

```
Index of /csaf/csaf/v2.1/
../
csaf-v2.1.html 21-Oct-2026 17:00 1M
csaf-v2.1.md 21-Oct-2026 17:00 835K
csaf-v2.1.pdf 21-Oct-2026 17:00 4M
csd01/ 28-May-2025 17:00 -
csd02/ 25-Feb-2026 17:00 -
csd03/ 11-Sep-2026 17:00 -
csd04/ 21-Oct-2026 17:00 -
schema/ 21-Oct-2026 17:00 -
```

There is no `cs/` and no `os/` directory; direct probes return 404: `https://docs.oasis-open.org/csaf/csaf/v2.1/cs/` → 404, 41334 bytes (row 11); `https://docs.oasis-open.org/csaf/csaf/v2.1/os/` → 404, 41334 bytes (row 12). Top-level `csaf/csaf/` listing shows only `v2.0/` (12-Feb-2024) and `v2.1/` (21-Oct-2026).

The v2.1 latest-stage document header (`https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html`, normalized 12,240 lines):

```
L1 Common Security Advisory Framework Version 2.1
L2 Common Security Advisory Framework Version 2.1
L3 Committee Specification Draft 04
L4 21 October 2026
```

```
L13 Latest stage
L14 https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.md (Authoritative)
L15 https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html
L16 https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.pdf
```

```
L65 Common Security Advisory Framework Version 2.1. Edited by Stefan Hagen and Thomas Schmidt. 21 October 2026. OASIS Committee Specification Draft 04. https://docs.oasis-open.org/csaf/csaf/v2.1/csd04/csaf-v2.1-csd04.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html.
```

TC page citation (`https://www.oasis-open.org/committees/csaf/`, normalized L76):

```
L76 Common Security Advisory Framework Version 2.1. Edited by Stefan Hagen and Thomas Schmidt. 21 October 2026. OASIS Committee Specification Draft 04. https://docs.oasis-open.org/csaf/csaf/v2.1/csd04/csaf-v2.1-csd04.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html.
```

Stage detail: CSD 04 is in a 15-day public review (metadata page, normalized 89 lines):

```
L3  Public Review
L4  of Committee Specification Draft 04
L5  Starts 23 October 2026
...
L19 The Committee Specification Draft is now available for a 15-day
L20 public review.
L21 Public Review Dates:
L22 The public review starts 23 October 2026 at 00:00 UTC and ends 6 November 2026
L23 at 23:59 UTC.
...
L49 Timeline Summary:
L50 Committee Specification Draft 04 (CSD04) approved for public review
L51 21 October 2026, 15-day review (the TC Process minimum for a subsequent
L52 review): https://github.com/oasis-tcs/csaf/issues/1708.
L53 Published under standing rule #SR1BP, Editor CSD Publication Right
...
L56 15-day public review 04 to be opened on 23 October 2026 and closed
L57 on 6 November 2026.
```

GitHub tags (row 13) list the v2.1 draft tags and the v2.0 tag, and no v2.1 CS/OS tag:

```
csaf-2.1-csd-04-20261021-rc1
csaf-2.1-csd-03-20260911-rc1
csaf-2.1-csd-02-20260225-rc1
csaf-2.1-csd-01-20250528-rc2
csaf-2.1-csd-01-20250528-rc1
csaf-2.0-os
csaf-2.0-errata-01-csd-01-20231208-rc1
csaf-2.0-errata-01-starter
```

Conclusion F3: as of 2026-10-26, v2.1 exists only at Committee Specification Draft 04 (dated 21 October 2026), under a public review running 23 October–6 November 2026. It is not a Committee Specification and not an OASIS Standard.

## 5. Fact F4 — the nouns the scope cell uses are the document's own terms

```
L1756 Label of the flag (label) of value type string and enum specifies the machine readable label. Valid enum values are:
L1757 component_not_present
L1758 inline_mitigations_already_exist
L1759 vulnerable_code_cannot_be_controlled_by_adversary
L1760 vulnerable_code_not_in_execute_path
L1761 vulnerable_code_not_present
L1762 The given values reflect the VEX not affected justifications. See [VEX-Justification] for more details. The values MUST be used as follows:
```

```
L1855 Product status (product_status) of value type object with 1 or more properties contains different lists of product_ids which provide details on the status of the referenced product related to the current vulnerability. The eight defined properties are First affected (first_affected), First fixed (first_fixed), Fixed (fixed), Known affected (known_affected), Known not affected (known_not_affected), Last affected (last_affected), Recommended (recommended), and Under investigation (under_investigation) are all of value type Products (products_t).
```

```
L2134 4.5 Profile 5: VEX
L2135 This profile SHOULD be used to provide information of the "Vulnerability Exploitability eXchange". The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability. See [VEX] for details.
...
L2152 /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats. For the latter one, the category value for such a statement MUST be impact and the details field SHALL contain a a description why the vulnerability cannot be exploited.
```

So "product_status categories" and "machine-readable not-affected justification flags" are supported as the document's own vocabulary (eight product-status properties; five `label` enum values whose sentence says they "reflect the VEX not affected justifications"; the VEX profile requires the impact statement for `known_not_affected`).

## DELIVERABLE

Exact `scope` cell wording for the S055 row. One line; 318 bytes including the trailing newline; sha256 `0d7892e56de55dca981049f6233351b84d5d24a80da76226891e0250b52de1e2`.

```text
CSAF v2.0 OASIS Standard (18 November 2022) text at csaf-v2.0-os.html: the VEX profile's product_status categories and the machine-readable not-affected justification flags, scoped to that text and not to the separate Errata 01 (26 January 2024) or to the v2.1 Committee Specification Drafts (CSD 04, 21 October 2026)
```

Why this wording, against the S051 precedent:

- S051's row (SOURCES.md:57) names the version in its scope cell — "Immunefi's own Web3 severity classification system v2.2 as this page states it: …" — and its companion registry-changes bullet at SOURCES.md:110 records the no-recency rule: "S051 scope recorded without a recency claim: no cell says `latest` or `current`, because the index fetch of 2026-10-26 (no committed capture; observation only) marks v2.3 and v2.2 both Currently in Use; S051 therefore states v2.2 and carries a `90d` cadence rather than a recency claim, and no other cell or entry claim rests on that observation."
- The proposed S055 cell mirrors that shape: it states the version (`v2.0`) and its stage-with-date (`OASIS Standard (18 November 2022)`), which F1 supports, and binds the subject to the OS document (`text at csaf-v2.0-os.html`), which F2 requires because the v2.0 "Latest stage" URL serves Errata 01 bytes.
- The two exclusions are dated facts, not recency claims: Errata 01 (26 January 2024) is a separate approved-errata document (F2); the v2.1 Committee Specification Drafts (CSD 04, 21 October 2026) are drafts (F3). Neither sentence says which artifact is newest, current, or in force.
- Token audit: `grep -c -i -E 'latest|current|newest|most recent|up to date|in force|authoritative|today|now|as of|still'` over the cell returns `0`; `grep -c '|'` returns `0` (safe inside a markdown table cell).

## Row-column context (recommendation, not part of the deliverable)

The frozen claim fixes the row's source and URL. For the remaining cells, the facts above give:

- `source`: `Common Security Advisory Framework (CSAF) v2.0 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`
- `kind`: `spec`; `tier`: `A`; `status`: `mined`; `opened`: `2026-10-26`
- `recheck`: `180d` recommended. The OS text and its approved errata are frozen artifacts, unlike S051's live vendor page that warranted `90d`. If the scribe prefers to track the v2.1 review clock (ends 6 November 2026), `90d` is also defensible; either cadence is a scheduling choice, not a recency claim.
- `used-by`: `corpus/knowledge/csaf-vex-product-status-and-justifications.md`

If a registry-changes bullet is written for S055, the dated stage facts to record are: v2.0 OASIS Standard 18 November 2022; v2.0 Approved Errata 01 26 January 2024 at a separate URL; v2.1 CSD 04 dated 21 October 2026 under public review 23 October–6 November 2026, with no v2.1 CS or OS artifact (404 on `/v2.1/cs/` and `/v2.1/os/`).

## Risks and caveats

1. Do not bind a raw-body digest for S055. Cloudflare intermittently injects a beacon `<script>` into the HTML response (414858 vs 415225 bytes observed four minutes apart); the normalized snapshot is stable at `63c8ad…` because the instrument strips scripts. The manifest should pin the snapshot digest and the quoted lines in the snapshot, not a Content-Length.
2. Line numbers quoted above are in the `63c8ad…` snapshot of the OS URL. If the S055 capture is made from a different URL — in particular `https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html`, which serves Errata 01 bytes (sha256 `05ce174d…`, only 359 normalized lines) — the digest and every anchor line shift. Claims fix the OS URL; keep it.
3. The v2.1 public review closes 6 November 2026. After it, v2.1 may advance to Committee Specification; any statement about v2.1's stage after that date needs a fresh fetch. The proposed cell only dates CSD 04 and does not assert it is the final draft.
4. The OS header's "Latest stage" block (L13–L16) is stale relative to the errata-01 document now served there. Do not quote the OS header's Latest-stage URL as if it were the OS text.
5. `csaf-v2.0-os.html` remains served with HTTP 200 and a stable normalized snapshot at 2026-10-26 18:29Z; the last-modified header on the response was `Sun, 05 Apr 2026 13:17:09 GMT` (CDN metadata). No claim here rests on that header.

## Writes, cleanup, and read-only discipline

- Wrote only this receipt: `.ufo/waves/round-38/wave1/ExecCsafStatus.md`.
- Scratch `/fast/scratch/hyaku/kasegi-r38/ExecCsafStatus` was removed after copying the receipt; verified absent (`test -e` false) at yield.
- No lane-file edits, no mutating git/jj, no fleet-root or shokuknow writes, no service restarts, no pacman transactions, no tool installs.
