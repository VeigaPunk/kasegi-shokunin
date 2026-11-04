# FIRST PSIRT Services Framework v1.1 — the product-side service catalogue, its maturity definition, and what the document does not state

source: S098 — https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 — "PSIRT Services Framework 1.1" (capture title, L1), capture corpus/source-snapshots/round-65/S098.txt (1573 lines, 170137 bytes; sha256 cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2; opened 2026-11-04, HTTP 200, 229255 fetched bytes); document body L216-L1536 (site navigation column L1537-L1549 and the Downloads sidebar L1550-L1573 are chrome)
verified-at: 2026-11-04 (opened this round; the page states no publication or revision date — the only four-digit years in the body are ISO edition years in the Annex 1 and Glossary citation lists, and the copyright footer is the site's)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098
ground: F44 — FIRST's own catalogue of the services a product incident response team may provide: the four-level spine (service area → service → function → sub-function) over six service areas, three organizational models, and the maturity *definition* the document carries. Not F43 (CERT/CC's phase-to-role matrix), not F06/S018 (multi-party coordination guidelines), and not a maturity-level ladder — the page contains no level vocabulary.

## Scope

This entry covers what the S098 capture actually says. It is a **catalogue of possible
services**, not a requirement set: the frameworks are "high level documents detailing
possible services that computer incident response teams (CSIRTs) and product incident
response teams (PSIRTs) may provide" (E01, L219), and their stated use is "when defining an
initial service catalogue for new teams" (E02, L219). The page says so itself: "The
Frameworks are guides and identify various models, capabilities, services, and outcomes"
(E05, L221), and "In this way, teams are free to implement their own model and to build
capabilities that meet their stakeholder’s unique needs" (E06, L221).

The document is product-side by construction. It was split from the CSIRT Services
Framework because "PSIRTs do provide quite different services and typically operate in quite
different environments" (E03, L220) — "It was thus decided to create a separate document
covering PSIRTs" (E04, L220) — and its own stated differentiator is that "The focus on
products is the key differentiator between the PSIRT of an organization and other incident
response teams represented in the same organization" (E12, L244).

The organization spine is four levels deep: "SERVICE AREAS – SERVICES – FUNCTIONS –
SUB-FUNCTIONS" (E08, L227). The capture defines each level in its own words — service
areas "regroup services related to a common aspect" (E07, L229); a service is "a set of
recognizable, coherent actions towards a specific result on behalf of or for the
constituency of an incident response team" (E09, L231). The document separates *what* is
done from *how*: "Service Areas, Services, and Functions identify what is being done at
different levels of details, while Tasks and Actions identify how it is being done" (E10,
L289).

## The catalogue

The capture's own headings enumerate **six service areas**, **28 services**, **84
functions** and **159 sub-function headings**. Their names, in the capture's own order:

| Service area | Name as the capture carries it | Anchor |
|---|---|---|
| Service Area 1 | Stakeholder Ecosystem Management (named only in prose, L331; the heading at L402 is the bare string "Service Area 1") | E33, L331 |
| Service Area 2 | Vulnerability Discovery (named only in prose, L1184; the heading at L674 is the bare string "Service Area 2") | E34, L1184 |
| Service Area 3 | Vulnerability Triage and Analysis | E29, L843 |
| Service Area 4 | Remediation | E30, L941 |
| Service Area 5 | Vulnerability Disclosure | E31, L1145 |
| Service Area 6 | Training and Education | E32, L1309 |

Two service headings carry the intake and qualification duties that a package review
actually turns on: "Service 2.1 Intake of Vulnerability Reporting" (E35, L680) and "Service
3.1 Vulnerability Qualification" (E36, L849).

Intake is the document's stated main scenario: "For a PSIRT the main scenario is the intake
of reports affecting a stakeholder’s product" (E23, L681). Disclosure-side coordination is
organized as named functions — "Function 5.2.1 Bi-lateral Coordination" (E24, L1195) and
"Function 5.3.1 Release Notes" (E25, L1236) — under the service area "Service Area 5
Vulnerability Disclosure" (E31, L1145). The disclosure area's premise is "It is important
to create a transparent and collaborative environment where vendors, coordinators and
finders can share information with their stakeholders and each other" (E19, L1146), and the
coordination service asks a vendor PSIRT to "make arrangements for sharing vulnerability
information with coordinators or other vendors" (E21, L1212).

Remediation is decided by impact rather than by a fixed interval: "The delivery mechanism
for a remediation should be determined based on impact of the vulnerability to stakeholders
when exploited" (E18, L942).

## Maturity: what the document defines, and what it does not

The capture carries exactly **one** maturity definition, in its Glossary: maturity is "how
effectively an organization executes a particular capability within the mission and
authorities of the organization" (E13, L1510), and it "is a level of proficiency attained
either in actions or tasks or in an aggregate of functions or services" (E14, L1510). It also
states, once, how maturity is *measured*: "Maturity of a PSIRT may be measured via the
availability and efficiency of the difference services prescribed in this service area"
(E15, L675) — quoted with the source's own wording, "difference services prescribed in this
service area" (E45, L675) for "different services".

**The capture contains no maturity levels, stages, or ladder.** Measured over the capture's
document body (L216-L1536): `grep -c -iE 'Maturity Level|Level [0-9]'` returns 0; the words
"Basic", "Intermediate" and "Advanced" appear only as ordinary English prose (for example
"intermediate vendor" at L1159-L1172, "more advanced notice" at L468), never as level
names. The level vocabulary belongs to a *different* FIRST document, which this page's
Downloads sidebar links as "PSIRT Maturity, HTML" (E37, L1553). Any F44 sentence naming a
level, stage, or tier of PSIRT maturity is unsupportable from S098.

## Organizational models and operational foundations

Three organizational models are named: "However, three PSIRT models are used by most
companies: Distributed, Centralized and Hybrid" (E11, L248). The Distributed model's core
responsibility includes "Creating policies, processes procedures and guidelines for the
triage, analysis, remediation, and communication of fixes, mitigations or other advisory
information" (E40, L252); the Centralized model's programme-management role is "PSIRT
Program Management Department: Creates policies, processes procedures and guidelines for the
triage, analysis, remediation, and communication of fixes" (E41, L262).

Before the services come "Operational Foundations" (E26, L309), tiered Strategic /
Tactical / Operational — the tier's first item is "A. Executive Sponsorship" (E27, L316)
and the operational tier's first item is "A. Policies and Procedures" (E28, L386). These
three tiers are *foundation layers*, not maturity levels; the capture does not equate them
to maturity.

## Falsifiable package rules

1. **Catalogue-attribution rule.** When a package invokes this page, cite it as FIRST's
   catalogue of services a PSIRT *may* provide (E01, E02, L219), with the version string
   from the capture title (E43, L1). Do not convert a service, function or sub-function
   into a requirement, and do not import a maturity level from it.
2. **Maturity rule.** Maturity may be quoted only as the Glossary definition (E13, E14,
   L1510) or the measurement statement (E15, L675). A sentence naming Basic/Intermediate/
   Advanced or any numbered level fails against this capture, and its ground, if needed, is
   the separate PSIRT Maturity document (E37, L1553).
3. **Product-side rule.** Read this entry as the *receiving team's* side. The scope is what
   a PSIRT does with a report (E23, E16, E17), not what a finder or a coordinator must do;
   F06/S018 holds the multi-party relationship rules and F43 holds CERT/CC's phase-to-role
   matrix.
4. **No-timeline rule.** The framework asks for negotiated timelines — "The timeline for
   remediation and disclosure should be negotiated as soon as possible" (E22, L1160) — and
   states no interval of its own. Do not read a number into this page.

## Rejected readings

- **"The PSIRT Services Framework defines maturity levels (Basic/Intermediate/Advanced)." —
  rejected.** The capture contains 0 occurrences of "Maturity Level" or "Level N"; its one
  maturity definition is the Glossary entry (E13, E14, L1510), and the level vocabulary sits
  in the separately linked PSIRT Maturity document (E37, L1553). Flip requires a capture of
  that document, not a re-reading of this one.
- **"The framework mandates these services." — rejected.** The page calls the frameworks
  high-level documents of services a team *may* provide (E01, L219) and says teams "are
  free to implement their own model" (E06, L221). The capture contains 0 occurrences of
  "shall" and 0 of "conform", and its three uses of "certification" are staff
  qualifications and a tracking tool (L370, L1319, L1343), not a certification scheme for
  a reader.
- **"This is the multi-party coordination framework." — rejected.** The only FIRST
  cross-reference of that kind on the page is a footnote URL to the *v1.0* multiparty PDF
  (E20, L1531); the coordination content here is the PSIRT's own services — bi-lateral
  coordination (E24, L1195) and vendor-to-vendor remedy planning (E44, L1225). F06/S018
  holds the multiparty guidelines.
- **"This is a CVD phase-and-role model." — rejected.** The capture has no phase model and
  no responsibility matrix: "phase" occurs 3 times in the body and only in the SDL
  sense (L225, L298, L783), the word "role" occurs 14 times and only for staffing and
  incident assignments, and the served HTML contains 0 `<table>` elements. The capture
  states that "Vulnerability intake and triage comprise the case management function of a
  PSIRT" (E16, L844) and that "While the order of operations is very similar among PSIRTs,
  there are variations, such as the exact point when a ‘case’ is created" (E17, L844).
  F43 holds CERT/CC's phase-to-role matrix.

## Limits — what this document does not state

- **No publication or revision date.** The page states none; the only date-bearing line in
  the capture is the site's copyright footer, "Copyright © 2015—2026 by Forum of Incident
  Response and Security Teams, Inc. All Rights Reserved." (E38, L1573). The body's own
  four-digit years are ISO edition years in the Annex 1 and Glossary citation lists
  (L1442-L1445, L1513-L1523) — 2002, 2009, 2013, 2014, 2018 — not a date for this document.
  `verified-at` is an access date, and the "1.1" in the title (E43, L1) is the document
  version the page serves, not a revision history.
- **No maturity levels, stages or ladder** — see the Maturity section above; 0 occurrences
  of "Maturity Level" or "Level N" in the body.
- **No disclosure or remediation interval.** No numeric interval appears anywhere in the
  body (`\b\d+\s*(day|week|month|year|hour)\b` → 0 matches), and the words "day", "days",
  "week" and "deadline" occur only as "day to day" (L284), "every day" (L1283), "day of
  advisory publication" (L1287) and "zero-day" (L504, L723, L1060) — "deadline" occurs 0
  times. Timelines are to be negotiated (E22, L1160).
- **No normative requirement vocabulary.** "shall" occurs 0 times in the capture; "should"
  occurs 138 times on 109 body lines and "must" 30 times on 25 body lines, in the register
  of guidance about what a PSIRT *should* do, not of an external obligation. "conform"
  occurs 0 times and "certification" only 3 times, all of it about staff qualifications
  (L370, L1319) and a tracking tool (L1343) — not a certification scheme for a reader.
  Nothing in the capture grants authority, sets a statutory duty, or states a legal safe
  harbour ("safe harbor" / "safe harbour" occur 0 times).
- **No CVSS, EPSS or SSVC definition.** The capture references CVSS and 30111 only as
  external sources — for example the footnote "ISO/IEC 30111:2013 Information
  technology—Security techniques—Vulnerability handling processes-Terms/Definitions 3.7"
  (E42, L1522). "CVSS" occurs 4 times in the body (L593, L853, L1503, L1532): a
  description of what CVSS does, a glossary gloss, and two citation lines — no metric, no
  vector, no base-score semantics. "EPSS" and "SSVC" occur 0 times in the body.
  Severity ground stays F01 (CVSS), prioritization stays F19 (EPSS) and F20
  (SSVC), and the ISO records stay F11/F38.
- **No figure content.** The capture carries 40 `Figure N:` caption lines for 20 distinct
  figures — 20 in the body and 20 again in the Annex 3 illustration list — and no diagram
  interior ("Figure 9: Vulnerability Qualification Process", L851); the 30 `<img>` elements
  in the served HTML are separate PNG assets. A claim that depends on a figure's arrows or
  ordering is not groundable here.
- **No PDF text layer.** The same document exists as a downloadable PDF ("Also available in
  PDF.", E39, L217); that artifact carries a printed version and date that the HTML
  rendering does not. A date-bearing or page-bearing citation needs its own capture.
- **Two service-area headings lost their titles.** "Service Area 1" (L402) and "Service
  Area 2" (L674) are bare strings in the HTML; their names survive only in prose (E33,
  L331; E34, L1184). A quote asserting a service-area name must come from that prose, not
  from the heading line.
- **The capture is a web rendering, not the artifact.** Body-only wordings differ from the
  PDF's printed wording; the capture pins the served instance, and upstream edits under the
  same URL are possible.

## Scope and limits

- This entry is grounded in the round-65 S098 capture (`corpus/source-snapshots/round-65/
  S098.txt`, sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`).
  EntryS098 captured the page independently with the lane's own
  `corpus/instruments/capture-source.py --kind html` and obtained a byte-identical snapshot
  to ScoutS098's candidate and to the L1's committed capture; the independent open is
  recorded in `.ufo/waves/round-65/w1/EntryS098.md`.
- The recheck compares digest-pinned local bytes and manifest quotes. It does not establish
  upstream freshness, that any team implements any service, or that a particular disclosure
  met any duty.
- Overlap is bounded: F43 (S095) records CERT/CC's adapted phase-to-five-role matrix; F06
  (S018) records FIRST's multi-party coordination guidelines; F01 (S001/S002) records CVSS
  severity; F19 (S053) and F20 (S054) record EPSS and SSVC. The new ground is the
  product-side service catalogue, its organizational models, and the maturity *definition*.
- The entry's sentence-level grounding is audited in
  `.ufo/waves/round-65/w1/EntryS098/claim-table.md` (QUALITY R76), with the gate block in
  `.ufo/waves/round-65/w1/EntryS098/gate.md`.
- Documentation only: these are local package-review rules, not instructions to probe,
  scan, authenticate, submit, contact a target, or execute a vulnerability demonstration.
