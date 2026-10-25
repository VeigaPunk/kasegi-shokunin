# CvdRecheck — S004 CERT/CC disclosure policy recheck (round 23)

Read-only public-document seat. No production file was edited; this report is the only
file written. No subagent was dispatched. Source opened live, not from a cached copy.

## Scope

- Target: S004 `CERT/CC Vulnerability Disclosure Policy` —
  https://certcc.github.io/certcc_disclosure_policy/
- Existing row: `corpus/SOURCES.md:10` (anchor field, verbatim):
  "Vulnerability Disclosure Policy and Frequently Asked Questions; page shows no publication
  or revision date, opened 2026-10-19".
- Existing entry: `corpus/knowledge/coordinated-disclosure-timelines.md:22-23`.
- r22 gate sample: `corpus/lessons/round-22.md:80`.
- Question answered here: which quote assertions are stable enough to carry the entry and
  its 180-day recheck, and what does the page actually document as exceptions to the
  45-day rule.

## Version and date (observed)

| property | value |
|---|---|
| first fetch | 2026-10-20T21:42:42Z, HTTP/2 200 |
| cache-busted refetch | 2026-10-20T21:43Z, HTTP 200, byte-identical |
| body bytes | 28,742 |
| body SHA-256 | `4e10ee9f802397df9ffe6410b4622af59acd4d1e010739adf1cdc716bc53594e` |
| `Last-Modified` | `Tue, 26 May 2026 17:52:01 GMT` |
| `ETag` | `"6a15ddc1-7046"` |
| ETag decode | `0x6a15ddc1` = 1779817921 = 2026-05-26T17:52:01Z; `0x7046` = 28,742 → matches the two fields above |

The page itself publishes **no** date: no visible publication or revision line, no
`article:modified_time` / `datePublished` / `dateModified` meta, no git-revision footer,
no source/edit/commit link. The only headers are `<meta name="author" content="CERT
Coordination Center">` and `<meta name="generator" content="mkdocs-1.6.1,
mkdocs-material-9.7.6">` (generator, not policy revision). Therefore the S004 row's phrase
"page shows no publication or revision date" is **confirmed for page content**, and the only
falsifiable version marker available is the server-declared artifact metadata:
`Last-Modified 2026-05-26T17:52:01Z` + ETag + the body digest above.

Attempted commit pin: `https://github.com/certcc/certcc.github.io` returned HTTP 404, and the
GitHub REST API returned HTTP 403 rate-limit for this host. No source-repository revision was
obtained; that is recorded as unknown, not inferred.

## Stable quote assertions

All quotes below are exact, contiguous substrings of the page text after the normalization
recipe in "Recheck procedure". Each occurs exactly once in the normalized text (count = 1),
so the location is unambiguous. Word counts use whitespace splitting and are all ≤25.
Offsets are character offsets in the 7,411-character normalized text of the pinned digest.
Quotation marks below are meta-delimiters, not part of the quote.

| id | quote (verbatim) | words | exact location | offset |
|---|---|---|---|---|
| A | "Vulnerabilities reported to the CERT/CC will be disclosed to the public 45 days after the initial report" | 17 | h1 `Vulnerability Disclosure Policy` (`#vulnerability-disclosure-policy`), opening paragraph, sentence 1 | 477 |
| J | "regardless of the existence or availability of patches or workarounds from affected vendors" | 13 | same paragraph, same sentence 1, continuation | 583 |
| B | "Extenuating circumstances, such as active exploitation, threats of an especially serious (or trivial) nature, or situations that require changes to an established standard" | 23 | same paragraph, sentence 2, first clause | 676 |
| H | "may result in earlier or later disclosure" | 7 | same paragraph, sentence 2, final clause (the fragment the entry currently carries) | 848 |
| I | "negotiate alternate publication schedules with the affected vendors when required" | 10 | same paragraph, sentence 4, final clause | 1069 |
| F | "We think that 45 days can be a pretty tough deadline for a large organization to meet." | 17 | FAQ admonition `Why not 30 days, or 15 days, or immediately?`, body sentence 1 (the r22 gate quote) | 2115 |
| G | "No. There may often be circumstances that will cause us to adjust our publication schedule." | 15 | FAQ admonition `Will all vulnerabilities be disclosed within 45 days?`, body sentences 1–2 | 3041 |
| C | "Threats that are especially serious or for which we have evidence of exploitation will likely cause us to shorten our release schedule." | 22 | same admonition, body sentence 3 | 3133 |
| D | "Threats that require hard changes (changes to standards, changes to core operating system components) will cause us to extend our publication schedule." | 22 | same admonition, body sentence 4 | 3269 |
| E | "We may not publish every vulnerability that is reported to us." | 11 | same admonition, body sentence 5 | 3421 |

The full sentence 2 of the opening paragraph is 30 words, over the cap. It must be carried
as the two exact substrings B and H (or B alone); truncating it with an ellipsis would break
verbatim matching. B is the 23-word span that pairs all three conditions with the governing
"Extenuating circumstances" frame; the list-only tail (without that frame) also fits the cap
but drops the sentence's subject. H alone states the effect but not a single condition.

## 45-day policy exceptions (observed inventory)

The page states the 45-day interval in exactly one policy sentence (A); its other two
"45 days" occurrences are a FAQ question title and F's rationale sentence, and it documents
five adjustment mechanisms:

1. **Earlier or later for extenuating circumstances** — "active exploitation", "threats of an
   especially serious (or trivial) nature", and "situations that require changes to an
   established standard" (B + H).
2. **Negotiated alternates with vendors** — CERT/CC will "negotiate alternate publication
   schedules with the affected vendors when required" (I), immediately after promising to
   "apprise any affected vendors of our publication plans".
3. **Shorten** — especially serious threats or evidence of exploitation "will likely cause us
   to shorten our release schedule" (C).
4. **Extend** — threats requiring "hard changes (changes to standards, changes to core
   operating system components)" "will cause us to extend our publication schedule" (D).
5. **No publication at all** — "We may not publish every vulnerability that is reported to us."
   (E); the separate admonition `Do you disclose every reported vulnerability?` adds
   discretion to "decline to coordinate or publish a vulnerability report", based on scope,
   severity and ability to add value. So the 45-day interval is a default, not a guarantee of
   publication.

Trigger and patch relationship: the clock starts at "the initial report" and runs
"regardless of the existence or availability of patches or workarounds from affected
vendors" (A + J). The page does not tie the interval to a fix being available. Interval
inventory on the page: "45 days" appears three times (A, the admonition title, F);
"30 days" and "15 days" appear once each, only inside the rhetorical question title
`Why not 30 days, or 15 days, or immediately?` and are not stated deadlines; no 90-day,
14-day, 6-month or 180-day text occurs.

## Findings against the existing corpus (falsifiable)

- **P1 PASS — r22 gate quote.** F is verbatim, unique, 17 words, and correctly located at
  `Frequently Asked Questions → "Why not 30 days, or 15 days, or immediately?"`
  (`corpus/lessons/round-22.md:80`). Falsifier: normalized text no longer contains F at
  offset 2115, or the heading attribution changes.
- **P2 GAP — F cannot carry the interval claim.** F is CERT/CC's rationale ("pretty tough
  deadline"), not the policy statement: it names no trigger, no scope and no exception. A
  recheck that cites only F leaves "45 days after the initial report" unquoted. The
  load-bearing assertion should be A (+J), with F retained only as the gate sample.
- **P3 GAP — S004 row anchor lacks a version falsifier.** "page shows no publication or
  revision date" is true of page content, but the anchor stops there, so a 180-day recheck
  has no way to tell whether the page changed. The server metadata is available and
  reproducible: `Last-Modified: Tue, 26 May 2026 17:52:01 GMT`, `ETag "6a15ddc1-7046"`,
  SHA-256 `4e10ee9f…`. Recommended anchor suffix: "no in-page date; HTTP Last-Modified
  2026-05-26T17:52:01Z, sha256 4e10ee9f… (opened 2026-10-20)". Falsifier: refetch returns a
  different digest or Last-Modified.
- **P4 GAP — entry evidence is thinner than its own rule.** The entry's rule requires that
  "any extension names its documented condition"
  (`corpus/knowledge/coordinated-disclosure-timelines.md`, Rule), but its S004 evidence
  carries only H ("may result in earlier or later disclosure"), which names no condition.
  Adding B, C, D and E (or B, C, D at minimum) makes the rule checkable against the source.
  This is a completeness gap, not a quote-accuracy error: H itself is exact and unique.
- **P5 PROCEDURE FALSIFIER — raw-HTML matching falsely fails.** Fetched HTML soft-wraps the
  sentences inside the text, e.g. `...public 45 days\nafter the initial report...` and
  `...for a large\norganization to meet.`. A `grep -F` or direct `in` check against raw bytes
  returns false for **9 of the 10** assertions above (A–G, I, J; H is the exception only
  because its 7 words happen to fall on a single source line). Any recheck must normalize
  whitespace first; otherwise it will report a false quote regression. In the quoted spans there are no HTML entities (12 straight apostrophes,
  zero `&rsquo;`, `&nbsp;`, `&amp;`), so entity decoding is not the failure source here, but
  belongs in the recipe for robustness.
- **P6 SCOPE — no transplanting.** The page asserts exactly one interval (45 days); the
  30/15-day strings are rhetorical alternatives in a question title. The entry's existing
  "Rejected" and "Limits" paragraphs are consistent with the observed text: this is CERT/CC's
  own coordinator policy for reports it receives (with U.S. Government web sites forwarded to
  CISA), not a general legal deadline.

## Recheck procedure (executable, local)

Python 3, standard library only; no network beyond the single GET, no installs:

```python
import re, html, hashlib
raw = open('s004.html', encoding='utf-8').read()          # pinned bytes
assert hashlib.sha256(raw.encode()).hexdigest() == \
  '4e10ee9f802397df9ffe6410b4622af59acd4d1e010739adf1cdc716bc53594e'
s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', raw)
s = re.sub(r'(?i)<br\s*/?>', ' ', s)
s = re.sub(r'(?i)</(p|li|h[1-6]|div|blockquote|tr|td|th)>', '\n', s)
s = re.sub(r'<[^>]+>', '', s)
text = re.sub(r'\s+', ' ', html.unescape(s))
q = ("Vulnerabilities reported to the CERT/CC will be disclosed to the public "
     "45 days after the initial report")
assert text.count(q) == 1 and text.find(q) == 477
```

Run the same pattern for the other ids; expected `(count, words, offset)`:
A (1,17,477), J (1,13,583), B (1,23,676), H (1,7,848), I (1,10,1069),
F (1,17,2115), G (1,15,3041), C (1,22,3133), D (1,22,3269), E (1,11,3421).
Offsets are valid for the pinned digest only; on a changed digest, re-verify by substring
presence and re-derive offsets.

## Unknowns and scope limits

- Policy authoring/revision date: **unknown** — the page states none, and no public source
  repository or commit was reachable (404; API rate-limited). `Last-Modified` is the GitHub
  Pages artifact time; it is a change detector, not evidence of when the policy was authored
  or last reviewed.
- Whether `Last-Modified` can move on a rebuild without content change: **unknown**; treat
  the body digest as the authoritative content signal and the headers as corroboration.
- This report verifies quotes and exceptions only. It does not assert that CERT/CC applies
  these rules in every case, does not test the site, and does not contact CERT/CC. No
  claim is made about other coordinators' intervals.

Report: .ufo/waves/round-23/build/CvdRecheck.md
