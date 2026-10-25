# CnaFix — current CNA Rules wording for counting "Independently Fixable" vulnerabilities (round 23)

Read-only public-document seat. No production file was edited; this report is the only
file written. No subagent dispatched, no admission claimed. Official documents were opened
live on 2026-10-20 (UTC); nothing was taken from a secondary summary. No tool was installed,
so there is no install/update to record.

## Question

The frozen assign asks for the exact normative wording that governs counting CVE IDs for
independently fixable vulnerabilities, keyed to the existing S022 row. The answer must name
the version and date of the official text that is current on 2026-10-20, not merely the
version S022 or its successor S030 happened to capture.

## Verdict

The current official text is **CNA Operational Rules v4.2.6, approved 2026-10-14, effective
2026-10-20**. Its counting rule is mandatory, not recommended:

> **"CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities."**
> — §4.2.11, page 15 of 27, CNA Operational Rules v4.2.6 (11 words)

The production F07 entry still quotes the superseded v4.2.0 sentence ("CNAs SHOULD assign …")
at `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:30`, and S030 still calls
v4.2.0 "current" (`corpus/SOURCES.md:36`). That is falsified by the official v4.2.6 text and
by the CVE Program's own 2026-10-20 notice that v4.2.0 "has been deprecated". S022
(`corpus/SOURCES.md:28`, v4.1.0, effective 2025-05-14) is two versions historical.

## Artifacts opened (observed bytes)

| artifact | URL | HTTP | bytes | SHA-256 |
|---|---|---|---|---|
| CNA Rules v4.2.6 PDF (current) | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | 200 `application/pdf` | 271,367 | `e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22` |
| CNA Rules v4.2.0 PDF (deprecated) | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf | 200 `application/pdf` | 665,517 | `7be61b7fc082c1b388510589d7e2ba86e7b96f908b19fab889e7e9c847b31039` |
| CNA Rules v4.1.0 PDF (S022, historical) | https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf | 200 `application/pdf` | 250,107 | `9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0` |
| CVE site SPA bundle (news + rules HTML) | https://www.cve.org/assets/index-BYO9YwiF.js | 200 | 4,230,438 | `ec9ca65974cdc153ea8d334c272f719b79b8c8f50c339affd8fdd0d6a1d3694f` |

Response metadata for the current PDF (HEAD, `date: Tue, 20 Oct 2026 21:43:09 GMT`):
`last-modified: Tue, 20 Oct 2026 18:15:24 GMT`, `etag: "dccb6759e795f420bec63a9a40ae4a47"`,
`content-length: 271367`, served by AmazonS3 via CloudFront. Two independent GETs returned
the same SHA-256.

`pdfinfo` metadata:

| version | Title | CreationDate | pages | Approved / Effective (title page) |
|---|---|---|---|---|
| 4.2.6 | CVE Numbering Authority (CNA) Operational Rules Version 4.2.6 | 2026-10-20 14:15:45 -03 | 27 | 2026-October-14 / 2026-October-20 |
| 4.2.0 | … Version 4.2.0 | 2026-08-25 16:50:08 -03 | 27 | 2026-August-20 / 2026-August-25 |
| 4.1.0 | … Version 4.1.0 | 2025-05-13 10:39:55 -03 | 23 | Effective May 14, 2025 / approved May 14, 2025 |

The `/ResourcesSupport/AllResources/CNARules` page is a JavaScript single-page application:
the static shell is 880 bytes and the rules/news text ships inside the hashed bundle above.
That is a verifiability caveat, not a second authority: the PDF is the linked official
document, and the bundle is the official website's own rendering of the same rules.

## Exact located quotes — current v4.2.6

All are contiguous substrings of the PDF text after whitespace normalization
(`pdftotext -layout … | tr -s ' \n' ' '`). Word counts are whitespace splits; all ≤25.
Each quote occurs exactly once in the v4.2.6 PDF text. Quotation marks below are
meta-delimiters, not part of the rule text.

| id | section, page | exact quote | words | role |
|---|---|---|---|---|
| Q1 | §4.2.11, p.15 | "CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities." | 11 | Primary counting rule; the sentence a current F07 entry must carry |
| Q2 | §4.2.12, p.15 | "If a CNA is uncertain whether two issues are Independently Fixable, then the CNA SHOULD assign a single CVE ID." | 20 | Default under uncertainty: one ID, not an inflated count |
| Q3 | §4.1.9, p.12 | "To help determine whether separate Vulnerabilities exist, CNAs SHOULD consider whether the Vulnerabilities are Independently Fixable." | 16 | Determination guidance feeding the assignment rule |
| Q4 | §4.2.6, p.14 | "CNAs MUST assign different CVE IDs to separate Vulnerabilities, as determined using the guidance in 4.1." | 16 | General separateness rule, also raised to MUST in v4.2.6 |
| Q5 | §4.2.13(1), p.15 | "MUST NOT assign more than one CVE ID if the Products are vulnerable because they share the vulnerable code." | 19 | Upper bound when products share vulnerable code |
| Q6 | §1.4, p.4 | "Specific terms are defined in the CVE Program Glossary and are capitalized when used in this document." | 17 | Locates the term definition outside the PDF |
| Q7 | CVE Program Glossary entry `glossaryIndependentlyFixable` (website, not PDF) | "A vulnerability is independently fixable when it can be fixed without fixing a separate vulnerability." | 15 | Definition of the operative term; see scope limits |

Q7 is deliberately labelled a glossary entry, not rule text: the PDF's §1.4 defers defined
terms to the CVE Program Glossary, and the term "Independently Fixable" is not itself
defined anywhere in the PDF. Any entry that quotes only the PDF and then glosses the term
without the glossary is incomplete, though the rule sentence remains exactly as quoted.

## Normative change across the three versions

| clause | v4.1.0 (S022) | v4.2.0 (S030) | v4.2.6 (current) |
|---|---|---|---|
| "consider whether … Independently Fixable" | §4.1.10, SHOULD, p.12 | §4.1.9, SHOULD, p.12 | §4.1.9, SHOULD, p.12 |
| "assign different CVE IDs to separate Vulnerabilities" | §4.2.6, SHOULD | §4.2.6, SHOULD | **§4.2.6, MUST, p.14** |
| "assign different CVE IDs to different, Independently Fixable Vulnerabilities" | §4.2.11, SHOULD, p.14 | §4.2.11, SHOULD, p.15 | **§4.2.11, MUST, p.15** |
| "uncertain … SHOULD assign a single CVE ID" | §4.2.12, SHOULD, p.14 | §4.2.12, SHOULD, p.15 | §4.2.12, SHOULD, p.15 |

The v4.2.6 change is stated by the CVE Program itself in the same-day news item, whose
rendered bullets include: `Section 4.2.11 was updated to clarify that: "CNAs MUST assign
different CVE IDs to different, Independently Fixable Vulnerabilities."` The Program calls
this a clarification; the compliance level nevertheless changed from recommended to
mandatory, and a current entry that keeps the SHOULD sentence misstates it.

## Why v4.2.6 is the current text (two official channels)

1. The PDF title page states `Version: 4.2.6`, `Approved date: 2026-October-14`,
   `Effective date: 2026-October-20`, and the PDF was created 2026-10-20.
2. The CVE Program news item "CNA Rules v4.2.6 Now in Effect", dated 2026-10-20, states:
   "The previous version, CNA Rules v4.2.0, has been deprecated." and "CNAs are now required
   to comply with the CNA Rules v4.2.6." (site bundle, paragraph 1).
3. The bulk rules HTML inside the same bundle reproduces §4.2.11 as MUST, matching the PDF.

No official page observed still calls v4.1.0 or v4.2.0 current. v4.1.0 remains served for
historical reading; S022's date/version fields are accurate for that historical document,
not for the present rule.

## Falsifiable findings

**F1 (corpus, current-claim defect).** `corpus/knowledge/cna-assignment-and-vulnerability-
rules.md:30` presents `"CNAs SHOULD assign different CVE IDs to different, Independently
Fixable Vulnerabilities."` as the current §4.2.11 text. Falsifier: that exact sentence does
not occur in the current v4.2.6 PDF (count 0, grep exit 1), while it does occur in v4.2.0
and v4.1.0. A reviewer can reproduce this in one command (below).

**F2 (source row staleness).** `corpus/SOURCES.md:36` says S030 is the v4.2.0 current
requirements row. As of 2026-10-20 that predicate is false: v4.2.0's effective period
(2026-08-25) ended when v4.2.6 took effect. The row's immutable fields (URL, version,
anchor) cannot be edited in place under R8; a new superseding row is required.

**F3 (S022 anchor scope).** S022's anchor is "Sections 3.1 and 4.1" (`corpus/SOURCES.md:28`),
which does not locate the ID-counting clauses at all; they are in §4.2. Its "effective and
approved 2025-05-14" belongs to v4.1.0, where §4.2.11 was SHOULD. Treating S022 as the
current source for counting understates the current requirement by two revisions.

**Bidirectional discriminator (validated).**

| test | v4.2.6 current PDF | v4.1.0 historical PDF |
|---|---|---|
| `grep -cF` Q1 MUST sentence | 1 (exit 0) | 0 (exit 1) |
| `grep -cF` old SHOULD sentence | 0 (exit 1) | 1 (exit 0) |

The strings are mutually exclusive across the two byte streams, so the test distinguishes
the versions rather than merely finding text somewhere. The old SHOULD sentence also occurs
once in v4.2.0.

## Executable recheck (run and observed on 2026-10-20)

Positive (network fetch of the current official PDF; fails closed if the file, digest, or
sentence changes):

```
curl -sSL https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf -o /tmp/cna426.pdf &&
sha256sum /tmp/cna426.pdf &&
pdftotext -layout /tmp/cna426.pdf - | tr -s ' \n' ' ' |
grep -cF '4.2.11 CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities.'
```

Observed: digest `e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22`, output `1`, exit 0.

Negative control on the same bytes (must fail):

```
pdftotext -layout /tmp/cna426.pdf - | tr -s ' \n' ' ' |
grep -cF 'CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities.'
```

Observed: output `0`, exit 1.

Reverse control on the historical bytes (proves the control can fire):

```
curl -sSL https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf -o /tmp/cna410.pdf &&
pdftotext -layout /tmp/cna410.pdf - | tr -s ' \n' ' ' |
grep -cF 'CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities.'
```

Observed: output `1`, exit 0.

Freshness of the version claim (site news; the bundle path must be re-derived because it is
content-hashed):

```
js=$(curl -sS https://www.cve.org/ResourcesSupport/AllResources/CNARules | grep -o '/assets/index-[^"]*\.js' | head -1) &&
curl -sS "https://www.cve.org$js" | python3 -c "import sys; s=sys.stdin.read(); i=s.find('The previous version,'); print(s[i:i+140])"
```

Observed on 2026-10-20: `The previous version, <a …>CNA Rules v4.2.0</a>, has been deprecated.`
The shell is 880 bytes; the text is client-side data, so a bundle change is itself a signal
to re-open the PDF rather than a stable citation anchor.

Snapshot-based alternative (Q7-style, for the writer once it creates S031.txt): add a
manifest record `{"id":"S031","path":"S031.txt","sha256":"<digest of captured text>",
"quotes":[{"id":"Q1","quote":"CNAs MUST assign different CVE IDs to different, Independently
Fixable Vulnerabilities.","location":"CNA Rules 4.2.6, 4.2.11, p.15"}]}` and run
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S031`.
At observation time (2026-10-20T21:46:13Z) `corpus/source-snapshots/round-23/manifest.json`
and `S031.txt` were **absent**; this report does not create them.

## Recommended integration (not performed by this seat)

1. Add a new row, not an edit: `S031 | CVE Numbering Authority Operational Rules v4.2.6 —
   https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | spec | A | CVE Program CNA
   scope, vulnerability determination and assignment in version 4.2.6 | Approved 2026-10-14,
   effective 2026-10-20; §§4.1.9 p.12, 4.2.6 p.14, 4.2.11–4.2.13 p.15 | supersedes S030 — the
   4.2.6 counting rules are MUST, not SHOULD; v4.2.0 is deprecated | mined | 2026-10-20 |
   on-release | corpus/knowledge/cna-assignment-and-vulnerability-rules.md`.
2. In the entry: change the `source:` line to S031; change the §4.2.11 quote at line 30 to Q1
   (MUST); replace the sentence at lines 14–17 that calls 4.2.0 "current" with the v4.2.6
   date/version; keep Q2 and the other quotes. I re-verified every other quoted location in
   v4.2.6 and all pages are unchanged: 3.1.1 p.7, 3.1.4 p.7, 4.1.2 p.11, 4.2.1.1 p.13,
   4.2.12 p.15, 4.2.13(1) p.15, and the §4.1.10 interdependent-condition example p.12.
3. Record the S030 → S031 old→new status/used-by change in the round-23 lesson (R8), and leave
   S022 and S030 immutable as historical rows. Do not describe v4.1.0 or v4.2.0 as current.

## Rejected over-generalizations

- **Rejected:** "The CNA rules require a separate CVE ID for every affected product or every
  distinct bug name." Q5 forbids more than one ID when products share vulnerable code; §4.1.10
  treats interdependent conditions as one vulnerability; Q2 defaults to one ID under
  uncertainty. The rules set a higher bar for splitting than naming distinct weaknesses.
- **Rejected:** "SHOULD → MUST is editorial and can be quoted either way." The level of
  requirement is the operative content; the official change log quotes the MUST sentence, and
  the old sentence is absent from the current PDF. An entry may discuss the historical SHOULD
  text, but must not present it as the current rule.
- **Rejected:** "CNA assignment rules authorize research or establish bounty eligibility."
  These are CNA duties under CVE Program rules; they say nothing about permission to test a
  target, safe harbor, or bounty scope (Q4, Q6).

## Scope limits

- Not an admission decision and not self-credit; F07 remains for L1/integration to admit.
- Clause-level reading, not the comprehensive reading §1.5 says the rules require.
- The term "Independently Fixable" is defined outside the PDF (Q7); the PDF-only quote cannot
  stand alone as a definition.
- The v4.2.6 PDF's own §6 Revision History (p.26) has no 4.2.6 row and still shows the
  placeholder `4.2.0 2026-mm-dd`; the revision dates in this report therefore come from the
  title page, PDF metadata, and the same-day official news item, not from §6.
- Quotes are pinned to the observed bytes/digests above; a changed official file will fail
  the recheck rather than silently pass. No claim is made about CNA behavior, any actual CVE
  assignment, or future versions.
- Only public documentation GETs were performed; no target, portal, account, or CNA was
  contacted. No production file was edited.

## Axes moved

- **depth:verifiability** — exact page-located quotes from the current official PDF, confirmed
  by a second official channel (site rules HTML + change log), with pinned digests and a
  positive/negative/reverse executable discriminator.
- **coverage** — supplies the corrected F07 source path (S031/v4.2.6) and the precise one-line
  entry correction; makes no claim on F06 or F08.

Report: .ufo/waves/round-23/build/CnaFix.md
