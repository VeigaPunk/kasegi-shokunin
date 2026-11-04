# NOTES — candidate S098, FIRST PSIRT Services Framework v1.1

Seat: ScoutS098 (leaf, read-only reconnaissance for C2)
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Round: 65, wave 1. Claims NOT frozen — this is a candidate, not a committed snapshot.
Base master: a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b

---

## 1. The exact URL

```
https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1
```

This is the **HTML rendering** of the framework, served under the FIRST "Standards &
Publications > Service Frameworks > PSIRT Services Framework" tree. The page is the
*landing/rendered* document; the same document also exists as a downloadable PDF at

```
https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Services_Framework_v1.1.pdf
```

The landing page links the PDF with the words "Also available in PDF." (candidate L217).

## 2. Capture method, bytes, sha256, time

### 2.1 Candidate capture (the deliverable)

`S098.candidate.txt` was produced by the **lane's own instrument**, so the bytes are
what the L1 integrator's committed snapshot will contain (same instrument, same
conversion, same deterministic output):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/capture-source.py --id S098 \
  --url "https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1" \
  --out .ufo/waves/round-65/w1/ScoutS098/S098.candidate.txt --kind html
```

Instrument output (verbatim):

```
S098 status=200 fetched_bytes=229255 snapshot_bytes=170137
sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2
utc=2026-11-04T19:26:42Z
```

| item | value |
|---|---|
| HTTP status | 200 |
| fetched bytes (raw HTML) | 229255 |
| snapshot bytes (converted text) | 170137 |
| snapshot sha256 | `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2` |
| snapshot lines | 1573 |
| fetch time (UTC) | 2026-11-04T19:26:42Z |
| content-type | `text/html; charset=UTF-8` |
| raw HTML sha256 | `3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11` |
| `Last-Modified` header | `Mon, 26 Jan 2026 14:43:46 GMT` |
| `Cache-Control` | `public, max-age=3600, s-maxage=3600` |

### 2.2 Determinism re-check (actually run)

The capture was run **twice** (second run to a scratch path) and the snapshot digests
are byte-identical:

```
S098b status=200 fetched_bytes=229255 snapshot_bytes=170137
sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:26:44Z
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  S098b.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  S098.candidate.txt
```

A third fetch with a *different* User-Agent produced the **same raw HTML bytes**
(`cmp` reported identical), so the capture is not UA-dependent:

```
3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11  raw_ua.txt   (UA: kasegi-shokunin/1.0)
3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11  psirt_v11.html (UA: Mozilla/5.0 …)
IDENTICAL bytes across both UAs
```

The raw HTML decodes as **strict UTF-8** with zero replacement characters, and the
converted snapshot contains **0 U+FFFD** — no lossy transcoding anywhere in the chain.

### 2.3 Secondary fetches (cross-checks, not the deliverable)

| artifact | bytes | sha256 | note |
|---|---|---|---|
| `FIRST_PSIRT_Services_Framework_v1.1.pdf` | 2712956 | `be85371ba2bcadbd2243005b610c4652e2e31842ee396cc2117119f8626cba5a` | 91 pages, PDF CreationDate 2021-01-19 |
| `FIRST_PSIRT_Maturity_Document.pdf` | 644190 | `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f` | separate document, see §5 |
| `psirt_maturity_document` (HTML) | 82978 | — | separate document, `Last-Modified` same as the framework page |

## 3. Title / version / date lines

**On the HTML page itself** (the URL under review):

- `<title>` and `og:title` → **`PSIRT Services Framework 1.1`** — the only place the
  version "1.1" appears as a string in the raw HTML.
- `<h1 id="PSIRT-Services-Framework">` → `PSIRT Services Framework` (no version suffix).
- The page carries **no visible publication date, no revision date, and no version
  history table**. `grep` for `April`, `Spring 2020`, `2020`, `2021` in the converted
  text returns **zero** hits in the body. The page has **no `<table>` elements at all**
  (parsed count: 0), so the "document version history" that the PDF carries is absent
  from the HTML.
- The **only** date-bearing line in the whole capture is the copyright footer at
  **L1573**: `Copyright © 2015—2026 by Forum of Incident Response and Security Teams, Inc. All Rights Reserved.`
- The version survives in the body only indirectly, via the **Downloads** list at
  L1550-1573, which lists `v1.1 HTML`, `v1.1 PDF Format`, `v1.0 HTML`, `v1.0 PDF Format`
  and the Arabic/Chinese/French/Spanish/Japanese/Russian v1.1 PDFs, plus `PSIRT
  Maturity, HTML` and `PSIRT Maturity, PDF Format`.
- The last-modified date is available only as an **HTTP response header**, not as
  page content: `Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`.

**Cross-check against the canonical PDF** of the same v1.1 (fetched for verification):

- Cover page (rendered and read): FIRST logo, `Version 1.1`, `TLP:WHITE`, **`Spring 2020`**,
  title `Product Security Incident Response Team (PSIRT) Services Framework`, `Version 1.1`,
  `1 of 91`.
- Every page header/footer carries `Product Security Incident Response Team (PSIRT) Services
  Framework  Version 1.1  https://www.first.org  N of 91` and `TLP:WHITE`.
- `pdfinfo`: Creator `Acrobat PDFMaker 20 para Word`, CreationDate `Tue Jan 19 16:56:29 2021 -03`,
  ModDate `Tue Jan 19 16:57:19 2021 -03`, 91 pages, PDF 1.6.
- **Caution on the PDF text layer:** `pdftotext` emits a stray first line
  `Version 2 (April 202` on page 1 that is **not visible in the rendered page**
  (confirmed by rendering page 1 to PNG and reading it). It is an artefact of an
  off-page/hidden text run, not document content. **Do not cite it.**
- The HTML rendering and the PDF agree on all headings and on the whole service tree
  (see §4), so the HTML is a faithful rendering of the v1.1 PDF — but the HTML is
  *strictly less* as a version/date ground than the PDF.

**Recommendation for the L1:** pin the version from the `<title>` string plus the
Downloads list (both inside the captured bytes), and pin the date from the HTTP
`Last-Modified` header — **not** from page content, which has none. If the L1 wants a
first-party *publication date* for v1.1, that date (`Spring 2020`) is only in the PDF,
which is a different URL and a different capture; treating it as part of the S098 HTML
capture would be a scope error.

## 4. Actual scope and structure of the document

**Scope.** FIRST's Services Frameworks are the FIRST-community's description of the
services a CSIRT or PSIRT *may provide*. The PSIRT document exists as a sibling of the
CSIRT Services Framework, split off because "PSIRTs do provide quite different services
and typically operate in quite different environments" (L220). The frameworks are
described as guides — "teams are free to implement their own model" (L221). The PSIRT
one is explicitly about **products**: "The focus on products is the key differentiator
between the PSIRT of an organization and other incident response teams" (L244).

**Structural spine** (L227): `SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS`.
Each level has a written definition (L229 service areas, L231 services, L235 functions,
L239 sub-functions) and each service/function carries a `Description` +
`Purpose`/`Outcome` template.

**Counts actually measured in the candidate capture:**

| element | count |
|---|---|
| Service Areas | 6 |
| Services | 28 |
| Functions | 84 |
| Sub-Functions | 159 |

**Headings present** (from the parsed DOM, `h1`–`h4`):

- `h1` PSIRT Services Framework
- `h2` Purpose · Introduction · PSIRT Framework Structure · PSIRT Organizational Structure ·
  What does the PSIRT do? · Operational Foundations · **Service Area 1** · **Service Area 2** ·
  **Service Area 3 Vulnerability Triage and Analysis** · **Service Area 4 Remediation** ·
  **Service Area 5 Vulnerability Disclosure** · **Service Area 6 Training and Education** ·
  Annex 1 Supporting Resources · Annex 2 Acknowledgements · Annex 3 Tables and Illustrations ·
  Annex 4 Pros and Cons of PSIRT Organizational Models · Annex 5 Types of Incident Response
  Teams · Glossary · Downloads
- `h3` Definitions · I. Strategic · II. Tactical · III. Operational · + 28 `Service N.N` headings
- `h4` Distributed Model · Centralized Model · Hybrid Model · Other Considerations ·
  Stakeholders · + 84 `Function N.N.N` headings

Note: **Service Area 1 and Service Area 2 headings carry no title text in the HTML**
(L402 is literally `Service Area 1`, L674 is literally `Service Area 2`), whereas
Service Areas 3, 4 and 5 carry their names inline. The names for SA1/SA2 exist only
in prose ("Service Area 1 Stakeholder Ecosystem Management", L331) and in the PDF's
table of contents. A quote that asserts the SA1/SA2 titles must be taken from the
prose or the PDF, not from the heading line.

**Service tree** (service names verified against both the PDF TOC and the HTML):

- **Service Area 1** — Stakeholder Ecosystem Management: 1.1 Internal Stakeholder Management ·
  1.2 Finder Community Engagement · 1.3 Community and Organizational Engagement ·
  1.4 Downstream Stakeholder Management · 1.5 Incident Communications Coordination within
  the Organization · 1.6 Reward Finders with Recognition & Acknowledgement ·
  1.7 Stakeholder Metrics
- **Service Area 2** — Vulnerability Discovery: 2.1 Intake of Vulnerability Reporting ·
  2.2 Identify Unreported Vulnerabilities · 2.3 Monitoring for Product Component
  Vulnerabilities · 2.4 Identifying New Vulnerabilities · 2.5 Vulnerability Discovery Metrics
- **Service Area 3** — Vulnerability Triage and Analysis: 3.1 Vulnerability Qualification ·
  3.2 Established Finders · 3.3 Vulnerability Reproduction
- **Service Area 4** — Remediation: 4.1 Remedy Release Management Plan · 4.2 Remediation ·
  4.3 Incident Handling · 4.4 Vulnerability Release Metrics
- **Service Area 5** — Vulnerability Disclosure: 5.1 Notification · 5.2 Coordination ·
  5.3 Disclosure · 5.4 Vulnerability Metrics
- **Service Area 6** — Training and Education: 6.1 Training the PSIRT · 6.2 Training the
  Development Team · 6.3 Training the Validation Team · 6.4 Continuing Education for all
  Stakeholders · 6.5 Provide Feedback Mechanisms

**Organizational models** (L248): Distributed, Centralized, Hybrid — with the
Distributed/Centralized/Hybrid duties and Annex 4's pros-and-cons table.

**Operational Foundations** (L309-401) are tiered **Strategic / Tactical / Operational**
(I. Strategic: Executive Sponsorship, Stakeholder, PSIRT Charter, Organizational Model,
Management and Stakeholder Support; II. Tactical: Budget, Staff, Resources and Tools;
III. Operational: Policies and Procedures, Evaluation and Improvements). These three
tiers are the closest thing the HTML page has to a maturity ladder — but they are
labelled *Strategic/Tactical/Operational*, **not** levels, and they are a different
axis from maturity (see §5).

## 5. Maturity: what this document does and does NOT define

**This is the single most important negative finding for the L1.**

The HTML page **does not define maturity levels**. Measured on the candidate capture:

- `grep -iE "level [0-9]"` over the body → **0 hits**.
- `grep -iE "Maturity Level|Level [0-9]|maturity model"` → **0 hits** in the body.
- The only "maturity" mentions in the body are:
  - L274 — "As a PSIRT continues to mature and scale…" (organisational change, prose)
  - L403 — "…throughout the lifecycle of an incident or the maturity lifecycle of the PSIRT."
  - L433, L439, L863, L875 — prose uses of "mature" (adjective)
  - L675 — "**Maturity of a PSIRT may be measured via the availability and efficiency of
    the difference services prescribed in this service area.**" (note: the source's own
    typo, "difference services" for "different services" — quoted verbatim)
  - L1499 — Glossary: "Actions — the list of how something is done at varying levels of
    detail / maturity."
  - **L1510** — Glossary: "**Maturity** — how effectively an organization executes a
    particular capability within the mission and authorities of the organization. It is
    a level of proficiency attained either in actions or tasks or in an aggregate of
    functions or services."
  - L1553-1554, L1567-1568 — the **Downloads** links `PSIRT Maturity, HTML` and
    `PSIRT Maturity, PDF Format`.

So the page contributes exactly **one maturity definition**: the **Glossary entry at
L1510**. It defines *maturity as a concept*; it does **not** enumerate levels, stages,
or a ladder.

**The actual maturity levels live in a different FIRST document**, linked from the
Downloads section of this page:
`https://www.first.org/standards/frameworks/psirts/psirt_maturity_document` /
`FIRST_PSIRT_Maturity_Document.pdf` (2019, 29 pages). Its structure (measured from the
PDF text layer) is **Maturity Level 1 (Basic)**, **Maturity Level 2 (Intermediate)**,
**Maturity Level 3 (Advanced)**, plus "Beyond Level 3", with a figure listing desired
Service Areas and Services per level. Its cover reads "Product Security Incident
Response Team (PSIRT) Maturity Document", `FIRST.Org, Inc. (www.first.org)`, 2019.

**Consequence for F44:** if F44 is admitted as "FIRST PSIRT Services Framework v1.1",
the maturity-*level* material is **out of scope** and belongs to a separate candidate
source. The L1 must not let "maturity levels" leak into F44 from this HTML capture —
there is no level vocabulary in it to cite.

## 6. Distinguishishment from the held rows

The following paragraph is the suggested distinguishing ground for F44.

> **F44 — FIRST PSIRT Services Framework v1.1: the product-side service taxonomy that
> a vendor PSIRT is measured against.** This document is FIRST's own description of
> the services a **product** incident response team may provide, organised as a
> four-level spine — *service areas → services → functions → sub-functions* (L227) —
> over six service areas: Stakeholder Ecosystem Management, Vulnerability Discovery,
> Vulnerability Triage and Analysis, Remediation, Vulnerability Disclosure, and Training
> and Education, containing 28 services, 84 functions and 159 sub-functions. Its
> subject is the **vendor's own PSIRT operation**: the Distributed/Centralized/Hybrid
> organisational models, the Operational Foundations tiered Strategic/Tactical/Operational,
> and the per-service Purpose/Outcome templates. Its differentiator from every other
> FIRST document the lane holds is stated by the document itself: "The focus on products
> is the key differentiator between the PSIRT of an organization and other incident
> response teams represented in the same organization" (L244).
>
> It is **not** F43 (CERT/CC's CVD phases and five-role matrix): F43 is a *phase-and-role*
> model of the disclosure process as CERT/CC adapted it from ISO/IEC 30111:2019, with a
> responsibility matrix whose Validation row assigns report validation to Vendor and
> Coordinator. S098 has no phase model and no role matrix — it has a *service
> catalogue*, and it explicitly says the order of operations varies ("there are
> variations, such as the exact point when a 'case' is created", L844).
>
> It is **not** F06/S018 (FIRST's multi-party coordination guidelines): S018 is a
> *recommended practice* for coordinating multiple parties through an upstream/downstream
> web, where the unit of analysis is the party relationship and the clock is negotiated.
> S098's Service Area 5 covers the **same territory from the vendor-PSIRT's side** —
> notification to intermediate vendor/coordinator/finder, bi-lateral and multi-vendor
> coordination, disclosure artefacts (release notes, security advisory) — but it treats
> them as **services the PSIRT itself performs**, with a Service/Function/Sub-Function
> taxonomy and Purpose/Outcome metrics, not as guidelines for how parties should relate.
> S018 is also a different artifact: it is a PDF guidelines document v1.1 (Spring 2020)
> at a `/global/sigs/vulnerability-coordination/multiparty/` URL; S098 is the
> `/standards/frameworks/psirts/` HTML rendering. S018 is not even cited by name on the
> S098 page — the only FIRST cross-reference in S098's footnotes is the multiparty
> *v1.0* PDF URL at L1531.
>
> It is **not** S053/S054 (EPSS / SSVC): EPSS is a published 0–1 exploitation-likelihood
> *score* and SSVC is a decision-point *prioritisation* method; S098 defines no score and
> no prioritisation method at all. It names CVSS once, in Service 3.1 (L853, as a way to
> "capture the principal characteristics of a vulnerability and produce a numerical score
> reflecting its severity") and once in the glossary (L1503) — i.e. it *references* the
> severity scale the lane already holds (F01, S001/S002) without restating it, and it
> contains **no** EPSS scoring content and **no** SSVC decision points. SSVC/EPSS are
> *scoring inputs* a PSIRT consumes; S098 is the *service structure* around them.
>
> Finally it is **not** the maturity document: S098 contains **no maturity levels** —
> only a Glossary definition of the word (L1510) and a link to a separate
> `FIRST_PSIRT_Maturity_Document` (Levels 1–3, 2019) in its Downloads section.

### 6.1 Every held row that could overlap, and why it does not

Overlap candidates were enumerated from the `F01`–`F43` frontier rows in
`corpus/README.md` and the `S001`–`S097` rows in `corpus/SOURCES.md`. The rows whose
subject matter touches a service framework's vocabulary:

| held row | subject | overlap with S098 | why it does not overlap |
|---|---|---|---|
| **F43** (S095) | CERT/CC adapted CVD phase-to-five-role matrix | **Highest overlap.** Both describe a coordinated disclosure workflow; both contain the words "phase", "role", "validation", "remediation". | F43's unit is a **phase → role** matrix with a specific Validation/Remediation/Deployment row assignment (S095.txt:112-116, 129-146). S098 has **no phases and no role matrix**; it has a service/function/sub-function catalogue, and L844 states the order of operations varies between PSIRTs. F43 is also CERT/CC's adaptation of ISO/IEC 30111:2019; S098 is FIRST's own product-team framework and cites 30111 only as a glossary footnote (L1522-1523, "ISO/IEC 30111:2013 … Terms/Definitions 3.7/3.8"; the 29147 footnotes are L1513-1517). |
| **F06** (S018) | FIRST multi-party CVD guidelines v1.1 | **High.** Same publisher (FIRST), same domain (multi-party coordination of vulnerabilities). | F06 is *guidelines for parties*: role/relationship recording, negotiated timelines, upstream/downstream web, and the "upstream fix is not downstream evidence" rule. S098 is a **service catalogue for one organisation's PSIRT**, and its Service Area 5 explicitly frames notification/coordination/disclosure as *services the PSIRT performs* (L1145-1146, L1195, L1210, L1236, L1248). Different URL tree, different artifact type (HTML rendering vs PDF guidelines). See also the S018-vs-S098 footnote gap noted in §6. |
| **S053 / F19** | FIRST EPSS exploitation-likelihood | Medium — same publisher, and both concern what a PSIRT knows about a vulnerability's risk. | EPSS is a published numeric 0–1 probability with a 30-day horizon (S053.txt:216-217). S098 contains **no** EPSS content; "EPSS" appears in the S098 capture only as site-navigation chrome (L153, L1547). S098 cites CVSS (L853, L1503) but not EPSS. EPSS is a scoring artifact; S098 is a service taxonomy. |
| **S054 / F20** | CERT/CC SSVC decision-point categorisation | Medium — both are prioritization-adjacent and both are named in the lane's "keep distinct" clauses. | SSVC is a modular decision-point method producing stakeholder-tailored prioritisation. S098 contains **no** decision points, no "Exposure", no prioritisation scale. It has Service 3.1 "Vulnerability Qualification" with Quality Gate/Bug Bars (L852, L298) — a *threshold* concept for what counts as a vulnerability, which is a different object from a priority category. |
| **F01** (S001/S002) | FIRST CVSS v4 severity & vector | Medium — S098 names CVSS. | S098 references CVSS only as an external reference for severity communication (L593, L853, L1503); it defines no metric, no vector, no score semantics. All CVSS ground stays F01. |
| **F02** (S003-S005) | Coordinated-disclosure timelines | Medium — timelines appear in S098 (L1160, L1190, L1401, L1291). | F02 holds *stated clocks* from specific policies. S098 states **no** numeric timeline; it asks teams to *negotiate* timelines and to define SLAs, without values (L1160, L1190). No number in S098 can be cross-read as a disclosure deadline. |
| **F07** (S031) | CVE CNA operational rules | Low | S098 never mentions CNA, CVE assignment or identifier rules; CVE appears only in the glossary (L1502). |
| **F10** (S036-S040) | Vendor-side disclosure policies as corpus objects | Low-medium — both are "what a vendor's PSIRT does". | F10 reads *a specific vendor's published policy* (Cisco, Hitachi, JPCERT/CC). S098 is FIRST's **generic** framework: it names no vendor, no specific policy, no clock. It is the template against which such policies could be read, not an instance. (This is also the source of the corpus's only other use of the word "PSIRT" — see §7.) |
| **F11 / F38** (S041) | ISO/IEC 29147/30111 division of labour | Low | S098 cites 29147/30111 only in its glossary footnotes (L1516-1521) as definitional sources. It assigns no division of labour between them. |
| **F15** (S048) | Vendor research programme as an intake route | Low-medium — "intake" is a shared word. | F15 is one named programme (Microsoft MSVR) as an intake route for *other vendors' bugs*. S098's Service 2.1 "Intake of Vulnerability Reporting" (L680) is a **generic service** with Functions "Ensure Reachability" (L686) and "Handle Vulnerability Reports" (L704) — the framework's structure, not a specific programme's rules. |
| **F24** (S063) | RFC 9116 security.txt | Low | S098 mentions no machine-readable discovery file for intake. |
| **F21 / F22** (S055, S043) | CSAF/VEX | Low-medium — S098 recommends machine-readable advisories. | L1259 *recommends* publishing advisories in CSAF format; it does not define CSAF, product_status or VEX justification flags. Those stay F21/F22. S098 cites CSAF only as a URL footnote (L1525). |
| **F25 / F30** (S032, S076) | CVE record format / CVE Services API | Low | S098 has no CVE-record schema and no API. |
| **F18** (S052) | CISA KEV | Low | KEV appears in the S098 capture only in navigation chrome; S098 has no KEV content. |
| **F08 / F09 / F03** (S029, S0xx) | CRA duties, authorisation, safe harbor | Low | S098 is a service framework for a PSIRT's own operation; it grants no authority, sets no statutory duty and states no legal safe harbour. |

**Not-overlapping rows** (checked and cleared on a keyword sweep): F04, F05, F13, F14,
F16, F17, F23, F26, F27, F28, F29, F31, F32, F33, F34, F35, F36, F37, F39, F40, F41, F42.
These concern AI-assisted findings, CWE, reward ladders, crowdsourced testing, bounty
classifications, SBOM/CycloneDX, cloud VRP scope, kernel process, GitHub advisories,
OSV, NVD, Scorecard, and Project Zero — none of which the S098 text touches as subject
matter (their keyword hits are the generic words "intake"/"triage"/"disclosure"/"FIRST"
in unrelated contexts, itemised in `scope-screen.txt`).

## 7. Scope screen — summary

Full output (commands, per-term counts, and every file:line hit) is in
`scope-screen.txt` in this directory. Headline counts over the four screened surfaces
(`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md` — 81 files):

| term | case-sensitive lines | case-insensitive lines |
|---|---|---|
| PSIRT | 12 | 12 |
| FIRST | 37 | 204 |
| maturity | **0** | **0** |
| intake | 91 | 93 |
| triage | 59 | 73 |
| remediation | 43 | 49 |
| disclosure | 283 | 315 |
| services framework | **0** | **0** |
| multi-party | 11 | 14 |
| multiparty | 6 | 6 |
| SSVC | 75 | 87 |
| EPSS | 70 | 72 |
| CVD | 40 | 45 |
| CERT/CC | 86 | 86 |

Reading of the two decisive zeros and the two small ones:

- **`maturity` = 0/0.** No frontier row, no source row and no knowledge entry uses the
  word at all. S098's maturity vocabulary (L1499, L1510) is entirely new to the lane.
- **`services framework` = 0/0.** The lane holds no services-framework document of any
  kind. F44 would be the first.
- **`PSIRT` = 12/12.** Every hit is a PSIRT as an **organisation** — Cisco's PSIRT in
  S040 (`corpus/SOURCES.md:46`) and the vendor-disclosure crosswalks
  (`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:1,46,47,48,50,51,52`;
  `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:59,63` — the latter a
  Japanese JPCERT/CC vendor-policy sentence) — plus two ISO crosswalk mentions
  (`corpus/knowledge/iso-29147-and-30111-division-of-labour.md:19`;
  `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:60`). **Not one** hit
  is FIRST's PSIRT Services Framework, and **not one** hit names a service area,
  service, function, sub-function or maturity level.
- **`FIRST` = 37 cs / 204 ci.** The 167-line ci inflation is the English word "first".
  The 37 cs hits are exactly: `PROVINCE.md:78` (F19/EPSS), `corpus/README.md:207` (F06),
  `corpus/README.md:389` (F19), `corpus/SOURCES.md:7,8` (S001/S002 CVSS),
  `corpus/SOURCES.md:24` (S018), `corpus/SOURCES.md:59` (S053), `corpus/SOURCES.md:117,122,123,128,134`
  (source-table prose), and the knowledge entries that cite them
  (`cisa-cvd-program-stages.md:5,54,95,114`; `csaf-vex-product-status-and-justifications.md:125`;
  `cvss-v4-severity-and-vector.md:38,43`; `epss-exploit-prediction-scoring.md:1,10,11,14,83,99,102,110,132,186,196,247`;
  `multiparty-vulnerability-coordination.md:15,44,51,52`; `ufo-archive-2026.md:80`;
  `vendor-third-party-finding-coordination.md:63`). **None** of them is the FIRST
  Service Frameworks standards area — `first.org/standards/frameworks` occurs **zero**
  times anywhere in the lane, and `psirt_services_framework` occurs **zero** times.
- The high-count generics (`intake` 91, `triage` 59, `remediation` 43, `disclosure` 283)
  are **not** evidence of overlap: they are the shared English of the whole
  vulnerability-disclosure domain and are spread across every knowledge entry. Their
  complete file:line listings are in `scope-screen.txt`; the discriminator is the
  document's *unit of analysis* (service catalogue vs phase/role matrix vs guidelines vs
  score), not its vocabulary.

## 8. Flags — is this a good first-party ground?

**Strengths**

- **First-party**: served from `www.first.org` itself, HTTP 200, no paywall, no login,
  no cookie wall, no bot challenge. The whole document body is in the initial HTML
  response (raw fetch = 229255 bytes, converted body = 170137 bytes).
- **Deterministic**: identical snapshot digest on two consecutive captures two seconds
  apart, and identical raw bytes under two different User-Agents.
- **Clean encoding**: strict UTF-8 in, zero U+FFFD out.
- **Not JavaScript-dependent**: the page contains **1** `<script>` tag (the site's
  nav/freshworks widget) and **0** `<noscript>` blocks; all document content is
  server-rendered markup.
- **Structured and quotable**: stable `id` anchors on every heading
  (`id="Service-3-1-Vulnerability-Qualification"`, `id="Glossary"`, …), a stable
  downloadable-PDF cross-reference, and a stable footer.
- **Counterpart artifact available**: the same v1.1 exists as a 91-page PDF with a
  printed version string and a `Spring 2020` date, if the L1 later wants a
  date-bearing capture (as a *separate* source, not as part of S098).

**Weaknesses / cautions**

1. **No in-page version or date.** The version "1.1" appears only in `<title>`,
   `og:title` and the Downloads list; there is **no** publication date, **no**
   revision date, **no** version-history table and **no** `<table>` element anywhere in
   the HTML. The only date in the capture is the copyright range `2015—2026` at L1573,
   and the only date outside the capture is the HTTP `Last-Modified` header. This is a
   **weaker version ground** than most held sources and must be described as such.
2. **Mutable, unversioned URL shape.** The URL embeds the version (`..._v1.1`), which
   helps, but the page also serves the whole "Downloads" list (v1.0 and v1.1 in six
   languages) from the same HTML, and `Last-Modified` is a **site-wide** timestamp
   (identical for the framework page and the maturity page:
   `Mon, 26 Jan 2026 14:43:46 GMT`) — so it reflects a site publish, not a document
   revision. A future re-fetch may serve edited prose under the same URL; the sha256
   pin is the only defence.
3. **No maturity levels in it.** See §5 — the page's one maturity definition (L1510) is
   a glossary entry, and the level ladder lives in a different document. Any F44 claim
   that mentions levels, stages or "Basic/Intermediate/Advanced" would be unsupportable
   from this capture.
4. **Rendering, not the artifact.** The HTML is a web rendering of a Word-produced PDF.
   It has no page numbers, and the 20 figure artworks are **not in the text capture**:
   the `<img>` elements point at separate PNGs under `psfw_media/v1.1/image1.png` …
   `image20.png` (30 `<img>` tags total, all fetched over HTTP 200 — verified for
   `image5.png`: `HTTP/2 200`, `content-type: image/png`, 37667 bytes), so the capture
   carries only the 40 *caption lines* ("Figure 5: General PSIRT Activities", …).
   Two service-area headings also lost their titles. A claim that depends on a figure's
   **content** cannot be grounded in this text capture — only its caption; and the
   figure PNGs are relative-path assets a re-capture does not pin.
5. **Site chrome dominates the byte count.** Lines 1–216 of the capture are
   FIRST's global navigation ("Member Portal", "About FIRST", the CVSS-SIG menu, the
   PSIRT SIG link at L173, the Standards menu at L198-208). Any quote must be pinned
   against the body range (L217-1573) so that a re-capture whose chrome differs does
   not silently move anchors. The lane's own `body_lines` mechanism
   (`corpus/source-snapshots/round-62/manifest.json` shows `body_lines: [56,157]`)
   is the right instrument for that.
6. **Not a normative standard.** The document's own Notice (present in the PDF at
   page 2) says it "describes what the Forum of Incident Response and Security Teams,
   Inc. (FIRST.Org) believes are best practices… for informational purposes only" and
   that FIRST.Org "is not liable for any damages". The HTML page does not carry that
   Notice; the PDF does. The L1 should describe S098 as a **framework/catalogue**,
   never as a requirement.
7. **Minor source typo to preserve.** L675 reads "the availability and efficiency of
   the **difference** services prescribed in this service area" — the source's own
   wording ("difference" for "different"). Quote verbatim; do not silently correct.

## 9. What I did not do

- No production file was read-modified: `PROVINCE.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/*`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
  `QUALITY.md` are untouched. Only `corpus/instruments/capture-source.py` was *run*,
  with `--out` pointed at my own seat directory.
- No commit, no push, no mutating git/jj command. No git fixture was needed.
- No task/subagent dispatch (leaf seat).
- No package was installed; `pdftotext`/`pdftoppm` (poppler) and `python3` with
  `beautifulsoup4` 4.15.0 were already present.
- Scratch `/fast/scratch/hyaku/kasegi-r65/ScoutS098/` was used for the raw HTML, the
  PDF cross-checks and the second capture, and is removed on exit after the receipts
  above are copied into this directory.
