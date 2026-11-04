# EntryS098 — NOTES: every sentence weakened, and every correction made

Seat: EntryS098 (leaf scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round 65, wave 1. **Predata draft — nothing here is admitted by itself.**

Entry: `first-psirt-services-framework.md` (this directory).
Sentence table: `claim-table.md` (this directory).
Gate block: `gate.md` (this directory).

This file records two distinct things, kept apart on purpose:

* **Part 1 — weakened sentences**: sentences whose first, stronger draft was not
  supportable by the capture, together with the weaker form that shipped and the reason.
* **Part 2 — corrections**: sentences this seat wrote into the draft, then caught and fixed
  by re-measuring. These were *errors*, not stylistic choices; each is listed with the false
  statement, the measurement that refuted it, and the corrected statement.

---

## Part 1 — sentences that had to be weakened

### W-1 — "the maturity levels (Basic / Intermediate / Advanced) of the PSIRT Services Framework"

**Stronger draft.** "The framework defines three maturity levels — Basic, Intermediate and
Advanced — for a product incident response team."

**Why it could not stand.** The S098 capture contains **no** maturity level vocabulary.
Measured over the document body (L216-L1536): `grep -c -iE 'Maturity Level|Level [0-9]'` → 0.
The words "basic", "intermediate" and "advanced" appear 7, 8 and 2 times respectively, and
every occurrence is ordinary English prose ("basic program elements" L335, "intermediate
vendor" L1159-L1172, "more advanced notice" L468) — never a level name. The level ladder
belongs to a *separate* FIRST document that this page merely links from its Downloads
sidebar as "PSIRT Maturity, HTML" (L1553).

**Weakened to.** "The capture carries exactly **one** maturity definition, in its
Glossary" — the definition at L1510 — plus the measurement statement at L675, and the
Limits section states that the page contains no maturity levels, stages or ladder.

**Maps to** claim-table rows C-24, C-25, C-26, C-27, C-28, C-29.

### W-2 — "159 sub-functions"

**Stronger draft.** "The framework defines 159 sub-functions."

**Why it could not stand.** The capture has 159 `Sub-function N.N.N.N` *heading lines* but
only 158 distinct numbers: L1242 and L1244 are both numbered `5.3.1.1` ("Release Note
Disclosure" and "Release Note Review"), and L570/L572 carry a five-level numbering
(`1.5.1.1.2`, `1.5.1.1.3`) that the other sub-functions do not use. "159 sub-functions"
would assert a cardinality the document's own numbering does not support.

**Weakened to.** "159 sub-function headings", with the count presented as a re-derivation
from the capture's own headings rather than as a number the document states.

**Maps to** claim-table row C-12.

### W-3 — "the service areas are named Service Area 1 … Service Area 6"

**Stronger draft.** "The framework's six service areas are Stakeholder Ecosystem
Management, Vulnerability Discovery, Vulnerability Triage and Analysis, Remediation,
Vulnerability Disclosure and Training and Education."

**Why it could not stand.** The capture's heading lines for the first two service areas
carry **no title at all**: L402 is literally the string `Service Area 1` and L674 is
literally `Service Area 2`. Their names survive only in running prose — L331 ("Service Area
1 Stakeholder Ecosystem Management") and L1184 ("Service Area 2 Vulnerability Discovery") —
and in the PDF's table of contents, which is a different artifact with its own capture.

**Weakened to.** A table that gives each area's name with its anchor, and states in the
entry that SA1 and SA2 are "named only in prose" with the bare heading line noted. The
Limits section repeats that a quote asserting a service-area name must come from the prose,
not the heading line.

**Maps to** claim-table rows C-13, C-14, C-54.

### W-4 — "the framework defines what a PSIRT must do"

**Stronger draft.** "The framework specifies the obligations of a product incident response
team."

**Why it could not stand.** The page's own register is advisory. "shall" occurs 0 times in
the whole capture; "conform" occurs 0 times. The document describes itself as "high level
documents detailing possible services that computer incident response teams (CSIRTs) and
product incident response teams (PSIRTs) may provide" (L219) and says "In this way, teams
are free to implement their own model" (L221). A word like "obligations" attributes a
binding character the source disclaims.

**Weakened to.** "a catalogue of possible services, not a requirement set", with the two
supporting quotes inline and a rejected reading that rejects the mandate reading outright.

**Maps to** claim-table rows C-1, C-2, C-3, C-4, C-39, C-40.

### W-5 — "a maturity ladder of three levels (Strategic / Tactical / Operational)"

**Stronger draft.** "The framework organises PSIRT capability into three maturity levels:
Strategic, Tactical and Operational."

**Why it could not stand.** The Operational Foundations tiers (L315 `I. Strategic`, L356
`II. Tactical`, L385 `III. Operational`) are a *foundation* section, not a maturity
ladder, and the capture never puts them in a maturity ladder. Only two of the three tiers'
first sub-items are quotable at the entry's chosen anchors, so a claim covering all three
tiers' contents would have outrun the quotes.

**Weakened to.** "Before the services come 'Operational Foundations', tiered Strategic /
Tactical / Operational", with the first sub-item of the first tier (A. Executive
Sponsorship) and of the third tier (A. Policies and Procedures) quoted, plus an explicit
statement that "these three tiers are *foundation layers*, not maturity levels; the capture
does not equate them to maturity".

**Maps to** claim-table rows C-33, C-34, C-35, C-36.

### W-6 — "the framework sets disclosure deadlines"

**Stronger draft.** "The framework specifies disclosure timelines for PSIRTs."

**Why it could not stand.** The capture states no interval at all. It asks for timelines to
be *negotiated* — "The timeline for remediation and disclosure should be negotiated as soon
as possible" (L1160, and the same sentence at L1190 and L1212) — and no numeric interval
appears anywhere in the body.

**Weakened to.** "The framework asks for negotiated timelines … and states no interval of
its own", with a package rule forbidding reading a number into the page, and a Limits
bullet that names the measurement.

**Maps to** claim-table rows C-37, C-48.

### W-7 — "the framework is the multi-party coordination standard"

**Stronger draft.** "The PSIRT Services Framework defines how vendors, coordinators and
finders coordinate disclosure."

**Why it could not stand.** That is F06/S018's ground (FIRST's multiparty coordination
guidelines). This page's only FIRST cross-reference of that kind is a *footnote URL* to the
**v1.0** multiparty PDF (L1531) — a different document from the v1.1 guidelines the lane
already holds as S018 — and the page contains no party-relationship guidance of its own.

**Weakened to.** The service catalogue reading, with an explicit rejected reading for the
multi-party reading and a cross-reference row (R-2) naming the held row.

**Maps to** claim-table rows C-41, C-42, R-2, R-4.

### W-8 — "this is a phase-and-role model like CERT/CC's"

**Stronger draft.** "The framework maps disclosure phases to the responsible roles, in the
manner of the CERT Guide."

**Why it could not stand.** The capture has no phase model and no responsibility matrix.
"phase" occurs 3 times in the body, all in the SDL sense; the served HTML contains 0
`<table>` elements, so there is no matrix to read. The capture in fact says the opposite of
a fixed order: "While the order of operations is very similar among PSIRTs, there are
variations, such as the exact point when a 'case' is created" (L844).

**Weakened to.** A rejected reading that quotes the two L844 sentences instead, with the
absence measurements stated, and a cross-reference row (R-1) naming F43's held ground.

**Maps to** claim-table rows C-43, C-44, R-1.

---

## Part 2 — corrections: sentences written, then refuted by re-measurement

These were caught by this seat's own verification pass, not by a reviewer. Each is stated
here so a reviewer can see the failed measurement, not only the corrected text.

### X-1 — "the capture contains 0 occurrences of 'days', 'week' or 'deadline'"

**False as written.** Measured over L216-L1536, the body has **7** occurrences of
`day`/`days`/`week`/`deadline` on 6 lines: "day to day" (L284), "zero-day vulnerabilities"
(L504, L723, L1060), "every day" (L1283), "day of advisory publication" (L1287). The
original `grep -c -iE 'days|week|deadline'` returned 0 only because the source uses the
singular "day" and the compound "zero-day".

**Corrected to.** "No numeric interval appears anywhere in the body
(`\b\d+\s*(day|week|month|year|hour)\b` → 0 matches), and the words 'day', 'days', 'week'
and 'deadline' occur only as 'day to day' (L284), 'every day' (L1283), 'day of advisory
publication' (L1287) and 'zero-day' (L504, L723, L1060) — 'deadline' occurs 0 times."

The claim that survives is the stronger one that was actually wanted: no interval.

### X-2 — "the only date in the capture is the copyright range"

**False as written.** `grep -cE '20[0-9][0-9]'` over the body returns **12 lines** (13
occurrences), not 0: L1442-L1445 (Annex 1 supporting resources) and L1513-L1523 (Glossary
footnote URLs) carry ISO edition years — 2002, 2009, 2013, 2014, 2018.

**Corrected to.** "The page states none; the only date-bearing line in the capture is the
site's copyright footer … The body's own four-digit years are ISO edition years in the
Annex 1 and Glossary citation lists (L1442-L1445, L1513-L1523) — 2002, 2009, 2013, 2014,
2018 — not a date for this document."

The point the entry needed — the page publishes no date for *itself* — still holds, and
now for a stated reason instead of a false zero.

### X-3 — "no certification or compliance vocabulary"

**False as written.** "certification" occurs 3 times (L370 staff qualifications, L1319
"leading security certifications", L1343 "certified tracking tools") and "compliance"
6 times (L282, L303, L893, L1326, L1404, L1405).

**Corrected to.** "shall occurs 0 times in the capture; 'conform' occurs 0 times, and its
three uses of 'certification' are staff qualifications and a tracking tool (L370, L1319,
L1343), not a certification scheme for a reader." The absence claim is now about the two
words that are genuinely absent, and the two words that are present are named with their
meaning.

### X-4 — "'should' occurs 109 times in the body and 'must' 25 times"

**False as written.** Those are *line* counts. The occurrence counts are **138** ("should")
and **30** ("must").

**Corrected to.** "'should' occurs 138 times on 109 body lines and 'must' 30 times on 25
body lines" — both figures stated, each labelled.

### X-5 — "the capture has no role matrix … `grep -c 'Role'` → 2"

**Misleading as written.** `grep -c 'Role'` is case-sensitive and returns 2 (L1049, L1078).
The lowercase word "role" occurs on **14** body lines, all for staffing, training or
incident-role assignments.

**Corrected to.** "the word 'role' occurs 14 times and only for staffing and incident
assignments", with the 14 line numbers listed in the claim table. The claim is about the
absence of a *matrix*, not of the word, and the row now says so.

### X-6 — the body range, and the Downloads sidebar

**Imprecise as written.** The entry first gave the body as "L216-L1548" and treated the
Downloads block (L1550-L1573) as document content. The served raw HTML shows
`<div id="sidebar">` opens after the last document-content line, so L1537 onward is site
chrome: the navigation column (L1537-L1549) and the Downloads sidebar (L1550-L1573). The
committed round-65 manifest declares `body_lines: [216, 1450]`, which stops inside Annex 2
and so *excludes* the Glossary (L1498-L1512) where the maturity definition lives.

**Corrected to.** "document body L216-L1536 (site navigation column L1537-L1549 and the
Downloads sidebar L1550-L1573 are chrome)", and the E37 anchor is described as a chrome
anchor. See also the note in `gate.md` about the manifest's `body_lines`.

---

## Standing limits on this draft

- **Nothing here is admitted by itself.** This is a predata wave; the claims are not frozen.
  L1 (KasegiR65) is the sole production integrator.
- **The production entry for F44 already exists.** At the time this seat finished, L1 had
  committed `corpus/knowledge/first-psirt-services-framework.md` (commit `1c36d72`, along
  with the capture, the manifest and the F44 frontier row) and a later commit
  (`a333d8e`) followed. This seat read that landed entry and audited it — 18 quoted
  fragments, all verified verbatim at their declared anchors with matching word counts —
  but did **not** edit it, and does not claim it was produced from this draft. The draft
  here differs from the landed entry in two material ways, both recorded in
  `.ufo/waves/round-65/w1/EntryS098.md`: it treats the maturity *definition* (and the
  absence of maturity levels) as first-class ground, and it grades the landed entry's own
  sentences.
- **This seat produced documentation drafts only.** No frontier counter, census, gate,
  freeze check or score movement was run or claimed. No production corpus file was edited.
- **One capture, three identical copies.** This seat's independent capture, ScoutS098's
  candidate and L1's committed capture share sha256
  `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`. That is
  reproducibility of the *bytes*, not independent confirmation of the document's meaning.
