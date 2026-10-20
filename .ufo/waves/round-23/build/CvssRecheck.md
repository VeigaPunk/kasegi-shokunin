# CvssRecheck — S001 CVSS-B is severity, not risk

- Seat: `KasegiR23.CvssRecheck-5` (scout; read-only)
- Axes named: `depth:verifiability`, `coverage`
- Target: S001 existing row — <https://www.first.org/cvss/v4.0/user-guide>
- Access: 2026-10-20 21:43 UTC (HTTP `date` header)
- Production edits: **none**. This report is the only file written by this seat.
- Tool installs/updates: **none**.

## Verdict

**PASS — S001's recorded quote is exact and remains at one location.** No correction to the
existing quote is required. The registry anchor names the heading and `Document Version: 1.2`
but omits the section number and version date; the linked PDF supplies both (`§2.2`, PDF p. 5)
without contradicting the row.

This slice supplies verifiable evidence for S001 only. It supplies **no** F06–F08 evidence and
claims **no** coverage admission or axis score; S001 belongs to the F01 practice surface.

## Load-bearing assertion

Exact quote, **22 words** (limit 25), verbatim after whitespace normalization:

> CVSS Base (CVSS-B) scores are designed to measure the severity of a vulnerability and should not be used alone to assess risk.

This is a contiguous substring of the sentence beginning “The CVSS Specification Document
has been updated to emphasize and clarify the fact that …”; it is not a standalone sentence.
The excerpt is complete for the claim because it names `CVSS-B`, says it measures
**severity**, and says it must not be used **alone** to assess **risk**.

Durable location:

| carrier | location | identity on 2026-10-20 |
|---|---|---|
| HTML | `<h2 id="CVSS-Base-Score-CVSS-B-Measures-Severity-not-Risk">CVSS Base Score (CVSS-B) Measures Severity, not Risk</h2>`; capture-relative lines 124, 126–127 | 96,898 bytes; SHA-256 `1eb4e2a5b3a79c081e069e177575d9cb0ab95f98a0aff934c487983f187814e6` |
| PDF | `§2.2`, page 5, under the same heading | 1,721,199 bytes; SHA-256 `94e705a62ed016fe60e71b10afc6acd7b2151bf05df5150ec93166d3dc138952`; 32 pages |

The HTML anchor is the durable locator; “capture-relative lines” are evidence from this
capture only and will drift on re-render.

Document identity and dates (keep them distinct):

| fact | observed value | source |
|---|---|---|
| Document version | `1.2` | HTML line 26; PDF p. 1 |
| Version-history date for v1.2 | `2025-11-14` | HTML lines 1107–1108; PDF p. 32 |
| Version-history description | “Additional definitions in Glossary.” | same row |
| HTML `Last-Modified` | `Fri, 09 Oct 2026 18:44:07 GMT` | HTTP response header |
| PDF `Title` metadata | `CVSS v4.0 User Guide - 2025-11-16` | `pdfinfo` |
| Access date | `2026-10-20` | HTTP `date` header |

`Last-Modified` is origin page-modification metadata, not a document version date; the PDF
title date is renderer metadata, not the version-history date. Cite **`v1.2` + `2025-11-14`**
as the document identity, and the access date for this recheck.

Capture commands used (all run 2026-10-20):

```sh
curl -sS https://www.first.org/cvss/v4.0/user-guide -o cvss40ug.html
curl -sS -o cvss-v40-user-guide.pdf https://www.first.org/cvss/v4-0/cvss-v40-user-guide.pdf
pdftotext -layout cvss-v40-user-guide.pdf cvss40ug.txt
pdfinfo cvss-v40-user-guide.pdf
sha256sum cvss40ug.html cvss-v40-user-guide.pdf
```

## Minimal assertion set

| id | assertion | why it is in the minimal set |
|---|---|---|
| A1 | live HTTPS GET returns `200` | distinguishes a live document from an error/block page |
| A2 | `Document Version: 1.2` appears in rendered text | version gate; `on-release` recheck trigger |
| A3 | version-history row `2025-11-14` / `v1.2` is present | dates the version independently of page headers |
| A4 | exact `<h2 id="CVSS-Base-Score-CVSS-B-Measures-Severity-not-Risk">` and heading text | the located section, not a pagewide name match |
| A5 | 22-word quote occurs **inside that h2 section**, exact after whitespace normalization | the load-bearing semantic assertion |
| A6 | quote occurs **exactly once pagewide** | detects a moved or duplicated quote that would make location ambiguous |
| A7 | quote is ≤25 words (observed 22) | satisfies the evidence-format bound |

Minimality argument: A5 alone carries the severity-not-risk claim. A1–A4 and A6–A7 are
provenance/location gates that prevent a false pass on a version-drifted, moved, duplicated,
or over-long quote. No second quote is needed; the following paragraphs about Environmental
and Threat metrics corroborate the claim but are not necessary conditions for it.

## Executable local recheck

Stdlib only; `S001_URL` may point at a saved capture for offline or mutated-copy tests.

```python
#!/usr/bin/env python3
"""S001 executable recheck: CVSS v4.0 User Guide (severity, not risk).

Passes only if the exact quote occurs once, inside the named h2 section, on
Document Version 1.2. Set S001_URL=file:///path/to/capture.html for offline or
mutated-copy controls.
"""
import hashlib, json, os, re, sys, urllib.request
from html import unescape

URL = os.environ.get("S001_URL", "https://www.first.org/cvss/v4.0/user-guide")
QUOTE = ("CVSS Base (CVSS-B) scores are designed to measure the severity of a "
         "vulnerability and should not be used alone to assess risk.")
ANCHOR = 'id="CVSS-Base-Score-CVSS-B-Measures-Severity-not-Risk"'
HEADING = "CVSS Base Score (CVSS-B) Measures Severity, not Risk"

if URL.startswith("file:"):
    with open(urllib.request.url2pathname(URL[5:]), "rb") as fh:
        raw, status, last_modified = fh.read(), 200, None
else:
    req = urllib.request.Request(URL, headers={"User-Agent": "kasegi-s001-recheck/1",
                                               "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=30) as r:
        status, last_modified, raw = r.status, r.headers.get("Last-Modified"), r.read()
html = raw.decode("utf-8", "replace")

def text(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    return unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()

start = html.find(ANCHOR)
end = html.find("<h2", start + len(ANCHOR)) if start >= 0 else -1
section_text = text(html[start:end]) if start >= 0 and end > start else ""
page_text = text(html)

checks = {
    "http_200": status == 200,
    "document_version_1_2": "Document Version: 1.2" in page_text,
    "version_history_v1_2_2025_11_14": bool(
        re.search(r"2025-11-14\s*</td>\s*<td>\s*v1\.2\s*</td>", html)),
    "anchor_present": start >= 0,
    "heading_in_section": HEADING in section_text,
    "quote_in_section": QUOTE in section_text,
    "quote_exact_once_pagewide": page_text.count(QUOTE) == 1,
    "quote_words_le_25": len(QUOTE.split()) <= 25,
}
result = {
    "url": URL, "http_status": status, "last_modified": last_modified,
    "content_length": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
    "quote_words": len(QUOTE.split()),
    "pagewide_quote_occurrences": page_text.count(QUOTE),
    "checks": checks, "all_pass": all(checks.values()),
}
print(json.dumps(result, indent=2))
sys.exit(0 if result["all_pass"] else 1)
```

Observed run (`python3 check_s001.py`, exit 0):

```json
{
  "url": "https://www.first.org/cvss/v4.0/user-guide",
  "http_status": 200,
  "last_modified": "Fri, 09 Oct 2026 18:44:07 GMT",
  "content_length": 96898,
  "sha256": "1eb4e2a5b3a79c081e069e177575d9cb0ab95f98a0aff934c487983f187814e6",
  "quote_words": 22,
  "pagewide_quote_occurrences": 1,
  "checks": {
    "http_200": true,
    "document_version_1_2": true,
    "version_history_v1_2_2025_11_14": true,
    "anchor_present": true,
    "heading_in_section": true,
    "quote_in_section": true,
    "quote_exact_once_pagewide": true,
    "quote_words_le_25": true
  },
  "all_pass": true
}
```

## Red-before controls (observed)

Each mutant was applied to a **local copy** of the 2026-10-20 capture; the live page was not
modified. Command shape:
`S001_URL=file:///tmp/kasegi-r23-cvssrecheck/<mutant>.html python3 check_s001.py`.

| mutant | edit | exit | failing checks |
|---|---|---|---|
| `m1_drop_alone` | `should not be used alone` → `should not be used` | 1 | `quote_in_section`, `quote_exact_once_pagewide` |
| `m2_version_1_3` | `Document Version: 1.2` → `1.3` | 1 | `document_version_1_2` |
| `m3_history_v1_3` | history cell `v1.2` → `v1.3` | 1 | `version_history_v1_2_2025_11_14` |
| `m4_anchor_renamed` | `id="…-CVSS-B-…"` → `id="…-CVSS-…"` | 1 | `anchor_present`, `heading_in_section`, `quote_in_section` |
| `m5_duplicate_quote` | quote appended again before `</body>` | 1 | `quote_exact_once_pagewide` |
| `m6_reflow_only` | only extra whitespace/newline inside the quote | 0 | none (negative control) |

`m6` is the important control: whitespace reflow does **not** fail, so the checker tests words
and punctuation, not the page's line wrapping. `m1` shows that dropping the word `alone`
fails; `m5` shows a duplicate does not silently pass as one location.

## Falsifiers

The finding is false, or the guidance is unverified, if any of these hold on a future recheck:

1. **Quote drift** — any word or punctuation change in A5 fails; dropping `alone` was observed
   to fail (`m1`). A revision that changes the claim must be re-read, not string-patched.
2. **Version drift** — a new `Document Version` or version-history row fails A2/A3 (`m2`/`m3`),
   forcing a full re-open under the S001 `on-release` policy.
3. **Location drift** — renaming the h2 anchor fails A4/A5 (`m4`); the quote must be re-located,
   not assumed to remain in `§2.2`.
4. **Ambiguity drift** — a second identical quote fails A6 (`m5`), so location must be
   re-established before citing.
5. **Unreachable page** — a non-200, timeout, or block page cannot pass A1; record `unverified`.
   Absence of official text is not permission to substitute a secondary source.

## Scope limits and remaining unknowns

- **HTML only for the executable gate.** The PDF was checked once by hand (`pdftotext`,
  `pdfinfo`), not by the script. The PDF has its own digest and could diverge from the HTML
  between checks; neither carrier is notarized or archived here.
- **`Last-Modified` is not a content proof.** It is origin metadata and may move without a
  textual change (or vice versa). Content proof is the SHA-256 plus A2–A7.
- **A3 is raw-HTML-layout-coupled.** A template-only change can fail the version-history
  regex without a document revision; treat that failure as a re-open signal, not proof of a
  version bump.
- **The `2026-10-09` page modification is not a v1.3 release.** Version history still ends at
  `v1.2` / `2025-11-14`; the reason for the later page timestamp was not established.
- **The PDF title date `2025-11-16` was not reconciled** with the `2025-11-14` version-history
  date. Both are reported as observed; the version-history row is the document-version date.
- **No claim about `CVSS-BTE` = risk.** The same page says a `CVSS-BTE` score “can be considered
  much closer to ‘Risk’”; this report asserts only the `CVSS-B`/severity-not-risk sentence and
  does not promote `CVSS-BTE` to a risk rating.
- **No program-policy claim.** This evidence does not establish any bounty program's severity
  rubric, eligibility, or reward tier, and does not admit F06–F08.
- **No archival permanence.** The page is a live public document; this report records one
  access (2026-10-20) and the observed hashes, not a durable web archive.

## Existing-row disposition

The S001 row in `corpus/SOURCES.md:7` is accurate as written: its anchor is the exact heading
and `Document Version 1.2`, and its quote (recorded in `corpus/lessons/round-22.md:77` and
`corpus/knowledge/cvss-v4-severity-and-vector.md:25`) matches this capture. If L1 chooses to
sharpen the anchor without changing meaning, the minimal delta is to add
`§2.2; HTML #CVSS-Base-Score-CVSS-B-Measures-Severity-not-Risk; v1.2, version history 2025-11-14`.
No such production edit was made by this read-only seat.
