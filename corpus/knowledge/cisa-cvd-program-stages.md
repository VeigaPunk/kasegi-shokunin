# CISA's Coordinated Vulnerability Disclosure (CVD) Program page — the seven-stage coordinator pipeline, the CNA-of-Last-Resort role, the 45-day earliest-disclosure floor, the VEP exclusion, and the CVD-versus-VDP separation

source: S023 — https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program — capture corpus/source-snapshots/round-40/S023.txt (213 lines, 14,357 bytes; sha256 52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087): intake channel L88-L89, technology breadth L104-L110, simultaneous dissemination L111, Top Level Root and CNA of Last Resort L112, statutory authorities L114, the seven-stage process L115-L146, triage criteria L117-L123, in/out-of-scope outcomes L124-L127, coordination actions L128-L133, CVE record determination L134-L135, advisory preparation L136-L145, KEV evaluation L146, disclosure channels L147, disclosure-timeline factors L148-L152, VEP exclusion L153, CVD-versus-VDP separation L154-L155, resources L156-L171
verified-at: 2026-10-26 (capture fetched this day with `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` — HTTP 200, `text/html; charset=utf-8`, 75,587 raw bytes, raw sha256 383792fd393700210e2a6b8ac38f12c8bc249b85eb60bbbe1976667bab5ca6da at 2026-10-26T21:16:01Z, identical across two fetches — then normalized by the lane's `capture-source.py`; this entry's quotes were re-located in that capture with a whitespace-collapsing matcher)
ground: F06 — multi-party coordinated disclosure, read from the coordinator's own side: this page adds CISA's stage list, its CNA-of-Last-Resort role, and a 45-day earliest-disclosure floor that FIRST's guidelines (S018) do not state; its clock content is distinct from F02's CERT/CC and CISA-supplier-guide figures
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S023   # prints S023:sha256 OK then S023:Q1 OK and S023:Q2 OK, each occurrences=1 with anchor=151-ok and anchor=154-ok (the 45-day floor and the CVD/VDP separation); exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moves; the remaining quotes below are anchored claims, each counted by FC-1 to FC-9

## Attribution

CISA's own program page for its CVD program (title L68-L72: breadcrumb L68-L71, page title L72). It describes the program from the coordinator's side — "CISA plays a vital role in safeguarding national and economic security by coordinating the identification, remediation, and disclosure of cybersecurity vulnerabilities" (L104) — and names its own intake platform:

> "Vulnerability Information and Coordination Environment - New Technologies (VINCE-NT), sponsored, hosted, and managed by CISA" — L89

The capture carries no visible publication date or revision stamp (FC-6), so this entry pins the page as served on 2026-10-26T21:16:01Z rather than to an edition. L1-L71 and L183-L213 are site navigation and footer chrome that the HTML-to-text step kept; every claim below quotes body text between L88 and L171.

## Claim 1 — the statutory authority the page claims

> "for a cybersecurity purpose about security vulnerabilities relating to critical infrastructure in information systems and devices" — L114

The page attaches three citations to that sentence: 6 U.S.C. 659(c)(12) for receiving such information, 6 U.S.C 650(25) for the definition of "security vulnerability", and 6 U.S.C. 659(n) for departmental coordination policies (L114). The breadth it claims is a list of technology classes:

> "This coordination includes vulnerabilities affecting a broad spectrum of technologies such as:" — L104

continuing with operational technology and ICS, IoT devices, medical devices, open source software, artificial intelligence, and IT systems (L105-L110). The stated delivery property is simultaneity:

> "CISA facilitates the timely and synchronized dissemination of vulnerability information and any associated mitigations if available" — L111

## Claim 2 — CISA acts as CVE Top Level Root and CNA of Last Resort, and that role sits inside the pipeline

> "the CISA Top Level Root and the CVE Numbering Authority (CNA) of Last Resort responsibilities" — L112

The sentence says the program "operationalizes" those responsibilities "by assigning CVE identifiers to vulnerabilities reported to CISA" (L112). Step 4 then describes the routing decision rather than a guarantee:

> "CISA determines whether it should receive a CVE ID and identifies which CVE Numbering Authority (CNA) is responsible" — L134

and once a CNA is identified, "that CNA will reserve the CVE ID and gather the information necessary for publication" (L135). For the identifier rules themselves, F07 (S030) is the instrument; this page states the coordinator's role, not the CNA rules.

## Claim 3 — seven stages, with triage criteria and an explicit out-of-scope outcome

The stage list is numbered 1-7 at L116-L146 and is CISA's own decomposition: report submission (L116), intake and triage (L117), coordination (L128), CVE record determination if applicable (L134), advisory development and publication prep (L136), public disclosure (L141), and KEV evaluation (L146). Stage 1 names the reporter classes:

> "An individual (researcher, supplier, etc.) identifies a suspected vulnerability and reports it to CISA through VINCE-NT." — L116

Triage asks five questions — legitimacy, actionability, program scope, whether it is already known or publicly disclosed (including a possible existing CVE), and whether it meets coordination criteria (L119-L123). The outcome split is printed as a two-way branch, "In scope → CVE / Out of scope → Referred / closed" (L125-L126), with the referral rationale:

> "If referred, the report is valid but better handled by another organization or vendor" — L127

So a CVD report is not guaranteed a CVE: stage 4 is titled "CVE Record Determination (If Applicable)" (L134).

## Claim 4 — coordination is a named set of coordinator actions, including mediation

> "the case moves into coordinated disclosure where CISA performs" — L128

followed by supplier identification and outreach, technical analysis and vendor confirmation, timeline tracking, mediation between reporter and vendor when needed, and drafting of advisory language (L129-L133). Mediation between two other parties is the action F06's FIRST-guideline roles describe abstractly; here it is enumerated as a stage of one coordinator's work.

## Claim 5 — disclosure is a multi-channel publication act, and KEV evaluation is a further stage

Stage 5 aligns advisory text, publication timing, supplier and researcher disclosure plans, and cross-stakeholder alignment (L136-L140). Stage 6's outputs are "CISA Advisory", "Publish CVE Record enriched content", "CSAF", and notification of reporters and vendors (L141-L145). The page's summary of disclosure says

> "CISA discloses vulnerabilities through multiple channels to ensure that users receive complete, accurate, and timely information" — L147

and stage 7 is separate:

> "The process continues with the Known Exploited Vulnerabilities (KEV) Evaluation." — L146

The page does not state KEV listing criteria; the feed and its per-record fields are F18 (S052). What this page adds is the sequence — KEV evaluation follows disclosure, it is not a precondition of it.

## Claim 6 — the disclosure timeline is factor-based, and the 45-day figure is a floor for an unresponsive vendor

> "The timeline for disclosure may depend on factors including:" — L148

The four factors are disclosure status (publicly disclosed or actively exploited), potential impact (critical infrastructure, national security, public health), vendor responsiveness, and mitigation availability and timeline (L149-L152). The vendor-responsiveness factor carries the page's only number:

> "CISA may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made" — L151

The captured sentence continues ", regardless of the availability of a patch or update." (L151) — so the 45 days is an earliest-disclosure floor tied to an unresponsive vendor, not a standard disclosure deadline and not an acknowledgement clock for the reporter.

## Claim 7 — CVD reports are outside VEP adjudication, and CVD is not VDP

> "vulnerabilities reported to CISA through the CVD process are no subject to VEP adjudication, per Section 5.4 of the VEP Charter" — L153

("no subject" is the source's wording; the sentence is quoted verbatim). The separation from a policy program is stated in one line and then expanded:

> "The Vulnerability Disclosure Process (VDP) is separate from CVD." — L154

> "A VDP does not involve coordination, remediation, or advisory publication" — L155

The expansion assigns CVD triage, CVE assignment, remediation and advisory publication, and assigns VDP the intake policy for an organisation's own assets — "how an organization receives reports, what is in scope, and what reporters can expect" (L155). This is the same distinction BOD 20-01 draws from the other side (S021, Claim 8); S023 is where a reader confirms that CISA's own coordinator pipeline is not a VDP.

## What a reviewer does with it

- When a report is routed to CISA for coordination, the expected stages are the seven in Claim 3; a report can end at "referred / closed" without a CVE, and stage 4 is expressly conditional.
- Read the 45-day figure as a floor conditioned on vendor unresponsiveness (Claim 6); do not convert it into a deadline for the reporter or a promise that CISA will publish on day 45.
- Keep coordinator side and program side apart: CVD (this page) coordinates third-party products and publishes; VDP (S021's element set) is an organisation's own-asset intake policy.
- For the identifier rules CISA's CNA role applies, use F07 (S030); for KEV membership, F18 (S052); for the FIRST multi-party role model, F06 (S018). This page states the coordinator's sequence, not those rule sets.

## Falsifiable rule and checks

**Falsifiable rule.** Any S023 capture in which (a) the stage list is not seven numbered stages, (b) intake is not VINCE-NT or the CNA-of-Last-Resort sentence disappears, (c) the 45-day sentence loses its "as early as" floor, its unresponsive-vendor condition, or its "regardless of the availability of a patch" tail, (d) the VEP-exclusion sentence changes, or (e) CVD and VDP are merged into one process, makes the claims above false. Run from the lane root.

- **FC-1 — seven numbered stages.** `grep -cE '^[1-7]\. [A-Z]' corpus/source-snapshots/round-40/S023.txt` → `7` (L116, L117, L128, L134, L136, L141, L146).
- **FC-2 — the intake platform is named three times.** `grep -c 'VINCE-NT' corpus/source-snapshots/round-40/S023.txt` → `3` (L89, L116, L146).
- **FC-3 — the last-resort CVE role.** `grep -c 'CNA) of Last Resort' corpus/source-snapshots/round-40/S023.txt` → `1`.
- **FC-4 — one 45-day figure, in the vendor-responsiveness bullet.** `grep -c '45 days' corpus/source-snapshots/round-40/S023.txt` → `1`; the sentence's tail `regardless of the availability` occurs on the same line, `grep -c 'regardless of the availability of a patch or update' corpus/source-snapshots/round-40/S023.txt` → `1`.
- **FC-5 — no money vocabulary.** `grep -ciE 'reward|bounty|payment' corpus/source-snapshots/round-40/S023.txt` → `0`; the page prices nothing.
- **FC-6 — no publication or revision stamp.** `grep -ciE 'published|updated' corpus/source-snapshots/round-40/S023.txt` → `0`; the page states no edition date, which is why the entry pins the fetch instant instead.
- **FC-7 — the VEP sentence is present with its source typo.** `grep -c 'no subject to VEP' corpus/source-snapshots/round-40/S023.txt` → `1`.
- **FC-8 — KEV and CSAF appear only as pipeline outputs here.** `grep -c 'KEV' corpus/source-snapshots/round-40/S023.txt` → `5`; `grep -c 'CSAF' corpus/source-snapshots/round-40/S023.txt` → `3`; neither has a criteria list on this page.
- **FC-9 — every quoted anchor holds its quote.** `python3 -c 'n=lambda s:" ".join(s.split());L=open("corpus/source-snapshots/round-40/S023.txt").read().splitlines();qs=[(89,"Vulnerability Information and Coordination Environment - New Technologies (VINCE-NT), sponsored, hosted, and managed by CISA"),(112,"the CISA Top Level Root and the CVE Numbering Authority (CNA) of Last Resort responsibilities"),(114,"for a cybersecurity purpose about security vulnerabilities relating to critical infrastructure in information systems and devices"),(116,"An individual (researcher, supplier, etc.) identifies a suspected vulnerability and reports it to CISA through VINCE-NT."),(117,"CISA’s Coordinated Vulnerability and Disclosure (CVD) team performs an initial triage"),(127,"If referred, the report is valid but better handled by another organization or vendor"),(128,"the case moves into coordinated disclosure where CISA performs"),(134,"CISA determines whether it should receive a CVE ID and identifies which CVE Numbering Authority (CNA) is responsible"),(147,"CISA discloses vulnerabilities through multiple channels to ensure that users receive complete, accurate, and timely information"),(148,"The timeline for disclosure may depend on factors including:"),(151,"CISA may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made"),(153,"vulnerabilities reported to CISA through the CVD process are no subject to VEP adjudication, per Section 5.4 of the VEP Charter"),(154,"The Vulnerability Disclosure Process (VDP) is separate from CVD."),(155,"A VDP does not involve coordination, remediation, or advisory publication"),(146,"The process continues with the Known Exploited Vulnerabilities (KEV) Evaluation."),(104,"This coordination includes vulnerabilities affecting a broad spectrum of technologies such as:"),(111,"CISA facilitates the timely and synchronized dissemination of vulnerability information and any associated mitigations if available")];ok=sum(n(q) in n(" ".join(L[max(0,a-1):a+3])) for a,q in qs);print("anchors_ok",ok,"of",len(qs))'` → `anchors_ok 17 of 17`.

## Rejected over-generalizations

1. **"45 days is CISA's disclosure deadline."** Rejected: the sentence is "may disclose vulnerabilities as early as 45 days" (L151), a floor, conditioned on a vendor that is "unresponsive or will not establish a reasonable timeframe for remediation" (L151), and three other factors can move the timeline (L148-L152).
2. **"CISA's seven stages are the universal CVD process."** Rejected: the page presents CISA's own program ("CISA plays a vital role…", L104); F06's FIRST guidelines organize the same territory by party roles, not by one coordinator's numbered steps.
3. **"A CVD report always produces a CVE."** Rejected: stage 4 is titled "CVE Record Determination (If Applicable)" (L134) and out-of-scope reports are "Referred / closed" (L126) because another organisation is better placed (L127).
4. **"CVD reports go through VEP adjudication."** Rejected: the page states they "are no subject to VEP adjudication, per Section 5.4 of the VEP Charter" (L153).
5. **"CVD and VDP are the same intake."** Rejected: "The Vulnerability Disclosure Process (VDP) is separate from CVD." (L154), and a VDP "does not involve coordination, remediation, or advisory publication" (L155).
6. **"Being published means being KEV-listed."** Rejected: KEV evaluation is a further stage after public disclosure (L146), and this page states no listing criteria; the feed's fields are F18 (S052).
7. **"Disclosure is simultaneous with the report."** Rejected: the pipeline places intake, triage, coordination, determination and advisory preparation before stage 6 (L116-L145), and the timeline factors include disclosure status and impact (L149-L150).

## Honest limit

- **A self-description.** Every stage, role and figure is CISA describing CISA's own program; the capture contains no reporter-side statistics, no case counts, and no service-level commitment to the reporter beyond the stage list.
- **No reporter clock.** The page states no acknowledgement or triage deadline for a reporter; the only number is the 45-day vendor-responsiveness floor (L151). A reader wanting a reporter-facing clock must go to F02's sources or S021's FAQ.
- **The VEP sentence is ungrammatical in the source** ("are no subject", L153) and the next sentence reads "Lean more about VEP." (L153); both are quoted or cited as captured, not corrected.
- **Two non-breaking-space and interleaved-chrome hazards.** L112 contains U+202F narrow no-break spaces around "CVE Program", "CISA Top Level Root" and "CVE Numbering Authority (CNA) of Last Resort", which the matcher collapses; L117's triage sentence repeats at L118 in the capture, so its quote is not unique by substring and is anchored here rather than pinned in the manifest.
- **A dated pin.** 14,357 snapshot bytes, sha256 52a6671f…6087 at 2026-10-26T21:16:01Z; nothing here describes the page after that fetch.

## Scope and limits

- Pin: `corpus/source-snapshots/round-40/S023.txt`, 213 lines, 14,357 bytes, sha256 `52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087`, bound by the round-40 manifest record (id `S023`, path `S023.txt`, same digest, the program URL, `fetched_utc` 2026-10-26T21:16:01Z, HTTP 200, `text/html; charset=utf-8`). Normalization as recorded: tags stripped, entities unescaped, runs of space/tab/NBSP collapsed, blank lines dropped.
- Body text is L88-L171; L1-L87 and L172-L213 are navigation, resource blurbs and footer, and are not quoted as content except where the page's own resource list restates another document's role (L157-L171).
- `verified-at: 2026-10-26` is the day this entry was written and its quotes re-located in the pin, not a page date.
- Documentation only: the capture carries no credential, session or private URL, and this entry quotes none; the contact addresses it names (`central@cisa.gov`, `cvd@cisa.dhs.gov`, L175) are public CISA inboxes. Nothing here authorises probing, scanning, login or submission against any target.
