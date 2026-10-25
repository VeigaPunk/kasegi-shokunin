# CnaScope — CNA Operational Rules v4.1.0: Scope Definition MUST and assignment-overlap rules

- Seat: `KasegiR23.CnaScope-5` (scout, read-only lane)
- Round: 23 · observed base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`
- Observed: 2026-10-20 · axes: `depth:verifiability`, `coverage`
- Lane: open the frozen v4.1.0 public PDF, verify the Scope Definition MUST and the
  assignment-overlap rules, and locate exact ≤25-word quotes. Admission, SOURCES/Frontier
  edits and any version ruling are other seats'/L1's call. This seat wrote only this file.

## 1. Opened source identity (observed)

| field | value |
|---|---|
| URL | `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf` |
| fetch | `curl -sSL`, 2026-10-20 21:34:06 GMT, HTTP/2 **200** |
| bytes / content-type | 250107 · `application/pdf` |
| `last-modified` / `etag` | `Tue, 03 Jun 2025 17:05:56 GMT` · `"b5ddf94c61b1ec1bfaee6ca2a421d83e"` |
| PDF SHA-256 | `9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0` |
| `pdfinfo` | 23 pages, 612×792 pts; Title `CVE Numbering Authority (CNA) Operational Rules, Version 4.1.0`; CreationDate 2025-05-13, ModDate 2025-06-02 |
| extraction | `pdftotext -layout` (poppler **26.08.0**); extracted-text SHA-256 `22a948b150703df7c89d8508bce068d9aa6be09e8182f892c0e1f09623dc4754` |

Internal header block (PDF p. 1, verbatim lines):

```text
Version 4.1.0
Effective May 14, 2025
Approved by CVE Board on May 14, 2025
```

Date/version check against the existing S022 row (`corpus/SOURCES.md:28`): the row says
“Sections 3.1 and 4.1; effective and approved 2025-05-14” for `v4.1.0`. **Version and both
dates MATCH the opened PDF.** The section locator is discussed in F2.

## 2. Required located quote — Scope Definition MUST (24 words)

> “CNAs MUST develop, document, and operate within a Scope Definition that describes the types of Vulnerabilities for which the CNA will assign CVE IDs.”
> — §3.1.1, PDF **physical page 7** (printed page label 6), CNA Operational Rules **v4.1.0**, effective 2025-05-14.

- Whitespace word count: **24** (≤25). This is the complete sentence; the PDF wraps after “the”.
- Verified as an exact substring after collapsing PDF line breaks only (`' '.join(text.split())`).
- The existing S022 quote `“CNAs MUST develop, document, and operate within a Scope Definition”`
  is a **10-word exact prefix** of this sentence (verified `startswith`). It is not wrong, but it
  truncates before the clause that says what the Scope Definition must describe; the full
  24-word sentence fits the quote budget and is the stronger citation.

### Supporting Scope Definition MUSTs (all exact substrings, ≤25 words)

| clause | phys. p. | exact quote | words |
|---|---|---|---|
| 3.1.1.1 | 7 | “The Scope Definition is initially established during the CNA on-boarding process and MUST be completed and approved prior to a new CNA being authorized.” | 24 |
| 3.1.1.2 | 7 | “The CNA MUST obtain approval for the Scope Definition from their Root or TL-Root.” | 14 |
| 3.1.4 | 7 | “the Scope Definition MUST include a covered set of Products and MUST NOT only list non-covered items.” | 17 |
| 3.1.10 | 8 | “CNA Scope Definition disputes MUST initially be handled at the Root, TL-Root, or Council of Roots level.” | 17 |
| 3.1.12.1 | 8 | “Organizations with multiple CNAs or CNA-LRs MUST specify individual Scope Definitions for each CNA or CNA-LR.” | 16 |

For 3.1.4 the clause begins mid-sentence with the exact words “For Scope Definitions based on
Products,” followed by the quoted MUST clause.
3.1.1.2's second sentence (“Approved Scope Definitions MUST be published in the List of Partners”)
is also exact but is not reproduced here; it remains a separate obligation.

## 3. Assignment-overlap rules (observed)

`§4.2.16` is titled “Multiple CNAs With Overlapping Scopes” (body PDF p. 15). It is not itemised
in the TOC, which stops at §4.2 “CVE ID Assignment” (PDF p. 2); the body heading is the locator.
Its framing text is not a modal rule: it says overlaps happen and the rules below clarify which
CNA assigns. The operative rules split into a hard scope boundary, a hard escalation path, a
hard upstream-deferral duty, and several SHOULD coordination rules.

| clause | phys. p. | exact quote (≤25 words) | modal |
|---|---|---|---|
| 4.2.1.1 | 13 (label 12) | “The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign.” | MUST |
| 4.2.16.1 | 15 (label 14) | “CNAs MUST NOT assign CVE IDs to Vulnerabilities outside of their scope.” | MUST NOT |
| 4.2.16.2 | 15 | “CNAs SHOULD assign CVE IDs within their scope.” | SHOULD |
| 4.2.16.3 | 15 | “then the CNAs who are aware of the Vulnerability SHOULD work together to assign CVE IDs” | SHOULD |
| 4.2.16.4 | 15 | “those CNAs SHOULD work together to assign CVE IDs” | SHOULD |
| 4.2.16.5 | 15 | fragment: “the decision about which CNA assigns the ID MUST be made by the lowest level organization” | MUST |
| 4.2.16.6 | 15 | fragment: “they MUST notify and defer first-refusal CVE ID assignment to the upstream Supplier of the dependency” | MUST |
| 4.2.19 | 16 (label 15) | “CNAs SHOULD ask requesters if they have already requested an assignment from another CNA” | SHOULD |
| 4.2.20 | 16 | “CNAs SHOULD consider coordinating with an appropriate Root or CNA-LR before assigning CVE IDs” | SHOULD |
| 4.3.1 | 16 | “the first CNA SHOULD either refer the reporter or requester to or attempt to notify the appropriate CNA” | SHOULD |

Notes on the two MUST fragments:

- **4.2.16.5 full clause is 46 words**, over the quote budget. The fragment above is exact and
  contiguous; the rest of the clause adds that the lowest level is “(Root, TL-Root, Council of
  Roots)” and that this applies when “the CNAs cannot resolve the assignment decision themselves”.
- **4.2.16.6 full clause is 41 words.** The fragment is exact and contiguous; the remainder adds
  the condition “if the upstream Supplier is a CNA”. Do not drop that condition when citing.
- 4.2.16.3 applies to a Vulnerability “that has not yet been Publicly Disclosed”; 4.2.16.4 applies
  when multiple CNAs with overlapping scopes “are coordinating the Public Disclosure of a
  Vulnerability”.
- 4.2.16.6 is a Supplier-CNA duty about an upstream dependency, not a general tie-breaker.

## 4. Findings (each falsifiable against the opened bytes)

Row text quoted in F2 is from `corpus/SOURCES.md:28`; every other quote in this section is from
the opened v4.1.0 PDF (or, in F5, the opened v4.2.0 PDF and recorded here as a cross-check).

- **F1 — Scope Definition MUST verified.** §3.1.1 contains the exact 24-word MUST quoted above
  on physical p. 7. Falsifier: `pdftotext -f 7 -l 7 -layout v410.pdf - | grep -n "3.1.1 CNAs MUST"`.
- **F2 — S022 locator is incomplete for its own description.** The row describes “CNA scope,
  vulnerability determination and assignment” but locates “Sections 3.1 and 4.1”. Per the TOC,
  §4.1 is *Vulnerability Determination*; assignment authority/overlap lives in §4.2.1 (first
  refusal) and §4.2.16 (overlapping scopes). The row's locator therefore does not cover the
  assignment half of its own description. Minimal correction for the row owner: locator
  `3.1.1, 4.2.1, 4.2.16` (or drop “assignment” from the description). Falsifier: TOC at PDF p. 2
  plus the §4.1/§4.2 headings.
- **F3 — Overlap is not merely SHOULD coordination.** Three MUST-level duties are present:
  4.2.16.1 (no assignment outside scope), 4.2.16.5 (unresolved overlap decision by the lowest
  shared Root/TL-Root/Council of Roots), 4.2.16.6 (upstream Supplier CNA gets notified and
  first refusal). A summary that renders overlap handling as purely advisory is false against
  these lines.
- **F4 — Date/version verified.** Header says v4.1.0, Effective May 14, 2025, Approved by CVE
  Board on May 14, 2025; S022's “effective and approved 2025-05-14” matches. Falsifier: header
  text on PDF p. 1.
- **F5 — Cross-version cross-check (not this lane's admission basis).** The sibling official URL
  `CNA_Rules_v4.2.0.pdf` also returns HTTP 200 today (665517 bytes, SHA-256
  `7be61b7fc082c1b388510589d7e2ba86e7b96f908b19fab889e7e9c847b31039`) and its header reads
  “Version: 4.2.0”, “Approved date: 2026-August-20”, “Effective date: 2026-August-25”. The §3.1.1
  sentence is identical across the two versions (normalised comparison), while §4.2.16 in
  v4.2.0 extends the list with 4.2.16.7–4.2.16.9. Consequence: S022 is evidence for **v4.1.0
  only**; using it as evidence about the current rules requires the v4.2.0 text. Version
  adjudication belongs to `CnaVersion`/`CnaFix`, not this seat.

## 5. Reproduction (offline after one fetch; no network trust needed later)

```bash
mkdir -p /tmp/kasegi-r23-scope && cd /tmp/kasegi-r23-scope
curl -sSL -D headers.txt -o v410.pdf \
  https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf
sha256sum v410.pdf   # 9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0
pdftotext -layout v410.pdf v410.txt   # poppler 26.08.0
pdftotext -f 7  -l 7  -layout v410.pdf - | grep -n "3.1.1 CNAs MUST"
pdftotext -f 13 -l 13 -layout v410.pdf - | grep -n "4.2.1.1"
pdftotext -f 15 -l 15 -layout v410.pdf - | grep -nE "4\.2\.16\.[1-6]"

python3 - <<'EOF'
t = ' '.join(open('v410.txt').read().split())
q = {
 "3.1.1":   "CNAs MUST develop, document, and operate within a Scope Definition that describes the types of Vulnerabilities for which the CNA will assign CVE IDs.",
 "4.2.16.1":"CNAs MUST NOT assign CVE IDs to Vulnerabilities outside of their scope.",
 "4.2.16.5":"the decision about which CNA assigns the ID MUST be made by the lowest level organization",
 "4.2.16.6":"they MUST notify and defer first-refusal CVE ID assignment to the upstream Supplier of the dependency",
}
for k, s in q.items():
    print(k, len(s.split()), s in t)
EOF
```

Expected: all booleans `True`; word counts `24 12 16 16`; SHA-256 exactly as recorded.
If the served PDF digest differs, the quotes are unverified against this report — re-open and
re-locate rather than reusing these strings.

## 6. Scope limits

- Claims above are about the **v4.1.0 bytes** fetched on 2026-10-20 and nothing else. The v4.2.0
  material in F5 is a cross-check, not a verified v4.2.0 rule inventory.
- Page citations are **physical PDF pages** (`pdftotext -f`), which run one ahead of the printed
  page labels; both are given where it matters (physical 7 = label 6, 13 = 12, 15 = 14, 16 = 15).
- Quotes are verified against `pdftotext -layout` output with whitespace collapsed. They are not
  verified against the raw PDF content stream or a glyph-level comparison; ligature/encoding
  differences in other extractors are possible.
- Not verified here: any CNA's actual Scope Definition, its approval in the List of Partners,
  CNA registration status, whether a given program applies v4.1.0 or v4.2.0, or any assignment
  outcome. No external contact, no CVE request, no production/corpus edit was made.
- Current-version status, SOURCES/Frontier row edits, and any admission credit are out of this
  seat's lane and are not claimed.

## 7. Tooling record

No installs or upgrades. Used host `curl` and `pdftotext`/`pdfinfo` from poppler 26.08.0 already
present; scratch work confined to `/tmp/kasegi-r23-scope`. Pacman remains untouched (host pause).
