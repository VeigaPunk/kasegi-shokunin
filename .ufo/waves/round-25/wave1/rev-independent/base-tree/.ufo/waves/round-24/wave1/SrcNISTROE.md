# SrcNISTROE — package entry `authorised-testing-rules-of-engagement.md` re-grounded against NIST SP 800-115

Seat: scout (read-only). Item: re-ground the C2 candidate `knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md`
against its primary source. Lane base d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a. Date: 2026-10-25.
Bodies in /tmp/nistroespdf only. No production file, lane tree, git/jj state or shokuknow byte was written.

## Findings first

1. **The primary resolves and is byte-stable on re-fetch.** GET 200, 544047 bytes,
   sha256 `58e5ed41e5c8ca34ce14fd80b70f118f2c6d613d1647bc307edca30bcc45f063`. The document is
   80 pages; Appendix B occupies PDF sheets 67–69 (printed folia B-1..B-3); the ROE glossary entry
   is on sheet 77 (printed F-2).
2. **All four fragments the package entry cites in its `Evidence` block are exactly-once and each lies
   inside a single physical line of the `pdftotext -layout` rendering** — `grep -cF` returns 1 for each,
   in both the `-layout` and the default rendering. The entry's quotations are faithful; the entry's
   *locator* is also correct but easy to misread: the definition is in **Appendix F (Glossary, F-2)**,
   not in Appendix B.
3. **Appendix B is a 7-section template whose labels are: Introduction (Purpose, Scope, Assumptions and
   Limitations, Risks, Document Structure), Logistics (Personnel, Test Schedule, Test Site, Test
   Equipment), Communication Strategy (General Communication, Incident Handling and Response), Target
   System/Network, Testing Execution (Nontechnical Test Components, Technical Test Components, Data
   Handling), Reporting, Signature Page.** Full list in §(b).
4. **Three of the four concepts the lane wants to hang on Appendix B are NOT literally there.**
   `letter` = 0 occurrences, `permission` = 0, `evidence` = 0, `escalat*` = 0 across PDF sheets 67–69.
   Only **scope** is an actual Appendix B heading with substantive text. Escalation exists only as
   *Incident Handling and Response* (halt criteria / call tree / resumption); evidence handling exists
   only as *Data Handling* (gather/store/transmit/destroy **test data**, "should be considered
   sensitive"); "authorization letter" has no counterpart at all — the template's instrument is a
   *Signature Page* plus a signed assessment plan (§6.5, 6-11) and written permission to deviate
   (§7.2, 7-2). Detail and verdicts in §(e).
5. **Two recheck traps for the C1 verifiability instrument, both observed:**
   (i) `HEAD` on the nvlpubs URL returns **HTTP/2 404** while `GET` returns **200** with the correct
   PDF — a rechecker that probes with HEAD will false-fail this source;
   (ii) `pdftotext` 26.08.0 writes `Syntax Error: Expected the default config, but wasn't able to find
   it, or it isn't a Dictionary` to **stderr** yet exits **0** and extracts deterministically (byte-identical
   on re-run) — a rechecker that treats non-empty stderr as failure will false-fail it too.
6. The entry's `recheck:` line is prose (`90d — re-fetch the PDF and grep -F the four lines (ran
   2026-10-24)`), not an executable command, so as written it cannot itself exit 0/2. It can be made
   executable without changing any claim — see §(f).

## (a) Primary artifact record

| item | value |
|---|---|
| URL | `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` |
| GET status | `200` (`curl -sS -L -w '%{http_code}'`) |
| HEAD status | `404` (Cloudflare/CDN rejects HEAD; **GET is the only probe that answers**) |
| Content-Type | `application/pdf` |
| Bytes | `544047` (`ls -l`, cross-confirmed by `pdfinfo` "File size: 544047 bytes") |
| sha256 | `58e5ed41e5c8ca34ce14fd80b70f118f2c6d613d1647bc307edca30bcc45f063` |
| Pages | 80 (`pdfinfo`) — my `\f` split yields 81 segments, the last empty |
| CreationDate | `Mon Sep 29 14:09:24 2008` → matches "September 2008" printed on sheet 2 |
| ModDate | `Fri Nov 21 17:31:06 2025` — NIST re-saved the served bytes in Nov 2025; the hash above is the current body, not a 2008 byte-identity |
| Producer | `Acrobat Distiller 7.0.5 (Windows)` |
| Extraction | `pdftotext -layout sp800-115.pdf out.txt` → 3066 non-empty lines, exit 0, byte-identical on second run |

Evidence: `/tmp/nistroespdf/sp800-115.pdf`, `/tmp/nistroespdf/sp800-115-layout.txt`,
`/tmp/nistroespdf/sp800-115-raw.txt`, `pdfinfo sp800-115.pdf`.

Note the ModDate/2008-CreationDate split: the entry's Limit ("the guide is dated September 2008 and is
the version NIST still serves") is true of the *edition*; the *served bytes* are a 2025 re-save. Any
recheck must therefore pin either the PDF sha256 or the extracted-text hash, not "the 2008 file".

## (b) Appendix B — exact line labels as they render (PDF sheets 67–69, folia B-1..B-3)

Sheet 67 (B-1):
```
Appendix B—Rules of Engagement Template
1.  Introduction
1.1.  Purpose
1.2.  Scope
1.3.  Assumptions and Limitations
1.4.  Risks
1.5.  Document Structure
2.  Logistics
2.1.  Personnel
2.2.  Test Schedule
```
Sheet 68 (B-2):
```
2.3.  Test Site
2.4.  Test Equipment
3.  Communication Strategy
3.1.  General Communication
3.2.  Incident Handling and Response
4.  Target System/Network
5.  Testing Execution
```
Sheet 69 (B-3):
```
5.1.  Nontechnical Test Components
5.2.  Technical Test Components
5.3.  Data Handling
6.  Reporting
7.  Signature Page
```
Seven top-level sections, eleven numbered subsections, thirteen labels plus the appendix title. There is
no `Authorization`, `Escalation`, `Evidence`, `Evidence Handling`, `Legal`, or `Deliverables` heading.
Section 5 has a two-line intro and no numbered subsections of its own beyond 5.1–5.3; §4 is a flat
single-paragraph section. Footnote 42 on B-1 reads: "The structure of this template is intended to be
illustrative. Organizations should organize their ROEs in whatever manner they choose." — that
qualifier is what makes claiming any *absent* component against Appendix B a category error rather
than a defect.

## (c) Glossary entry, verbatim

PDF sheet 77, printed folio **F-2** (page marker: the folio line at the bottom of the extracted page;
sheet index from the `\f` split of `pdftotext -layout`). Three physical lines in the rendering:

```
Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information
security testing. The ROE is established before the start of a security test, and gives the test team
authority to conduct defined activities without the need for additional permissions.
```
Whitespace-collapsed verbatim: **"Rules of Engagement (ROE): Detailed guidelines and constraints
regarding the execution of information security testing. The ROE is established before the start of a
security test, and gives the test team authority to conduct defined activities without the need for
additional permissions."**

No trailing sentence; the entry for `Ruleset:` follows immediately. The package entry quotes this in
three correct fragments and attributes it to the glossary — verified.

## (d) Three exactly-once quote candidates (manifest assertions)

Method: split `pdftotext -layout` output on `\f`; page number = 1-based segment index; page marker =
the printed folio at the bottom of that segment; uniqueness = `grep -cF` over the whole 3066-line
extraction, confirmed 1 in **both** `-layout` and default rendering, and confirmed to sit inside a
single physical line (so a line-oriented `grep -F` rechecker works without joining lines).

| # | quote | words | PDF sheet | printed marker | `grep -cF` |
|---|---|---|---|---|---|
| 1 | `Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information` | 13 | 77 | `F-2` | 1 |
| 2 | `Appendix B provides a template for creating Rules of Engagement (ROE).` | 11 | 11 | `1-2` | 1 |
| 3 | `Identifies test boundaries in terms of actions and expected outcomes` | 10 | 67 | `B-1` | 1 |

Why these three: #1 is the glossary head (the definition the entry is built on); #2 is the only
sentence in the document that states Appendix B *is* the template, quoted by the entry verbatim;
#3 is Appendix B §1.2 Scope's whole body, so it is simultaneously the template's scope claim and an
in-template anchor. #1 and #3 are each inside one physical line even though they truncate at a line
break — #1's cut point (`...information` / `security testing.`) is stable across both renderings.

Verified alternates, same method, if a longer or resume-safer triple is wanted:

| quote | words | sheet | marker | `grep -cF` |
|---|---|---|---|---|
| `The ROE is established before the start of a security test, and gives the test team` | 16 | 77 | `F-2` | 1 |
| `Criteria for halting the information security testing should be provided` | 10 | 68 | `B-2` | 1 |
| `Identifies guidelines for gathering, storing, transmitting, and destroying test data` | 11 | 69 | `B-3` | 1 |

Do **not** assert on `Appendix B— Rules of Engagement Template` (table of contents) vs
`Appendix B—Rules of Engagement Template` (body heading): the em dash spacing differs between sheet 6
and sheet 67, so an em-dash assertion is a two-variant string. Same for anything spanning a line break
(`...execution of information security testing.` as one line does not exist; `...gives the test team
authority to conduct...` as one line does not exist).

## (e) Are the entry's four claims actually in Appendix B?

Entry text as filed names only two things: the glossary definition and "Appendix B provides a template
for creating Rules of Engagement (ROE)." The other three components are the lane's standard ROE
inventory. Checked each one against PDF sheets 67–69 only.

**Scope — PRESENT, and the strongest of the four.** Four distinct loci:
- §1.2 Scope (B-1): "Identifies test boundaries in terms of actions and expected outcomes."
- §2.3 Test Site (B-2): "Identifies the location or locations from which testing is authorized." plus
  "Areas to which the test team will not be given access should be identified here as well."
- §4 Target System/Network (B-2): "Information should include authorized and unauthorized IP addresses
  or other distinguishing identifiers" and "It is also crucial to identify any system not authorized for
  testing—this is referred to as the 'exclude list.'"
- §5 (B-2): "should detail allowable and unallowable activities"; §7 (B-3): signatories state "they
  understand the test's scope and boundaries."
The entry's core sentence — an authorisation is "a **defined scope**, written down in advance" — is
supported by Appendix B directly, and by the glossary's "defined activities". **Claimed/verified.**

**Authorization letter — ABSENT as such.** `letter` = 0 occurrences in Appendix B. `authoriz*` appears
7×, and every use is scope-membership, never conferral: "the location or locations from which testing is
authorized" (2.3); "tools authorized for use on the network" (2.4); "authorized and unauthorized IP
addresses", "any system not authorized for testing" (4); "whether files are authorized to be installed,
created, modified, and/or executed" (5.2); "what is authorized and to be expected" (5.2). `permission`
= 0 occurrences — the word that carries the conferral in the glossary ("without the need for additional
permissions") never appears in the template. The nearest instruments are:
- §7 Signature Page (B-3): "At a minimum, the test team leader and the organization's senior management
  (CSO, CISO, CIO, etc.) should sign the ROE stating that they understand the test's scope and
  boundaries." — an acknowledgement of scope, not a letter of authority.
- §5.1 (B-3): "a form—with appropriate signatures and contact information—generated for the test team to
  show to law enforcement or onsite security personnel in the event that they are questioned." — a
  get-past-security artefact, not an authorisation.
Conferral lives **outside** Appendix B: glossary F-2 ("gives the test team authority … without the need
for additional permissions"), §6.5 at 6-11 ("By signing the assessment plan, all parties acknowledge and
approve of the assessment"), and §7.2 at 7-2 ("The plan or ROE should be followed unless specific
permission to deviate has been obtained, normally in writing, from the original signatory or individual
in command").
Verdict: if an F09 entry is written as "the ROE is an authorization letter", that is **INFERENCE** and
over-reads the template. Defensible form: "the ROE is signed by both parties, and the signature records
acknowledgement of a defined scope; authority to act is stated in the glossary and in the signed
assessment plan, not in Appendix B."

**Escalation — ABSENT as a label; functionally present as incident handling.** `escalat*` = 0 in
Appendix B. The word appears 5× in the document, all outside it: privilege escalation in §2.4.1 discussion continued on 2-5 (sheet 16, which also opens §2.4.2) and
§5.2 penetration-testing prose (5-4 sheet 38, 5-6 sheet 40), §6.5 covert-testing reporting (6-11, sheet 52), and §7.2 "the
organization's normal escalation procedures" (7-2, sheet 56). Appendix B's carrier is §3.2 Incident Handling and Response (B-2):
"This section is critical in the event that an incident occurs on the network while testing is in
progress. Criteria for halting the information security testing should be provided, as should details on
the test team's course of action in the event that a test procedure negatively impacts the network or an
adversary attacks the organization while testing is underway. The organization's incident response call
tree/chain of command should be provided in a quick-reference format. A process for reinstating the test
team and resuming testing should also be provided."
That is a halt/notify/resume protocol. It is **not** an escalation ladder for scope disputes — Appendix B
has no equivalent of §6.5's "If questions regarding scope and level of authorization arise during the
course of an assessment, the assessors and the organization's identified point of contact should meet to
discuss them" (6-11).
Verdict: claim must be worded as "incident handling and halt criteria", not "escalation".

**Evidence handling — ABSENT as such; present as test-data handling.** `evidence` = 0 in Appendix B.
The document's only uses of `evidence` are assessment-methodology prose on sheets 8 and 12 ("obtain
evidence", "the location of evidence"), not forensic handling. Appendix B §5.3 Data Handling (B-3):
"Identifies guidelines for gathering, storing, transmitting, and destroying test data, and establishes
detailed, unambiguous requirements for data handling. Keep in mind that data results from any type of
information security test will identify vulnerabilities that an adversary can exploit, and should be
considered sensitive."
The frame is **sensitive data hygiene**, explicitly *not* evidentiary: no chain of custody, no
admissibility, no retention-for-proceedings. Outside Appendix B the same frame recurs at §6.5 (6-11,
four bullets: storage on assessor systems, long-term storage, transmission, removal) and §7.4 (7-4..7-7,
Data Collection/Storage/Transmission/Destruction).
Verdict: claim must be worded as "data handling", not "evidence handling". If the entry's purpose is to
support a court-facing argument, Appendix B does not carry it; §6.6 Legal Considerations (6-12) covers
indemnity, NDAs, privacy banners and legal-department review of data handling, and still says nothing
about evidence.

## (f) What this changes for the lane's instrument (C1 counter A, C2 gate Q1–Q6)

An executable `recheck:` for this entry, runnable from a committed capture and exiting 0 only on match
(one assertion per quote, `-c` == 1 catches both absence and duplication):

```sh
cap=<committed>/captures/sp800-115-layout.txt   # pdftotext -layout of the pinned PDF
test "$(grep -cF 'Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information' "$cap")" = 1
test "$(grep -cF 'Appendix B provides a template for creating Rules of Engagement (ROE).' "$cap")" = 1
test "$(grep -cF 'Identifies test boundaries in terms of actions and expected outcomes' "$cap")" = 1
```

If the capture is the PDF instead of text, pin the sha256 above and pipe through `pdftotext -layout -`
— but then the recheck must ignore the stderr `Syntax Error` line and the exit status of `pdftotext`
must be 0 (observed 0). Do not use `curl -I`; use `curl -sfL -o`.

## Confidence

- (a) artifact identity/hash/pages/date — **high** (two independent tools agree on size; hash single-run).
- (b) label list — **high** (verbatim extraction, contiguous B-1..B-3, checked no fourth sheet).
- (c) glossary verbatim — **high** (exactly-once, both renderings).
- (d) uniqueness/page markers — **high** for the six quoted candidates (counted, both renderings,
  physical-line containment checked).
- (e) presence/absence verdicts — **high** for presence; for absence, high within Appendix B, with the
  caveat that absence under footnote 42 is not a defect of NIST and must not be scored as one.

## Remaining unknowns

1. **UNVERIFIED:** byte-identity of the served PDF to the 2008 original. The served file carries
   `ModDate Fri Nov 21 17:31:06 2025`; only the edition/print date (September 2008) is verified. Whether
   the 2025 re-save changed any glyph is not established (would need an archived 2008 copy, not fetched).
2. **UNVERIFIED:** the lane's renumber map does not exist yet at
   `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/assimilation/renumber-map.tsv`
   (named by claims.json); `assimilation/` holds `census-before.txt`, `collisions/`, `reg-ids/`,
   `staged-ids/`. So whether the entry's `source: S123` is the id the round actually assigns is
   **not checkable** from round-24 bytes at the time of writing. Observation only, not my item:
   `S123` already matches the `^source: S1[0-9][0-9] ` shape that C2 counter B greps, and
   `census-before.txt` (3 lines) contains no `S1xx` id, so nothing in round-24 evidence contradicts it.
3. **UNVERIFIED:** whether any sibling seat is simultaneously re-grounding the second C2 candidate
   (`statutory-authorization-in-three-traditions.md`); out of scope for this item and not inspected.
