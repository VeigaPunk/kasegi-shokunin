# EntryS098 — F44 sentence claim table (QUALITY R76)

Entry under audit: `.ufo/waves/round-65/w1/EntryS098/first-psirt-services-framework.md`
(the predata draft this seat produced for frontier **F44**, source **S098**).

Capture under audit: `corpus/source-snapshots/round-65/S098.txt` — 1573 lines,
170137 bytes, sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`.
Quote ids `E01`–`E45` are this seat's own ids; each is a verbatim substring of the
capture line named, at most 25 whitespace-delimited words.

**Verdicts.** `GROUNDED` = a pinned quote carries the sentence. `OVERREACH` = the sentence
names an attribute or characterization no quote carries. `UNGROUNDED` = the sentence asserts
something the capture does not state at all.

**Scope note.** This table grades the *content* sentences of the draft entry. Header
metadata (source line, verified-at, recheck command, ground line), the four package rules,
the cross-reference to F43/F06/F01/F19/F20, and the closing documentation-only sentence are
**local method or registry statements**, not claims about the capture; they are listed at
the bottom as `M-method` rows with the registry evidence each rests on. The F43/F06/F19/F20
exclusion sentences are also recorded explicitly (rows R-1..R-4) because they are factual
comparisons between registry rows.

## Method rows (not claims about the capture)

| id | statement | evidence | status |
|---|---|---|---|
| M-1 | Source line: S098, the URL, capture title `PSIRT Services Framework 1.1` at L1, capture path/bytes/sha256, body range L216-L1536 with the navigation column and Downloads sidebar marked as chrome | E43 (L1); `sha256sum`/`wc` over the committed capture; the raw HTML this seat fetched (sha256 `3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11`) places `<div id="sidebar">` after the last document-content line, so L1537 onward is chrome; L1's `w1/L1/manifest-draft.json` is byte-identical to the committed `corpus/source-snapshots/round-65/manifest.json` | GROUNDED (provenance) |
| M-2 | `verified-at: 2026-11-04`; the page states no publication or revision date — the only four-digit years in the body are ISO edition years in the Annex 1 and Glossary citation lists, and the copyright footer is the site's | E38 (L1573); measured over L216-L1536: `20[0-9][0-9]` → 13 occurrences on 12 lines, all ISO edition designations (L1442-L1445, L1513-L1523); `Spring` → 0 | GROUNDED |
| M-3 | `recheck:` line is the lane's own `source-recheck.py` invocation against the committed round-65 manifest | Run by this seat: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098` → 18 OK lines, `RC=0` | GROUNDED (executed) |
| M-4 | `ground: F44` line names the four-level spine, three organizational models and the maturity *definition*, and excludes F43, F06/S018 and a maturity ladder | Rows R-1, R-2, R-3 and C-9 below | GROUNDED |
| M-5 | The four package rules (catalogue-attribution, maturity, product-side, no-timeline) | Each cites the E-quote it operationalises; rows C-1, C-9, C-10, C-13 below | GROUNDED (method derived from the cited rows) |
| M-6 | Documentation-only closing sentence | Local rule, consistent with every other entry in `corpus/knowledge/` | GROUNDED (method) |
| M-7 | The entry's sentence-level grounding is audited in this table, gate block in `gate.md` | File paths in the draft entry's own Scope-and-limits section | GROUNDED (provenance) |
| M-8 | "EntryS098 captured the page independently … and obtained a byte-identical snapshot to ScoutS098's candidate and to the L1's committed capture; the independent open is recorded in `.ufo/waves/round-65/w1/EntryS098.md`" | This seat's own run: `capture-source.py --id S098 --url … --out /fast/scratch/hyaku/kasegi-r65/EntryS098/S098.candidate.txt` → `sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`; identical to `ScoutS098/S098.candidate.txt` and to `corpus/source-snapshots/round-65/S098.txt` by `sha256sum` | GROUNDED (executed) |

## Content rows

| id | entry sentence (abridged) | grounding quote | anchor | words | status | note |
|---|---|---|---|---|---|---|
| C-1 | "It is a catalogue of possible services, not a requirement set: the frameworks are 'high level documents detailing possible services that computer incident response teams (CSIRTs) and product incident response teams (PSIRTs) may provide'" | E01 | L219 | 24 | GROUNDED | quote carries the whole sentence |
| C-2 | "…and their stated use is 'when defining an initial service catalogue for new teams'" | E02 | L219 | 9 | GROUNDED | |
| C-3 | "The page says so itself: 'The Frameworks are guides and identify various models, capabilities, services, and outcomes'" | E05 | L221 | 12 | GROUNDED | |
| C-4 | "…'In this way, teams are free to implement their own model and to build capabilities that meet their stakeholder's unique needs'" | E06 | L221 | 21 | GROUNDED | |
| C-5 | "It was split from the CSIRT Services Framework because 'PSIRTs do provide quite different services and typically operate in quite different environments'" | E03 | L220 | 13 | GROUNDED | |
| C-6 | "— 'It was thus decided to create a separate document covering PSIRTs'" | E04 | L220 | 11 | GROUNDED | |
| C-7 | "…its own stated differentiator is that 'The focus on products is the key differentiator between the PSIRT of an organization and other incident response teams represented in the same organization'" | E12 | L244 | 24 | GROUNDED | |
| C-8 | "The organization spine is four levels deep: 'SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS'" | E08 | L227 | 8 | GROUNDED | the four names and their order are the quote's own |
| C-9 | "service areas 'regroup services related to a common aspect'" | E07 | L229 | 9 | GROUNDED | |
| C-10 | "a service is 'a set of recognizable, coherent actions towards a specific result on behalf of or for the constituency of an incident response team'" | E09 | L231 | 25 | GROUNDED | at the 25-word bound |
| C-11 | "'Service Areas, Services, and Functions identify what is being done at different levels of details, while Tasks and Actions identify how it is being done'" | E10 | L289 | 25 | GROUNDED | at the 25-word bound; the capture's own "details" typo is preserved |
| C-12 | "The capture's own headings enumerate six service areas, 28 services, 84 functions and 159 sub-function headings." | *(no quote — a count)* | heading lines L402, L674, L843, L941, L1145, L1309 / service headings L409-L1236 / function headings / sub-function headings L422-L1434 | — | GROUNDED (by count, not by quote) | Counts re-derived by this seat over the committed capture: `grep -c '^Service Area [0-9]'` = 6, `grep -c '^Service [0-9]'` = 28, `grep -c '^Function '` = 84, `grep -ci '^sub-function [0-9]'` = 159 (158 distinct numbers: L1242 and L1244 both carry `5.3.1.1`; L570 and L572 carry a five-level `1.5.1.1.2`/`1.5.1.1.3`). The entry states the *count* and does not assert that the capture numbers them 6/28/84/159 — the counts are the re-derivation. |
| C-13 | "Service Area 1 — Stakeholder Ecosystem Management (named only in prose, L331; the heading at L402 is the bare string 'Service Area 1')" | E33 | L331 | 6 | GROUNDED | the parenthetical about the bare heading at L402 is verified by `sed -n '402p'` |
| C-14 | "Service Area 2 — Vulnerability Discovery (named only in prose, L1184; the heading at L674 is the bare string 'Service Area 2')" | E34 | L1184 | 5 | GROUNDED | same check at L674 |
| C-15 | "Service Area 3 Vulnerability Triage and Analysis" | E29 | L843 | 7 | GROUNDED | title inline in the heading |
| C-16 | "Service Area 4 Remediation" | E30 | L941 | 4 | GROUNDED | |
| C-17 | "Service Area 5 Vulnerability Disclosure" | E31 | L1145 | 5 | GROUNDED | |
| C-18 | "Service Area 6 Training and Education" | E32 | L1309 | 6 | GROUNDED | |
| C-19 | "'Service 2.1 Intake of Vulnerability Reporting'" | E35 | L680 | 6 | GROUNDED | the only quote in the set that is **not** unique: `occurrences=2` (the second is the Operational Foundations cross-reference at L382, "see Service 2.1 Intake of Vulnerability Reporting"). It carries an anchor, and the instrument's B2 limb resolves it: the recheck prints `occurrences=2 anchor=680-ok`. |
| C-20 | "'Service 3.1 Vulnerability Qualification'" | E36 | L849 | 4 | GROUNDED | |
| C-21 | "Intake is the document's stated main scenario: 'For a PSIRT the main scenario is the intake of reports affecting a stakeholder's product'" | E23 | L681 | 15 | GROUNDED | |
| C-22 | "'Function 5.2.1 Bi-lateral Coordination'" | E24 | L1195 | 4 | GROUNDED | |
| C-23 | "'Function 5.3.1 Release Notes'" | E25 | L1236 | 4 | GROUNDED | |
| C-23a | "The disclosure area's premise is 'It is important to create a transparent and collaborative environment where vendors, coordinators and finders can share information with their stakeholders and each other'" | E19 | L1146 | 24 | GROUNDED | at the 25-word bound |
| C-23b | "…the coordination service asks a vendor PSIRT to 'make arrangements for sharing vulnerability information with coordinators or other vendors'" | E21 | L1212 | 17 | GROUNDED | |
| C-23c | "Remediation is decided by impact rather than by a fixed interval: 'The delivery mechanism for a remediation should be determined based on impact of the vulnerability to stakeholders when exploited'" | E18 | L942 | 19 | GROUNDED | the "rather than by a fixed interval" half is the absence measured in C-48 |
| C-24 | "The capture carries exactly **one** maturity definition, in its Glossary: maturity is 'how effectively an organization executes a particular capability within the mission and authorities of the organization'" | E13 | L1510 | 16 | GROUNDED | "exactly one" is a count over the capture: the string `Maturity -` as a glossary headword occurs exactly once (L1510). The capture has 11 lines containing "maturity" in any case — L122-L124 (site navigation, "CTI Maturity model"), L274 (prose "continues to mature and scale"), L403 ("the maturity lifecycle of the PSIRT"), L675 (the measurement statement, C-26), L1499 (the glossary entry for "Actions"), **L1510 (the definition)**, L1553/L1554/L1568 (the Downloads sidebar links) — and none of the other ten is a definition. |
| C-25 | "…and it 'is a level of proficiency attained either in actions or tasks or in an aggregate of functions or services'" | E14 | L1510 | 20 | GROUNDED | second sentence of the same glossary entry |
| C-26 | "It also states, once, how maturity is *measured*: 'Maturity of a PSIRT may be measured via the availability and efficiency of the difference services prescribed in this service area'" | E15 | L675 | 21 | GROUNDED | source's own "difference services" typo preserved and flagged in the entry |
| C-27 | "**The capture contains no maturity levels, stages, or ladder.** Measured over the capture's document body (L216-L1536): `grep -c -iE 'Maturity Level\|Level [0-9]'` returns 0; the words 'Basic', 'Intermediate' and 'Advanced' appear only as ordinary English prose (for example 'intermediate vendor' at L1159-L1172, 'more advanced notice' at L468), never as level names." | *(no quote — an absence)* | L216-L1536 | — | GROUNDED (by absence, measured) | `grep -iE 'Maturity Level\|Level [0-9]'` over the body → 0. Body hits for the three words: "basic/basics" 7 lines (L285, L335, L1315, L1321, L1326, L1389, L1423), "Intermediate" 8 lines (all `intermediate vendor`, L1159-L1172), "Advanced" 2 lines (L468, L1283) — every one ordinary prose, none a level name. |
| C-28 | "The level vocabulary belongs to a *different* FIRST document, which this page's Downloads sidebar links as 'PSIRT Maturity, HTML'." | E37 | L1553 | 3 | GROUNDED | the link text is the quote; the served anchor `href` is `/standards/frameworks/psirts/psirt_maturity_document` (read from the raw HTML this seat fetched, sha256 `3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11`). L1553 sits in the page's `id="sidebar"` Downloads block, i.e. site chrome rather than document body — the entry says "sidebar" for that reason, and the quote is a chrome anchor, not a document-body anchor. |
| C-29 | "Any F44 sentence naming a level, stage, or tier of PSIRT maturity is unsupportable from S098." | *(derived from C-27 + C-28)* | — | — | GROUNDED (rule) | a review rule, not a new fact; follows from the two rows above |
| C-30 | "Three organizational models are named: 'However, three PSIRT models are used by most companies: Distributed, Centralized and Hybrid.'" | E11 | L248 | 13 | GROUNDED | |
| C-31 | "The Distributed model's core responsibility includes 'Creating policies, processes procedures and guidelines for the triage, analysis, remediation, and communication of fixes, mitigations or other advisory information'" | E40 | L252 | 20 | GROUNDED | source's own "processes procedures" wording preserved |
| C-32 | "…the Centralized model's programme-management role is 'PSIRT Program Management Department: Creates policies, processes procedures and guidelines for the triage, analysis, remediation, and communication of fixes'" | E41 | L262 | 19 | GROUNDED | |
| C-33 | "Before the services come 'Operational Foundations'" | E26 | L309 | 2 | GROUNDED | |
| C-34 | "…tiered Strategic / Tactical / Operational — the tier's first item is 'A. Executive Sponsorship'" | E27 | L316 | 3 | GROUNDED | the three tier labels are the capture's own section headings at L315 ("I. Strategic"), L356 ("II. Tactical"), L385 ("III. Operational"); only the first sub-item of the first and third tiers is quoted, and the entry does not claim the items of the middle tier |
| C-35 | "…and the operational tier's first item is 'A. Policies and Procedures'." | E28 | L386 | 4 | GROUNDED | |
| C-36 | "…these three tiers are *foundation layers*, not maturity levels; the capture does not equate them to maturity." | *(derived from C-27, C-33..C-35)* | — | — | GROUNDED (rule) | absence measured: no capture line places Strategic/Tactical/Operational in a maturity ladder; the only "maturity" uses are C-24, C-26 and the prose hits listed in C-27 |
| C-37 | "The framework asks for negotiated timelines — 'The timeline for remediation and disclosure should be negotiated as soon as possible' — and states no interval of its own." | E22 | L1160 | 13 | GROUNDED | the "no interval" half is an absence: `grep -c -iE 'days\|week\|deadline'` over the body → 0, and no numeric interval appears anywhere in the body |
| C-38 | "The capture contains 0 occurrences of 'Maturity Level' or 'Level N'; its one maturity definition is the Glossary entry …, and the level vocabulary sits in the separately linked PSIRT Maturity document." | E13, E14, E37 | L1510, L1553 | 16/20/3 | GROUNDED | see C-24, C-27, C-28 |
| C-39 | "The page calls the frameworks high-level documents of services a team *may* provide … and says teams 'are free to implement their own model'." | E01, E06 | L219, L221 | 24, 21 | GROUNDED | |
| C-40 | "The capture contains 0 occurrences of 'shall' and 0 of 'conform', and its three uses of 'certification' are staff qualifications and a tracking tool (L370, L1319, L1343), not a certification scheme for a reader." | *(absence)* | L1-L1573 | — | GROUNDED (by absence, measured) | `grep -c -i '\bshall\b'` over the whole capture → 0; `grep -c -i 'conform'` → 0; "certification" occurs 3 times (L370 "certifications" in a staff-qualifications list, L1319 "leading security certifications", L1343 "certified tracking tools"). **Correction made during drafting:** an earlier draft of this row claimed "no certification or compliance vocabulary", which was false — the capture does use both words (compliance 6×, at L282, L303, L893, L1326, L1404, L1405, always about the organization's own policies or regulatory training). The row now names the actual occurrences. |
| C-41 | "The only FIRST cross-reference of that kind on the page is a footnote URL to the *v1.0* multiparty PDF" | E20 | L1531 | 1 | GROUNDED | the capture's only `first.org/global/sigs/vulnerability-coordination` occurrence; the URL's own `v1.0` is in the quote |
| C-42 | "…the coordination content here is the PSIRT's own services — bi-lateral coordination … and vendor-to-vendor remedy planning." | E24, E44 | L1195, L1225 | 4, 23 | GROUNDED | |
| C-43 | "The capture has no phase model and no responsibility matrix: 'phase' occurs 3 times in the body and only in the SDL sense (L225, L298, L783), the word 'role' occurs 14 times and only for staffing and incident assignments, and the served HTML contains 0 `<table>` elements. It states that 'Vulnerability intake and triage comprise the case management function of a PSIRT'" | E16 | L844 | 12 | GROUNDED | the "no phase model / no responsibility matrix" half is an absence, measured: `\bphase\b` → 3 body lines, all SDL-sense ("maintenance phase of the SDL" L225, "next phase of development" L298, L783); `\brole\b` → 14 body lines (L285, L371, L411, L1310, L1370, L1381, L1383, L1389, L1395, L1401, L1407, L1413, L1419, L1431), all staffing, training or incident-role assignments; `<table` count in the served raw HTML = 0. **Correction made during drafting:** an earlier draft of this row said "`grep -c 'Role'` → 2" and omitted that lowercase "role" occurs 14 times — the claim is about the *absence of a matrix*, not of the word, and the row now says so. |
| C-44 | "…and that 'While the order of operations is very similar among PSIRTs, there are variations, such as the exact point when a 'case' is created'" | E17 | L844 | 23 | GROUNDED | the capture's own curly quotes preserved |
| C-45 | "The page states none; the only date-bearing line in the capture is the site's copyright footer, 'Copyright © 2015—2026 by Forum of Incident Response and Security Teams, Inc. All Rights Reserved.' The body's own four-digit years are ISO edition years in the Annex 1 and Glossary citation lists (L1442-L1445, L1513-L1523) — 2002, 2009, 2013, 2014, 2018 — not a date for this document." | E38 | L1573 | 15 | GROUNDED | the "page states no date" half is an absence, measured: `20[0-9][0-9]` → 13 occurrences on 12 body lines, every one an ISO/standard edition designation inside the Annex 1 supporting-resources list (L1442-L1445) and the Glossary footnote URLs (L1513-L1523); none is a publication or revision date for the framework. **Correction made during drafting:** an earlier draft of this row claimed `grep -cE '20[0-9][0-9]'` over the body returned 0, which was false — it returns 12 lines. The row now names the actual occurrences and the entry distinguishes them. |
| C-46 | "…the '1.1' in the title is the document version the page serves, not a revision history." | E43 | L1 | 4 | GROUNDED | the "not a revision history" half is an absence: no `<table>` element and no version-history section in the served HTML; the Downloads block (L1550-L1572) lists `v1.1 HTML`/`v1.1 PDF Format` and `v1.0 HTML`/`v1.0 PDF Format` but no dated history |
| C-47 | "No maturity levels, stages or ladder … 0 occurrences of 'Maturity Level' or 'Level N' in the body." | *(absence)* | L216-L1536 | — | GROUNDED (by absence, measured) | see C-27 |
| C-48 | "No disclosure or remediation interval. No numeric interval appears anywhere in the body (`\b\d+\s*(day\|week\|month\|year\|hour)\b` → 0 matches), and the words 'day', 'days', 'week' and 'deadline' occur only as 'day to day' (L284), 'every day' (L1283), 'day of advisory publication' (L1287) and 'zero-day' (L504, L723, L1060) — 'deadline' occurs 0 times. Timelines are to be negotiated." | E22 + absence | L1160 | 13 | GROUNDED | **Correction made during drafting:** an earlier draft of this row claimed 0 occurrences of "days"/"week"/"deadline", which was false — the body has 7 such word occurrences on 6 lines, but every one is the idiom "day to day", "every day", "day of advisory publication" or the compound "zero-day", and **no numeric interval** appears (`\d+\s*(day|week|month|year|hour)` → 0 matches over the body). The row now states the measured facts instead of a false zero. |
| C-49 | "'shall' occurs 0 times in the capture; 'should' occurs 138 times on 109 body lines and 'must' 30 times on 25 body lines, in the register of guidance about what a PSIRT *should* do, not of an external obligation." | *(absence + counted modal)* | L216-L1536 | — | GROUNDED (by count, measured) | `\bshall\b` over the whole capture → 0 occurrences; `\bshould\b` → 138 occurrences on 109 body lines; `\bmust\b` → 30 occurrences on 25 body lines. **Correction made during drafting:** the first draft quoted the line counts (109 / 25) as if they were occurrence counts; the entry now states both figures and names which is which. The reading of that register as guidance is the entry's own characterisation of the source's own "The Frameworks are guides" (E05, C-3). |
| C-50 | "Nothing in the capture grants authority, sets a statutory duty, or states a legal safe harbour ('safe harbor' / 'safe harbour' occur 0 times)." | *(absence)* | L1-L1573 | — | GROUNDED (by absence, measured) | `grep -c -i 'safe harbor'` = 0 and `grep -c -i 'safe harbour'` = 0; the capture states no obligation on any reader (`shall` = 0, C-40) |
| C-51 | "No CVSS, EPSS or SSVC definition. The capture references CVSS and 30111 only as external sources — for example the footnote 'ISO/IEC 30111:2013 Information technology—Security techniques—Vulnerability handling processes-Terms/Definitions 3.7'. 'CVSS' occurs 4 times in the body (L593, L853, L1503, L1532): a description of what CVSS does, a glossary gloss, and two citation lines — no metric, no vector, no base-score semantics. 'EPSS' and 'SSVC' occur 0 times in the body." | E42 | L1522 | 8 | GROUNDED | the "no definition" half is an absence, measured over L216-L1536: `CVSS` → 4 body lines (L593 a cross-reference to a VEX statement, L853 the CVSS sentence in Function 3.1.1, L1503 the glossary gloss "a numerical score that reflects a vulnerability's severity", L1532 the `first.org/cvss/` footnote URL); `EPSS` → 0 body lines (its two capture hits, L153 and L1547, are site navigation); `SSVC` → 0 body lines. No vector, metric or base-score semantics is defined anywhere. |
| C-52 | "The capture carries 40 `Figure N:` caption lines for 20 distinct figures — 20 in the body and 20 again in the Annex 3 illustration list — and no diagram interior ('Figure 9: Vulnerability Qualification Process', L851); the 30 `<img>` elements in the served HTML are separate PNG assets." | *(no quote — a count + an absence)* | L851 | — | GROUNDED (by count and absence, measured) | `grep -c -E '^Figure [0-9]+:'` over the body → 40 lines, with 20 distinct figure numbers; 20 of those caption lines are in the body and 20 are the Annex 3 "Tables and Illustrations" list (L1467-L1489), i.e. the same 20 titles twice. The served HTML carries 30 `<img>` elements pointing at separate PNG assets (`psfw_media/v1.1/image*.png`), so no diagram interior is in the text capture. The L851 caption is quoted verbatim in the entry text, not as a manifest quote. |
| C-53 | "No PDF text layer. The same document exists as a downloadable PDF ('Also available in PDF.'); that artifact carries a printed version and date that the HTML rendering does not. A date-bearing or page-bearing citation needs its own capture." | E39 | L217 | 4 | GROUNDED | the link's `href` is `/standards/frameworks/psirts/FIRST_PSIRT_Services_Framework_v1.1.pdf` (read from the raw HTML this seat fetched); the "printed version and date" refers to the PDF artifact ScoutS098 fetched and read (its own receipt), not to this capture |
| C-54 | "Two service-area headings lost their titles. 'Service Area 1' (L402) and 'Service Area 2' (L674) are bare strings in the HTML; their names survive only in prose." | E33, E34 | L331, L1184 | 6, 5 | GROUNDED | see C-13, C-14 |
| C-55 | "The capture is a web rendering, not the artifact. Body-only wordings differ from the PDF's printed wording; the capture pins the served instance, and upstream edits under the same URL are possible." | *(no quote — a structural limit)* | — | — | GROUNDED (structural) | a statement about the capture's own kind, not about a fact in it; the sha256 pin is the only defence against a same-URL edit. The URL embeds the version, which is stated in the source line (M-1). |
| C-56 | "Severity ground stays F01 (CVSS), prioritization stays F19 (EPSS) and F20 (SSVC), and the ISO records stay F11/F38." | *(registry rows)* | `corpus/README.md` F01, F19, F20, F11, F38 | — | GROUNDED (registry) | frontier rows read from `corpus/README.md`; F01 at line 202, F11 at 212, F19 at 389, F20 at 416, F38 at 938 |
| C-57 | "Overlap is bounded: F43 (S095) records CERT/CC's adapted phase-to-five-role matrix; F06 (S018) records FIRST's multi-party coordination guidelines; F01 (S001/S002) records CVSS severity; F19 (S053) and F20 (S054) record EPSS and SSVC." | *(registry rows)* | `corpus/README.md` F43, F06; `corpus/SOURCES.md` S095, S018, S001, S002, S053, S054 | — | GROUNDED (registry) | F43 at `corpus/README.md:1031`, F06 at `:207`; SOURCES rows S095, S018, S001, S002, S053, S054 all present |
| C-58 | "The new ground is the product-side service catalogue, its organizational models, and the maturity *definition*." | *(derived)* | C-8, C-30, C-24 | — | GROUNDED (rule) | follows from the cited rows |

## Cross-reference rows (registry comparisons — factual)

| id | statement | evidence | status |
|---|---|---|---|
| R-1 | "Not F43 (CERT/CC's phase-to-role matrix)" | `corpus/README.md:1031` F43 "CERT/CC adapted CVD phase-to-five-role matrix: Reporter fix confirmation versus Vendor/Coordinator report validation", entry `corpus/knowledge/cert-guide-cvd-phases-and-validation.md`, source S095. The S098 capture has no phase model and no role matrix (C-43); F43's subject is absent from S098. | GROUNDED |
| R-2 | "not F06/S018 (multi-party coordination guidelines)" | `corpus/README.md:207` F06 "Multi-party CVD — FIRST guidelines v1.1", source S018. S098's only FIRST coordination cross-reference is the v1.0 multiparty PDF URL (E20, C-41); the guidelines document is not the subject of this capture. | GROUNDED |
| R-3 | "not a maturity-level ladder — the page contains no level vocabulary" | C-27, C-28 measured over the capture; the level vocabulary lives in the separately linked document. | GROUNDED |
| R-4 | "not F43 … and the only FIRST cross-reference of that kind on the page is a footnote URL to the *v1.0* multiparty PDF" | E20 at L1531; the capture contains exactly one `first.org/global/sigs/vulnerability-coordination` occurrence. | GROUNDED |

## Counts

| status | rows |
|---|---|
| GROUNDED | 73 (61 content rows `C1`-`C58` incl. `C23a`-`C23c`, 8 method rows `M1`-`M8`, 4 cross-reference rows `R1`-`R4`) |
| OVERREACH | 0 |
| UNGROUNDED | 0 |

Every content row is graded. Rows graded **by count** or **by absence** rather than by a
pinned quote are marked as such above, and each carries the exact command or measurement
that reproduces it; they are not silently passed as quote-grounded.

## Weakening decisions

Recorded in full in `NOTES.md` in this directory. Summary of the sentences this seat had to
weaken during drafting, and the row each maps to:

1. "the maturity *levels* (Basic / Intermediate / Advanced) of the PSIRT Services Framework"
   → weakened to "the capture carries exactly one maturity *definition*" (C-24..C-28). The
   level vocabulary is in a different document this seat did not capture.
2. "159 sub-functions" → weakened to "159 sub-function headings" (C-12), because two
   headings share the number `5.3.1.1` (L1242, L1244) and two carry a five-level number.
3. "the service areas are named Service Area 1 … 6" → weakened to the six names with the
   two prose-only titles marked as such (C-13, C-14, C-54).
4. "the framework defines what a PSIRT must do" → weakened to "the frameworks are
   high-level documents detailing possible services" (C-1, C-39).
5. "a maturity ladder of three levels" → weakened to the Strategic/Tactical/Operational
   *foundation* tiers with an explicit non-equivalence statement (C-33..C-36).
6. "the framework sets disclosure deadlines" → weakened to "asks for negotiated timelines …
   and states no interval of its own" (C-37, C-48).

## Verification actually performed

- Quote set re-derived by this seat from the committed capture; every quote is a verbatim
  substring of its anchored line, every quote is at most 25 whitespace-delimited words
  (maximum observed: 25, at E09 and E10), and every quote has at least 12 normalized
  characters (the `source-recheck.py` floor). Result: 45/45 pass, 0 failures.
- The proposal was then exercised against the **real instrument** over a copy of the
  committed capture:
  `python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S098`
  → `S098:sha256 OK` plus 45 quote lines, `RC=0`. 44 of the 45 print
  `occurrences=1 anchor=N-ok`; the 45th, E35, prints `occurrences=2 anchor=680-ok` — the
  non-unique quote the instrument's B2 limb resolves by anchor (see row C-19).
- The **committed** round-65 manifest was also run unmodified:
  `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098`
  → `S098:sha256 OK` plus 18 `Q…OK` lines, `RC=0`.
- Absence and count measurements were run over the capture's document body (L216-L1536)
  and over the whole capture where the sentence says so; each command is named in the row
  that depends on it.
- The proposal file shipped alongside this table,
  `manifest-assertions-proposal.json`, is the exact file exercised above (copied into the
  scratch directory beside a copy of the committed capture, unmodified).

**Not run by this seat:** any frontier counter, census, claim-package gate, freeze check or
score movement. This seat produced documentation drafts only; nothing here is admitted by
itself, and no score is claimed.
