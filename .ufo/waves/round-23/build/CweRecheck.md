# CweRecheck — S013 stable methodology assertion (round 23)

- Seat: `KasegiR23.CweRecheck-5` (scout, read-only). Axes: depth:verifiability, coverage.
- Observed base: `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.
- Source opened: https://cwe.mitre.org/top25/archive/2025/2025_methodology.html (S013 row).
- Retrieved: 2026-10-20; HTTP `Date: Tue, 20 Oct 2026 21:43:11 GMT`; `200 OK`; 27,864 bytes.
- No production edits; only this report written. No tools installed.

## Chosen assertion (selected from the existing entry, not new wording)

Existing entry `corpus/knowledge/cwe-top25-2025-methodology.md` requires any year-over-year
comparison to disclose that the 2025 edition stopped View-1003 normalization. The stable anchor
for that requirement is this exact sentence already carried in the entry's Evidence:

> "For the first time in 2025, the Top 25 used the actual CWE mappings as provided, without normalizing them back to View-1003."

- Words: **22** (chars 124), under the 25-word Q3 bar.
- Exact location: S013, `<h2 class="header">2025 CWE Top 25 Methodology</h2>` →
  `<h3>Removal of CWE Mapping Normalization</h3>`, **third (final) paragraph, first sentence**.
- Exactness basis: identical contiguous substring after HTML whitespace normalization and entity
  decoding; occurs **exactly once** on the page. Raw HTML breaks the line between `back to` and
  `View-1003` (`back to\n   View-1003`) and carries **no inline tags inside the quote**, so a raw
  byte grep for the one-line sentence will legitimately fail; normalize first.
- Why stable: past-tense, edition-scoped statement about the completed 2025 calculation, on an
  archived `/archive/2025/` page, finalized after the 2025-11-17 data pull; it names the change
  itself rather than a revisable count. It does not depend on the 39,080-record number.

## Date / version

- Edition: **2025 CWE Top 25** (URL path `top25/archive/2025/`; h2 "2025 CWE Top 25 Methodology").
- Page self-reported revision: **"Page Last Updated: January 23, 2026"** (footer, verified verbatim).
- Document version string: **none present** (no `vN` label). Response headers carry **no
  `Last-Modified` and no `ETag`** (headers present: Date, Content-Type, Content-Length absent,
  Transfer-Encoding, CSP, cookies, STS, X-*).
- Strongest available revision pin: sha256 of the retrieved HTML
  `62c28eda60304d265dab6d96f7f9b7b45fabc63f769bd62263643075726051d6`.
- Consistency: `corpus/SOURCES.md` S013 already records "page last updated 2026-01-23"; the
  entry's `verified-at: 2026-10-19` re-dates without drift one day later (same displayed revision).

## Recheck (executed locally, exit 0)

Saved `2025_methodology.html` to `/tmp`, then asserted on normalized text:

```python
import re, html, hashlib
s = open('S013_methodology.html', encoding='utf-8').read()
norm = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()
page = norm(s)
Q = "For the first time in 2025, the Top 25 used the actual CWE mappings as provided, without normalizing them back to View-1003."
assert page.count(Q) == 1 and len(Q.split()) == 22
assert '<h3>Removal of CWE Mapping Normalization</h3>' in s
body = s.split('<h3>Removal of CWE Mapping Normalization</h3>', 1)[1].split('<h3>', 1)[0]
paras = [norm(p) for p in re.findall(r'<p>(.*?)</p>', body, re.S)]
assert len(paras) == 3 and paras[2].startswith(Q)
assert 'Page Last Updated: January 23, 2026' in page
assert '<h2 class="header">2025 CWE Top 25 Methodology' in s
print(hashlib.sha256(s.encode()).hexdigest())
```

Observed all PASS; sha256 matched the value above.

## Other entry quotes checked (same source, all exact, each once)

| Entry claim | Verified words | Location |
|---|---|---|
| "This year’s dataset included 39,080 CVE Records for vulnerabilities published between June 1, 2024 and June 1, 2025." | 18 | opening summary, para 1 |
| "only CVE Records that contain CVSS version 3.0 or 3.1 data were considered in the calculations." | 16 | h3 "Scoring", para 2 (sentence 2) |

Limit quote for over-reading the chosen assertion: "the Top 25 team received feedback on 2,459 CVE
Records (26% of total requested) from 170 CNAs (60% of total contacted)" — 21 words, h3 "CNA Expert
Collaboration", verified exact once. The chosen sentence therefore does **not** imply that all
mappings were reviewed or corrected.

Cross-reference (separate source, corroboration only, not a substitute): S014 h2 "2025 CWE Top 25
Key Insights" states "the 2025 CWE Top 25 used all CWE mappings as provided and reviewed by CNAs,
without normalizing them back to View-1003" — 21 words, exact once; S014 footer "Page Last Updated:
December 10, 2025".

## Falsifiable findings

1. If normalized S013 stops containing the 22-word sentence exactly once, or starts containing it
   more than once, the entry's mandated normalization disclosure loses its primary anchor and must
   be re-sourced or withdrawn — not silently reworded.
2. If the sentence survives but no longer sits in the third paragraph under the h3 heading, the
   recorded location pointer is falsified even though the wording is intact.
3. The sha256 pin falsifies silent edits: the footer date alone cannot prove the bytes are unchanged.
4. Using this quote to support the CVSS 3.0/3.1 limitation is a misattribution (falsifier: the
   sentence contains no CVSS term); that claim rests only on the 16-word "Scoring" quote.
5. Using this quote to imply complete mapping review is unsupported by the 21-word CNA-feedback
   sentence (2,459 of 9,468 scoped records; 170 of 281 CNAs).

## Scope limits

- Public archived MITRE page only; read-only, no target testing, no security probing.
- MITRE can still revise an archive page; S013's own displayed date plus my byte hash bound this
  observation to 2026-10-20, not to the original 2025 release.
- No S013 snapshot exists yet under `corpus/source-snapshots/round-23/`; this report is the durable
  copy of the quote and hash. Production snapshot creation is the writer/L1 lane's call.
- S014 is MITRE's companion interpretation of the same change, not an independent authority; no
  third-party source was used.
- No claim is made about ranking correctness, CWE prevalence, or any report's severity; the
  assertion is methodology provenance for the entry's disclosure rule only.
