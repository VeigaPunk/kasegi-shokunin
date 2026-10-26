# NIST SP 800-216 on its publication record — a *recommended* federal disclosure framework that formalizes accept/assess/manage locally under federal oversight, scoped to systems under federal control

source: S019 — https://csrc.nist.gov/pubs/sp/800/216/final — capture corpus/source-snapshots/round-40/S019.txt (132 lines, 4,901 bytes; sha256 514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6): publication header L66-L67, "Date Published: May 2023" L74, Planning Note L75, authors L78, Abstract L79-L83, Keywords L86, DOI L91, Download URL L92, Document History L95-L97; L1-L65 and L98-L132 are CSRC site chrome
verified-at: 2026-10-26 (re-opened by me this day: the URL returned HTTP 200, text/html; charset=utf-8, 44,658 raw bytes, raw sha256 1703b2954151b5f3e9dbe53a1da5fd0517ba1852de83b0d76ffafebf74e54b7d at 2026-10-26T21:16:38Z; converting that body with the lane's `corpus/instruments/capture-source.py html_to_text()` reproduced the landed capture byte for byte — 132 lines / 4,901 bytes / sha256 514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6, `cmp` clean. I also fetched the PDF the page links — https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf, HTTP 200, 1,510,851 bytes, sha256 363183f02e9366e63a0913080c6576cb4f10f1b635e0a3f12ad7367d8980b67f at 2026-10-26T21:16:57Z — only to confirm that the recommendations themselves are not in this capture; that PDF is not committed and no quote below comes from it)
ground: core — no frontier row covers a government-side disclosure framework. The nearest are F02 (timeline attribution), F06 (multi-party roles), F10 (vendor policies as corpus objects) and F11 (the ISO/IEC 29147/30111 division of labour), and none of them states a federal intake/assessment/tracking arrangement
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S019   # prints S019:sha256 OK then one S019:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved — a pinned-capture comparison under whitespace collapse, not a fresh network check

## Attribution

This is NIST's publication record for a NIST Special Publication, and both halves of that matter. The document is "NIST SP 800-216" (L66) / "Recommendations for Federal Vulnerability Disclosure Guidelines" (L67), authored by four NIST staff —

> "Kim Schaffer (NIST), Peter Mell (NIST), Hung Trinh (NIST), Isabel Van Wyk (NIST)" — S019.txt:L78

— and its own genre word is "recommends". Nothing on this page is a regulation, a directive or a contractual obligation, and the word `mandatory` does not occur in the capture.

> "This document recommends guidance for establishing a federal vulnerability disclosure framework, properly handling vulnerability reports, and communicating the mitigation and/or remediation of vulnerabilities." — S019.txt:L80

That sentence (which recurs verbatim at L83 under "See full abstract") is also the page's statement of the document's three objects: a framework, the handling of reports, and the communication of mitigation or remediation. The page does not reproduce the recommendations themselves — see "What the page does not carry" below.

## Claim 1 — the subject is a *framework* of formalized actions, not a published policy document

> "Receiving reports on suspected security vulnerabilities in information systems is one of the best ways for developers and services to become aware of issues." — S019.txt:L80

> "Formalizing actions to accept, assess, and manage vulnerability disclosure reports can help reduce known security vulnerabilities." — S019.txt:L80

The verbs are process verbs — accept, assess, manage — and the object is "actions", not a published text. Read against the lane's existing ground, this is the distinction that matters: F10's rows are vendor policy *documents* read as corpus objects, and F03's rows are authorization and scope statements; SP 800-216 recommends the handling arrangement in which such a published statement is one artifact among the reported, assessed and tracked ones. A reader who cites this row for "NIST's VDP template" is citing the wrong object.

## Claim 2 — the architecture is federated: local resolution, federal oversight

> "The framework allows for local resolution support while providing federal oversight" — S019.txt:L80

Two design commitments in one clause: resolution stays with the party that holds the system ("local resolution support"), and oversight is retained at the federal level. Neither is a call for central intake, and neither is a call for purely local handling. Any claim that SP 800-216 centralizes report handling in a federal body contradicts this sentence, and so does a claim that it leaves handling entirely to each unit with no federal layer.

## Claim 3 — the scope boundary is *control*, not software type or geography

> "should be applied to all software, hardware, and digital services under federal control" — S019.txt:L80

Three asset classes — software, hardware, digital services — and one qualifier — under federal control. The scope is therefore wider than "federal agency websites" (hardware and services are named) and narrower than "all software" (the control qualifier is stated once in the sentence and is the only scope limit it carries). The registry row's scope cell ("NIST's federal vulnerability-disclosure framework recommendations") matches; a claim about non-federal systems is an extension, not a reading.

## Claim 4 — the stated benefit is a possibility, and it is NIST's own rationale

> "can help reduce known security vulnerabilities" — S019.txt:L80

The modal is "can help reduce", not "reduces" and not a measured effect. The page reports no study, no baseline and no figure; the document's stated purpose is to recommend guidance. A reader must label this as NIST's first-party rationale (Q4), and must not cite SP 800-216 as evidence that formalizing a VDP reduces vulnerabilities — for that claim the publication record offers a possibility statement, and its evidence would sit in the PDF, which this capture does not contain.

## Claim 5 — the framework's vocabulary is named, not defined, in this capture

> "Federal Coordination Body; findings report; source vulnerability report" — S019.txt:L86

> "vulnerability processing; vulnerability tracking" — S019.txt:L86

The Keywords line carries ten terms of art (advisory, Federal Coordination Body, findings report, source vulnerability report, vulnerability communication, Vulnerability Disclosure, Vulnerability Disclosure Policy, Vulnerability Disclosure Program Office, vulnerability processing, vulnerability tracking). This is useful in exactly one way: it tells a reader which stage names to look for when it reaches the document body. It defines none of them — "Federal Coordination Body" occurs in the capture only inside that keyword list — so no entry may attribute a definition of those terms to this page.

## Claim 6 — the publication record, with two different dates that must not be merged

> "06/07/21: SP 800-216 (Draft)" — S019.txt:L96

> "05/24/23: SP 800-216 (Final)" — S019.txt:L97

> "Date Published: May 2023" — S019.txt:L74

> "Planning Note (05/24/2023):" — S019.txt:L75

> "https://doi.org/10.6028/NIST.SP.800-216" — S019.txt:L91

The page carries a month-granularity publication field ("May 2023", L74), a day-granularity Planning Note (L75), and a Document History with the draft (06/07/21) and the final (05/24/23). The registry row's "published 2023-05-24" is therefore a reading of the Document History entry, not of the Date Published field — a distinction a re-verifier can settle in one grep, and one worth keeping because a revised publication would add a new Document History line while the field would still read "May 2023".

## What the page does not carry

- **No numbered recommendations or section text.** The abstract (L80-L83) and keywords (L86) are the whole substantive content; the body is the linked PDF, which this capture is not.
- **No deadlines.** `deadline` and `timeline` each occur 0 times in the capture: no intake, acknowledgement or disclosure interval is stated here.
- **No severity vocabulary.** `CVSS`, `KEV`, `EPSS` and `CSAF` each occur 0 times.
- **No legal-position statement for researchers.** The only legal-adjacent line is a topic tag naming the "Internet of Things Cybersecurity Improvement Act" (L102), which is a page tag, not a finding about authority.
- **No definition of its own keywords** (Claim 5).

## How a reader uses it

1. **Cite the framework's shape, not its procedure.** Accept/assess/manage, local resolution plus federal oversight, federal-control scope (L80) — that is what these bytes support.
2. **Keep "recommends" in the sentence.** NIST recommends guidance (L80); `mandatory` is absent, and a claim of obligation needs another source.
3. **Do not read "federal" as "universal".** The qualifier is "under federal control" (L80) and it is the only scope limit stated.
4. **Do not present centralization as the design.** The sentence pairs local resolution with federal oversight (L80).
5. **Attribute the rationale as a possibility.** "can help reduce" (L80) is NIST's stated expectation, not a measured result.
6. **Use the keywords as a vocabulary index, then go to the PDF.** Ten named terms (L86), none defined here.
7. **Fix the date you quote.** Final publication 05/24/23 (L97); Date Published May 2023 (L74); draft 06/07/21 (L96).

## Sources overlap — F11 (ISO division of labour), F10 (vendor policy objects), F06 (multi-party roles), F02 (timelines)

`grep -oFi` on the capture gives `federal=9`, `disclosure=11`, `recommends=2`, `NIST=7`, `policy=3`, `CVSS=0`, `KEV=0`, `EPSS=0`, `CSAF=0`, `deadline=0`, `timeline=0`. Lane analysis, not a quote: F11 splits a vendor's outward-facing disclosure standard (29147) from its internal handling process (30111), while SP 800-216 recommends a *federal* arrangement in which both local units and a federal layer have roles — the unit of analysis is a government estate, not a vendor; F10's entries read published vendor policies as first-party statements and this page contains no vendor policy; F06's multi-party roles concern coordination among affected parties, and this page names a "Federal Coordination Body" only as a keyword; F02 compares clocks, and this capture states none.

## Falsifiable rule and checks

**Falsifiable rule.** A statement about SP 800-216 on this record is falsified by any of: (a) calling it mandatory or a regulation, when the document "recommends guidance" (L80) and `mandatory` occurs 0 times; (b) extending its scope beyond federal control, when the only scope qualifier is "under federal control" (L80); (c) describing it as centralized federal handling, when the framework pairs "local resolution support" with "federal oversight" (L80); (d) saying it has been shown to reduce vulnerabilities, when the sentence is "can help reduce" (L80) and no result is reported; (e) attributing procedure or deadlines to this page, when it carries the abstract and keywords only and `deadline`/`timeline` occur 0 times; (f) quoting "Date Published: May 2023" as an exact day, when the day-level final date is the Document History entry 05/24/23 (L97).

**FC-1 — every block-quoted span is verbatim, ≤25 words, and starts on its declared line.** Each `> "…" — S019.txt:Lnn` span was matched under the instrument's normalization (whitespace collapsed, `<u>` markup removed) against the landed capture; observed `spans=14 distinct=14 words_max=24 anchors_ok=14 of 14`. Six of the fourteen are abstract spans that occur 2-3 times in the capture, so each carries its anchor line; the other eight occur once.

**FC-2 — the abstract is triplicated.** L80 is the full abstract, L81 is a truncated copy ending "This…", and L83 is the full abstract again under "See full abstract"; every abstract quote above names L80 (or L83) and is disambiguated by its anchor, which the recheck prints as `anchor=80-ok`.

**FC-3 — the two dates.** `grep -n '06/07/21'` returns L96 and `grep -n '05/24/23'` returns L97 (Document History); `grep -n 'Date Published'` returns L74 ("Date Published: May 2023"); `grep -n 'Planning Note'` returns L75. Three date fields, two granularities, one document.

**FC-4 — the keyword list is ten terms.** L86 contains ten semicolon-separated terms; `grep -c 'Federal Coordination Body'` returns 1 line (L86) — the term is nowhere else in the capture, so it cannot be a definition drawn from prose.

**FC-5 — the substantive body is absent.** `grep -ci 'recommendation'` returns 2, and both are the document title (L1 tag, L67 heading); `grep -c 'recommends'` returns 2 (the abstract at L80 and its repeat at L83); the strings `deadline`, `timeline`, `CVSS`, `KEV`, `EPSS` and `CSAF` each occur 0 times, and the page's only route to the body is the "Download URL" label at L92 plus the DOI at L91 — which is why no claim here describes a procedure.

## Rejected over-generalizations

1. **"NIST requires federal agencies to run a vulnerability disclosure programme."** Rejected: the document "recommends guidance" (L80); `mandatory` occurs 0 times, and the page states no obligation.
2. **"SP 800-216 applies to all software."** Rejected: the scope is "all software, hardware, and digital services under federal control" (L80) — the control qualifier is part of the sentence.
3. **"The framework centralizes report handling in a federal body."** Rejected: it "allows for local resolution support while providing federal oversight" (L80).
4. **"Formalizing a disclosure process is proven to reduce vulnerabilities."** Rejected: the claim is "can help reduce known security vulnerabilities" (L80) — a possibility, with no measurement on the page.
5. **"This page states the framework's intake, assessment and tracking procedure."** Rejected: accept/assess/manage appear as the rationale's process verbs (L80) and the stage names only as keywords (L86); the procedure is in the PDF this capture does not contain.
6. **"SP 800-216 was published on 2023-05-24."** Half-rejected: the final publication is recorded as 05/24/23 in the Document History (L97) and the Planning Note is dated 05/24/2023 (L75), while the page's own Date Published field says only "May 2023" (L74); quoting the exact day requires naming which field it came from.
7. **"The page defines 'Federal Coordination Body'."** Rejected: the term occurs only in the keyword list (L86) and is undefined in the capture.

## Honest limit

- **Publication record, not the publication.** This capture is the CSRC landing page (132 lines, mostly chrome); the recommendations live in the linked PDF, which I fetched only to confirm that they are not on this page (HTTP 200, 1,510,851 bytes, sha256 363183f0…, 2026-10-26T21:16:57Z) and did not commit. No claim above describes SP 800-216's clauses, section numbering or page content.
- **Abstract recurrence.** The abstract appears three times (L80, L81 truncated, L83); quotes carry anchors for that reason, and the recheck reports `occurrences=` per quote.
- **Date granularity.** "Date Published: May 2023" (L74) cannot settle a day; the day-level statements are the Planning Note (L75) and the Document History (L97).
- **No currency claim.** The page is a publication record that NIST can revise; this entry binds the bytes captured on 2026-10-26, and a later revision is a new pin, not a correction.
- **Quotes are whitespace-normalized.** The abstract is a single long line in the capture, so quotes match under collapsed whitespace; punctuation is preserved as captured.
- Documentation only: the capture holds a public publication page, no credential, session or private URL, and this entry quotes none.
