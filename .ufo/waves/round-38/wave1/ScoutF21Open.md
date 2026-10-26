# ScoutF21Open — S055 source-opening receipt (round 38, F21, receipt only)

No deliverable file; no lane file touched. Scratch /fast/scratch/hyaku/kasegi-r38/ScoutF21Open/ removed before yield. Tools installed: none.

## 1. Fetch record (instrument UA `kasegi-shokunin/1.0`, access date 2026-10-26)
- URL: https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html (final URL identical, redirects=0)
- curl -sS -L --max-time 90 -A kasegi-shokunin/1.0, fetched 2026-10-26T18:35:44Z: **HTTP 200**, content-type `text/html`, 414858 bytes (CRLF), sha256 fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b. Headers: `date: Mon, 26 Oct 2026 18:35:44 GMT`, `last-modified: Sun, 05 Apr 2026 13:17:09 GMT`, `cache-control: public, max-age=31536000, immutable`, `server: cloudflare` (via CloudFront), no content-length (HTTP/2).
- `capture-source.py --id S055 --url <URL> --out <scratch>/S055.txt --kind html` (same minute) printed:
  `S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:35:44Z`; snapshot = 5146 lines, 272441 bytes.
- fetched_bytes differs between curl (414858) and the tool's urllib fetch (415225): the urllib response carries one extra Cloudflare-injected `<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/…">` tag at line 6410 of the raw HTML (`diff` of the two with CR stripped shows only that line). `html_to_text()` removes `<script>`, so the curl bytes run through `html_to_text` give the same snapshot sha256 63c8ad52…42 (checked). **Consequence for the manifest: pin `snapshot_bytes`/`sha256`/lines (deterministic); `fetched_bytes`/`raw_sha256` vary per fetch with the CDN beacon — record the tool's own numbers and note the beacon (S054 recorded 143053/raw_sha256 without that issue).** Content is `immutable` (OASIS Standard, 18 Nov 2022), so the snapshot should reproduce.

## 2. Document's own identity lines (normalized-line numbers, capture-source.py output)
- L1 and L2: `Common Security Advisory Framework Version 2.0` (title, repeated)
- L3: `OASIS Standard` (approval level/status)
- L4: `18 November 2022`
- L5-L13 "This stage / Previous stage / Latest stage" URLs: this stage `…/v2.0/os/csaf-v2.0-os.html` (`.md` marked "(Authoritative)", also `.pdf`); latest stage `…/v2.0/csaf-v2.0.html`
- L14-L15 TC: OASIS Common Security Advisory Framework (CSAF) TC; Chair Omar Santos (Cisco); Editors Langley Rock (Red Hat), Stefan Hagen, Thomas Schmidt (BSI) (L16-L19)
- L42 Abstract: "The Common Security Advisory Framework (CSAF) Version 2.0 is the definitive reference for the language which supports creation, update, and interoperable exchange of security advisories as structured information…"
- L43-L47 Status: "last revised or approved by the membership of OASIS on the above date"; Non-Assertion Mode of the OASIS IPR Policy (L46); the machine-readable JSON schema, not the prose, prevails on discrepancy (L47).
- Supersedes: CSAF Common Vulnerability Reporting Framework (CVRF) 1.2.
- Caveat: the registered "tier A spec" is the **OASIS Standard 2.0 HTML**, not the later stage; I did not check whether a newer CSAF version exists (not observed).

## 3. Citation format and copyright/licence (L48-L61)
- L48-L51, verbatim: `[csaf-v2.0]` / `Common Security Advisory Framework Version 2.0. Edited by Langley Rock, Stefan Hagen, and Thomas Schmidt. 18 November 2022. OASIS Standard. https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html. Latest stage: https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html.`
- L53 `Copyright © OASIS Open 2022. All Rights Reserved.`; L55: "This document and translations of it may be copied and furnished to others, and derivative works that comment on or otherwise explain it or assist in its implementation may be prepared, copied, published, and distributed, in whole or in part, without restriction of any kind, provided that the above copyright notice and this section are included on all such copies and derivative works. However, this document itself may not be modified in any way…" ; L56 permissions are perpetual; L57 "AS IS" disclaimer.
- **Committing a normalized capture is permitted** provided the copyright notice and Notices section are included: the snapshot is an unmodified-content copy (text extraction, no edits) and L52-L61 (Notices) are retained inside it (checked: lines 52-61 present). Recommend the entry/manifest cite `Copyright © OASIS Open 2022` and name the licence condition (copy "without restriction of any kind" with notice retained).
- Prior handling: no manifest in round-31…37 carries a licence/copyright field (grep of manifest.json for copyright|licen[sc]e|redistribut: no hit); 45 prior snapshots (round-24 … round-37) are committed verbatim, and 25 of them (e.g. S054, S053, S051, S001) contain a © line (grep -c over source-snapshots/round-*/S*.txt). S055 is the first capture with an explicit copy-permission clause, so naming it in the manifest `purpose` is an improvement, not a deviation.

## 4. Registry anchor (headings, body lines; ToC duplicates exist at L148/L152/L172 so do not anchor on them — each heading text occurs twice, `grep -nxF`)
| Section | Heading | Body line | ToC line |
|---|---|---|---|
| Flags (machine-readable not-affected justifications) | `3.2.3.5 Vulnerabilities Property - Flags` | 1729 | 148 |
| Product status | `3.2.3.9 Vulnerabilities Property - Product Status` | 1854 | 152 |
| VEX profile | `4.5 Profile 5: VEX` | 2134 | 172 |
Supporting: product_status property definitions L1885-L1894 (eight values: first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected, recommended, under_investigation; list at L1855); Flag label enum L1757-L1761 (component_not_present, inline_mitigations_already_exist, vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path, vulnerable_code_not_present) with definitions L1763-L1769; VEX profile rules L2137-L2156; tests 6.1.27.7 VEX Product Status L2843-L2861, 6.1.32 Flag without Product Reference L3084, 6.1.33 Multiple Flags with VEX Justification Codes per Product L3095-L3097; [VEX-Justification] reference L484-L485; /document/category csaf_vex L2156.
Suggested registry anchor string: `§3.2.3.9 Product Status (L1854), §3.2.3.5 Flags (L1729), §4.5 Profile 5: VEX (L2134)`.

## 5. Candidate located quotes for the lesson Gate (each ≤25 words, exact substring of one normalized line, occurrences=1 in the snapshot — counted with `str.count`)
1. **L1890** (22 words): `Known not affected (known_not_affected) of value type Products (products_t) represents that these versions are known not to be affected by the vulnerability.` — product-status category definition (same line continues "No remediation is required regarding this vulnerability.", 7 words, also occurrences=1).
2. **L1762** (9 words): `The given values reflect the VEX not affected justifications.` — ties the flags `label` enum to the VEX justification set (the enum itself is L1757-L1761).
3. **L2152** (18 words): `an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.` — VEX profile requirement for every known_not_affected product (line begins `/vulnerabilities[]/product_status/known_not_affected `, so quote from "an impact…").
Spare quotes (all occurrences=1): L1763 `component_not_present: The software is not affected because the vulnerable component is not in the product.` (15 words); L2135 `The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability.` (24 words); L1894 `represents that it is not known yet whether these versions are or are not affected by the vulnerability.` (18); L2156 `The value of /document/category SHALL be csaf_vex.` (7); L3096 `it MUST be tested that a Product is not member of more than one Flag item with a VEX justification code` (21).
Do NOT use `Valid enum values are:` (occurrences=4: L688, L1021, L1098, L1756).
Pitfall: L1855's "eight defined properties" sentence is 22+ words and spans the list; avoid it as a quote, cite L1855 as anchor only.

## 6. Reproduction
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S055 --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html --out corpus/source-snapshots/round-38/S055.txt --kind html` → expect snapshot_bytes=272441, sha256 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42, 5146 lines (fetched_bytes varies by Cloudflare beacon: 414858 curl / 415225 urllib at 18:35:44Z).
