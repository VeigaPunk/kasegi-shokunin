# ExecC2Capture — round 36 capture: F19 FIRST EPSS page (S053)

Seat: ExecC2Capture (leaf, executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).
Axis owned by this seat: coverage (C2's F19 source capture). Date of all measurements: 2026-10-26.
Report path: `.ufo/waves/round-36/wave1/ExecC2Capture.md`.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/ExecC2Capture/`.
No lane file, registry row, manifest, capture, entry or instrument was edited, and no git/jj mutation was run.
The scratch directory was removed after this receipt was written; every byte below is reproducible from the
embedded blocks and the pinned sha256 values.

---

## 1. Fetch (measured, not inferred)

| item | value |
|---|---|
| requested URL | `https://www.first.org/epss/` |
| method / UA | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` |
| followed redirects | yes (`-L`); **0 redirected**, requested URL == effective URL |
| effective (final) URL | `https://www.first.org/epss/` |
| HTTP status | `200` |
| content-type | `text/html; charset=UTF-8` |
| served bytes | `26804` (curl `size_download`); response `content-length: 26804` |
| response Date header | `Mon, 26 Oct 2026 15:35:06 GMT` |
| Last-Modified header | `Thu, 30 Jul 2026 13:48:13 GMT` |
| `fetched_utc` recorded | `2026-10-26T15:35:10Z` (local UTC clock read immediately after the transfer completed) |
| served-body sha256 | `66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868` (scratch `raw.html`, 26804 bytes; not committed) |

HTTP/2 response headers observed (scratch `headers.txt`): `HTTP/2 200`, `content-type: text/html; charset=UTF-8`,
`content-length: 26804`, `last-modified: Thu, 30 Jul 2026 13:48:13 GMT`, `date: Mon, 26 Oct 2026 15:35:06 GMT`,
`server: nginx`, `vary: Accept-Encoding`, `strict-transport-security: max-age=31557600`, plus
`cache-control: public, max-age=3600, s-maxage=3600` and `x-cache: MISS, HIT`. No `location:` header exists,
which is what "no redirect" means here beyond curl's `redirects=0`.

---

## 2. Normalization

The lane's own `corpus/instruments/capture-source.py` was imported read-only and its `html_to_text()` used
unchanged, so the capture semantics match every prior round: `<script>`/`<style>` blocks removed; block tags
(`p div li tr h1-h6 section article br`) converted to newlines; remaining tags stripped (this is the
"strip markup" step — the served page uses `<u>` accent markup in its navigation, and no tag or attribute
text survives); `html.unescape()` applied; runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8
kept byte-for-byte, including the page's en dash in `0–1`. The result is `S053.txt` (244 lines, 8448 bytes,
final newline) with sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`.

| artifact (scratch) | bytes | lines | sha256 |
|---|---|---|---|
| `S053.txt` (normalized capture) | 8448 | 244 | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` |
| `manifest.json` (below) | 3566 | — | `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` |

The two artifacts the L1 must land, byte-identically, are `corpus/source-snapshots/round-36/S053.txt` and
`corpus/source-snapshots/round-36/manifest.json`.

---

## 3. Manifest (full JSON)

Field note: the record array is the schema-mandated `sources[]` key — the key `corpus/instruments/source-recheck.py`
and `corpus/instruments/capture-binding-check.py` read — and its one record carries every field the item lists
(`url`, `fetched_utc`, `fetched_bytes`, `sha256`, `lines`, `normalized`) plus the four pinned quotes. No
`records[]` alias is emitted: a second copy of the same record would be unreferenced by both instruments and
would misstate the manifest as two records.

```json
{
  "schema_version": 1,
  "purpose": "Round-36 F19 captured-source assertions for S053 (FIRST Exploit Prediction Scoring System (EPSS) documentation page), fetched 2026-10-26T15:35:10Z with curl -L under the instrument UA kasegi-shokunin/1.0: HTTP status=200, content-type=text/html; charset=UTF-8, no redirect (requested URL == final URL), fetched_bytes=26804, snapshot_bytes=8448, 244 lines, sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9. Normalized with the lane's capture-source.py html_to_text() (markup stripped, entities unescaped, whitespace collapsed, UTF-8). The record array is the schema-mandated sources[] list read by source-recheck.py and capture-binding-check.py; it carries the requested url/fetched_utc/fetched_bytes/sha256/lines/normalized fields plus quotes Q1-Q4, each verified against the normalized capture with grep -cF (count 1 each).",
  "sources": [
    {
      "id": "S053",
      "path": "S053.txt",
      "url": "https://www.first.org/epss/",
      "fetched_utc": "2026-10-26T15:35:10Z",
      "fetched_bytes": 26804,
      "snapshot_bytes": 8448,
      "lines": 244,
      "sha256": "4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9",
      "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
      "http": {
        "status": 200,
        "content_type": "text/html; charset=UTF-8",
        "final_url": "https://www.first.org/epss/",
        "redirects": 0,
        "user_agent": "kasegi-shokunin/1.0",
        "fetched_utc": "2026-10-26T15:35:10Z"
      },
      "quotes": [
        {
          "id": "Q1",
          "quote": "(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.",
          "anchor": 216,
          "location": "L216; the page's definitional sentence is 'The Exploit Prediction Scoring System (EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.' The pinned span starts at the '(EPSS)' parenthetical and is exactly 25 words, because the full sentence is 30 words and the pin budget here is 25."
        },
        {
          "id": "Q2",
          "quote": "EPSS publishes a 0–1 probability (with ranking percentiles)",
          "anchor": 217,
          "location": "L217; the first clause of the publication sentence: the score is a 0-1 probability and the feed carries ranking percentiles alongside it."
        },
        {
          "id": "Q3",
          "quote": "every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo",
          "anchor": 217,
          "location": "L217; the daily-for-every-CVE cadence and the free/open distribution channels (CSV, API, github repo) in one 23-word clause of the same sentence."
        },
        {
          "id": "Q4",
          "quote": "EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.",
          "anchor": 235,
          "location": "L235; the maintenance/ownership sentence plus the score-generation sentence: the SIG at FIRST maintains EPSS and Empirical Security generates the scores published freely to the community."
        }
      ]
    }
  ]
}
```

---

## 4. Quote pinning (all four occur exactly once)

Quotes were derived from the normalized bytes and checked with the item's exact discriminator, `grep -cF`
(the loop read one quote per line from `quotes.txt` and printed the count; `-c` counts matching lines and every
quote lies inside one capture line). Independent assertions (`str.count == 1`, word count `<=25`, quote is on
its declared anchor line) passed for all four; `corpus/instruments/source-recheck.py` then re-verified the
manifest and exited 0.

| id | anchor | words | grep -cF count | pinned quote |
|---|---|---|---|---|
| Q1 | L216 | 25 | 1 | `(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.` |
| Q2 | L217 | 8 | 1 | `EPSS publishes a 0–1 probability (with ranking percentiles)` |
| Q3 | L217 | 23 | 1 | `every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo` |
| Q4 | L235 | 23 | 1 | `EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.` |

Why Q1 starts at `(EPSS)`: the page's definitional L216 sentence is
`The Exploit Prediction Scoring System (EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.`
— 30 words, over the item's 25-word pin budget. The pinned span keeps the model name (`EPSS`), the
`data-driven machine-learning model` definition and the full 30-day horizon in exactly 25 words; the
`sentence` prefix is recorded in the quote's `location` field so the reader sees the full sentence, not a
silently truncated claim. Q2 and Q3 are contiguous, non-overlapping clauses of the same L217 sentence: Q2
pins the 0–1 probability plus ranking percentiles, Q3 the daily-for-every-CVE cadence plus the free/open
CSV, API and github distribution. En dash `–` (U+2013) in Q2 is the page's own character, not a hyphen.

Evidence lines (scratch, verbatim):

```text
$ grep -cF -- '(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.' S053.txt
1
$ grep -cF -- 'EPSS publishes a 0–1 probability (with ranking percentiles)' S053.txt
1
$ grep -cF -- 'every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo' S053.txt
1
$ grep -cF -- 'EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.' S053.txt
1

$ python3 corpus/instruments/source-recheck.py --manifest manifest.json --source S053
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
rc=0
```

(The `source-recheck.py` run was read-only against the scratch manifest and confirms the manifest is valid for
the lane's schema: sha256 bound, path stem `S053` == id, anchors verify on the normalized capture. It is the
instrument's own reading, not a re-fetch.)

---

## 5. Primary-page text the pins rest on (L216, L217, L235)

```text
L216: The Exploit Prediction Scoring System (EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.
L217: It offsets subjective judgments with empirical signals from observed exploitation and ongoing activity, helping you focus limited remediation effort where attacks are most likely. EPSS publishes a 0–1 probability (with ranking percentiles) every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo, so it slots easily into workflows and dashboards.
L235: EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.
```

---

## 6. Normalized capture `S053.txt` (verbatim, 244 lines, sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`)

```text
Exploit Prediction Scoring System (EPSS)
Member Portal
About FIRSTMission Statement
Strategy Framework
History
Sustainable Development Goals
OrganizationBoard of Directors
Operations TeamCommunity & Capacity Building
Event Office
Executive Director
Infrastructure
Secretariat
CommitteesCompensation Committee
Conference Program Committee
Finance Committee
Membership Committee
Rules Committee
Standards Committee
Annual General Meeting
Annual Reports and Tax Filings
FIRST PoliciesAnti-Corruption Policy
Antitrust Policy
Bylaws
Board duties
Bug Bounty Program
Code of Conduct
Conflict of Interest Policy
Document Record Retention and Destruction Policy
FIRST Press Policy
Guidelines for Site Selection for all FIRST events
Identity & Logo Usage
Mailing List Policy
Media Policy
Privacy Policy
Registration Terms & Conditions
Services Terms of Use
Standards Policy
Statement on Diversity & Inclusion
Translation Policy
Travel Policy
Uniform IPR Policy
Whistleblower Protection Policy
PartnershipsPartners
Friends of FIRST
FIRST Supporters
FIRST Sponsors
NewsroomWhat's New
Press Releases
In the News
PodcastsFIRST Impressions Podcast
FIRSTCON Podcast
Newsletters
FIRST Press Policy
Procurement
Jobs
Contact
MembershipBecoming a MemberMembership Process for Teams
Membership Process for Associates
Membership Process for Individual Members
Membership Fees
FIRST Teams
FIRST Associates
FIRST Individual Members
Members around the world
InitiativesSpecial Interest Groups (SIGs)SIGs Framework
Academic Security SIG
AI Security SIG
Automation SIG
Cybersecurity Communications SIG
Common Vulnerability Scoring System (CVSS-SIG)Calculator
Specification Document
User Guide
Implementation Guide
Governance Guidelines
Examples
Frequently Asked Questions
CVSS v4.0 Documentation & ResourcesCVSS v4.0 Calculator
CVSS v4.0 Specification Document
CVSS v4.0 User Guide
CVSS v4.0 Implementation Guide
CVSS v4.0 Examples
CVSS v4.0 FAQ
CVSS v3.1 ArchiveCVSS v3.1 Calculator
CVSS v3.1 Specification Document
CVSS v3.1 User Guide
CVSS v3.1 Examples
CVSS v3.1 Calculator Use & Design
CVSS v3.0 ArchiveCVSS v3.0 Calculator
CVSS v3.0 Specification Document
CVSS v3.0 User Guide
CVSS v3.0 Examples
CVSS v3.0 Calculator Use & Design
CVSS v2 ArchiveCVSS v2 Complete Documentation
CVSS v2 History
CVSS-SIG team
SIG Meetings
Frequently Asked Questions
CVSS Adopters
CVSS Links
CVSS v1 ArchiveIntroduction to CVSS
Frequently Asked Questions
Complete CVSS v1 Guide
JSON & XML Data Representations
CVSS On-Line Training Course
Identity & logo usage
CSIRT Framework Development SIG
Cyber Insurance SIGCyber Insurance SIG Webinars
Cyber Threat Intelligence SIGCurriculumIntroduction
Introduction to CTI as a General topic
Methods and Methodology
Priority Intelligence Requirement (PIR)
Source Evaluation and Information Reliability
Machine and Human Analysis Techniques (and Intelligence Cycle)
Threat Modelling
Training
Standards
Glossary
Communicating Uncertainties in CTI Reporting
Webinars and Online Training
CTI SIG Blog
Contributors
Building a CTI program and teamProgram maturity stagesCTI Maturity model - Stage 1
CTI Maturity model - Stage 2
CTI Maturity model - Stage 3
Program Starter Kit
Resources and supporting materials
Detection Engineering & Threat Hunting SIG
Digital Safety SIG
DNS Abuse SIGDNS Abuse Techniques Matrix
Stakeholder AdviceCreation of Malicious Subdomains Under Dynamic DNS Providers
DNS Cache Poisoning
DGA Domains
DNS as a Vector for DoS
DNS Beacons - C2 Communication
DNS Rebinding
DNS Server Compromise
DNS Tunneling
DoS Against the DNS
Domain Name Compromise
Fast Flux
Infiltration and exfiltration via the DNS
Lame Delegations
Local Recursive Resolver Hijacking
Malicious registration of (effective) second level domains
Obfuscation via Dynamic DNS
On-path DNS Attack
Stub Resolver Hijacking
Spoofing of a Registered Domain
Use of an Unregistered Domain
Code of Conduct & Other Policies
Examples of DNS Abuse
Ethics SIGEthics for Incident Response Teams
Exploit Prediction Scoring System (EPSS)Why EPSS?
Get the Data
Using EPSS
How EPSS Works
Frequently Asked Questions
Research
Who is using EPSS?
Log4Shell Use Case
FIRST Multi-Stakeholder Ransomware SIG
Human Factors in Security SIG
Industrial Control Systems SIG (ICS-SIG)
Information Exchange Policy SIG (IEP-SIG)
Information Sharing SIGMalware Information Sharing Platform
Insider Threat SIG
Law Enforcement SIG
Malware Analysis SIGMalware Analysis Framework
Malware Analysis Tools
Metrics SIGMetrics SIG Webinars
NETSEC SIG
Public Policy SIG
PSIRT SIG
Red Team SIG
Security Lounge SIGSecurity Lounge SIG Framework
Security Operations Center SIG
Standards SIG
Strategic Thinking and Planning SIG
Threat Intel Coalition SIGMembership Requirements and Veto Rules
Time SIG
Traffic Light Protocol (TLP-SIG)
Transportation and Mobility SIG
Vulnerability CoordinationMulti-Party Vulnerability Coordination and Disclosure
Guidelines and Practices for Multi-Party Vulnerability Coordination and Disclosure
Vulnerability Reporting and Data eXchange SIG (VRDX-SIG)Vulnerability Database Catalog
Women of FIRST
CCB Initiatives
FIRST CORESponsorship Opportunities
Internet Governance
IR Database
Fellowship ProgramApplication Form
Mentorship Program
IR Hall of FameHall of Fame Inductees
Victim Notification
Volunteers at FIRSTFIRST Volunteers
Member Spotlight
Previous ActivitiesBest Practices Contest
Standards & PublicationsStandardsCommon Vulnerability Scoring System (CVSS-SIG)
Traffic Light Protocol (TLP)TLP Use Cases
Service FrameworksCSIRT Services Framework
PSIRT Services Framework
Information Exchange Policy (IEP)IEP 2.0 Framework
IEP 2.0 JSON Specification
Standard IEP PoliciesIEP TLP Policy File
IEP Unknown Policy File
IEP 1.0 Archive
Passive DNS Exchange
Exploit Prediction Scoring System (EPSS)
Publications
Community Resources
Events
EducationFIRST TrainingTraining Courses
FIRST Trainers
Blog
JoinDetails about FIRST membership and joining as a full member or liaison.LearnTraining and workshop opportunities, and details about the FIRST learning platform.ParticipateRead about upcoming events, SIGs, and know what is going on.CommunityCommunity and Capacity Building.
The Exploit Prediction Scoring System (EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.
It offsets subjective judgments with empirical signals from observed exploitation and ongoing activity, helping you focus limited remediation effort where attacks are most likely. EPSS publishes a 0–1 probability (with ranking percentiles) every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo, so it slots easily into workflows and dashboards.
Where to go from here
How It Works
Model methodology, feature overview, calibration, and known limitations.
Why EPSS?
The empirical case for exploitation likelihood as a prioritization signal. Performance data, CVSS comparison, and what the research shows.
Using EPSS
How to set thresholds, combine EPSS with CVSS and KEV, interpret score changes, and avoid common misuses.
Frequently Asked Questions
Answers to the questions practitioners ask most often about the score, the percentile, and how EPSS compares to other tools.
Research
Peer-reviewed papers, presentations, and the version changelog.
Get the Data
API reference, daily CSV downloads, historical scores, and integration examples.
Get involved
The EPSS Special Interest Group (SIG) is a practitioner community focused on putting EPSS to work. Members meet every other Friday, share implementations, and contribute case studies and talks. If you use EPSS or want to, the SIG is where the conversation happens.
Special Thanks
Special thank you to all of our data partners who make EPSS possible. Exploitation activity data used in EPSS is provided in part by a number of industry and government partners, which includes but is not limited to: VulnCheck KEV (VulnCheck Known Exploited Vulnerabilities), Shadow Server Foundation and LevelBlue.
EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.
Exploit Prediction Scoring System (EPSS)Why EPSS?
Get the Data
Using EPSS
How EPSS Works
Frequently Asked Questions
Research
Who is using EPSS?
Log4Shell Use Case
Copyright © 2015—2026 by Forum of Incident Response and Security Teams, Inc. All Rights Reserved.
```

---

## 7. Coordination

- `ExecC2QuoteOnce` asked for the manifest and capture bytes; answered with the normative path and the
  sha256, warned that the wave rule removes this seat's scratch at yield, and confirmed the receipt embeds
  `S053.txt` verbatim so the bytes are recoverable from it after that removal.
- `ScribeRowS053` asked whether the committed capture will be byte-identical and whether Q1 is the L216
  sentence at anchor 216; answered yes (sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`) and gave the 25-word span plus its 30-word
  source sentence so the row's anchor cell cites L216 correctly.
- No `agent://all` message was sent and no swarm/subagent was run.

---

## 8. Risks, limits and handoff

- The URL is a live page (`Last-Modified: Thu, 30 Jul 2026 13:48:13 GMT`); the pin is the 2026-10-26 fetch
  bytes, so a later re-fetch may change bytes and quote counts. The manifest is a capture assertion, not a
  currency claim; S053's recheck cadence belongs to its registry row, not to this receipt.
- `fetched_utc` is this host's UTC clock read at transfer completion (`2026-10-26T15:35:10Z`); the server
  `Date` header of the same response reads `15:35:06 GMT`. The four-second difference is transfer
  completion order, not a clock disagreement; both are UTC and same-day.
- Landing is the L1's write: copy the two embedded payloads byte-for-byte and re-check `sha256sum` against
  `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` (`S053.txt`) and `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` (`manifest.json`). The record `url` is exactly the registry URL
  `https://www.first.org/epss/`, trailing slash included, because `capture-binding-check.py` rule B5 compares
  it byte-for-byte with the S053 row's `https://` token.
- This seat did not run the lane's suite, census, harness or any build/lint/formatter; those gates belong to
  the parent after integration. Scratch `/fast/scratch/hyaku/kasegi-r36/ExecC2Capture/` was removed after
  this receipt was written.
