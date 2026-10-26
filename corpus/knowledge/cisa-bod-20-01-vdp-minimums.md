# CISA BOD 20-01 — the compulsory federal VDP minimum: required policy elements, prohibited terms, the scope-expansion schedule, target (not remediation) timelines, and the 45-90 day disclosure norm

source: S021 — https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy — capture corpus/source-snapshots/round-40/S021.txt (432 lines, 58,004 bytes; sha256 72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329): title and issuance date L72-L79, web-friendly-version note L91, compulsory-direction and addressee L92-L95, why a VDP L96-L98, bug-bounty contrast L107, required actions L108-L171, policy element list L119-L128, prohibited terms L130-L134, scope expansion L137-L140, handling procedures L141-L155, reporting and CyberScope metrics L156-L171, CISA actions L172-L181, implementation checklist L183-L196, DOJ-aligned template L197-L198, minimums-not-ceiling L204, revocation status of BOD 19-02 and BOD 22-01 L389-L401, no-fix-deadline FAQ L300-L301, 45-90 day norm L305, BOD 19-02 FAQ L310-L313, footnote recommendations 3/7/90 days L379-L384
verified-at: 2026-10-26 (capture fetched this day with `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` — HTTP 200, `text/html; charset=utf-8`, 127,832 raw bytes, raw sha256 fc7267288c8de400d433d911c3336fc573f65ea50d74d1b1a56f82a0cc998a5d at 2026-10-26T21:15:57Z — then normalized by the lane's `capture-source.py`; this entry's quotes were re-located in that capture with a whitespace-collapsing matcher, each `occurrences=1` unless stated)
ground: F03 — authorisation, safe harbour and scope: the compulsory federal VDP element set, its prohibited terms and its scope-expansion schedule; the clock material (target timelines and the 45-90 day norm) extends F02, which holds CISA's supplier guide (S003) and CERT/CC's 45-day figure (S004)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S021   # prints S021:sha256 OK then S021:Q1 OK with occurrences=1 and anchor=133-ok (the no-restriction-on-reporter-disclosure prohibition); exits 2 when the manifest or capture is absent and 1 when the digest differs or that assertion moves; the remaining quotes below are anchored claims, each counted by FC-1 to FC-10

## Attribution

CISA's Binding Operational Directive 20-01, issued "September 02, 2020" (L79), presented as "a web-friendly version of the Cybersecurity and Infrastructure Security Agency's Binding Operational Directive 20-01" (L91). It defines its own instrument class and addressees:

> "A binding operational directive is a compulsory direction to federal, executive branch, departments and agencies" — L92

and "Federal agencies are required to comply with DHS-developed directives." (L94), with a carve-out:

> "These directives do not apply to statutorily defined “national security systems”" — L95

(the carve-out continues to "certain systems operated by the Department of Defense or the Intelligence Community", L95). The authority named is 44 U.S.C. § 3553(b)(2) (L93). This is a federal-agency direction; nothing in it binds a private program, a platform or a researcher.

## Claim 1 — the directive mandates two deliverables: a published policy and handling procedures

> "This directive requires each agency to develop and publish a VDP and maintain supporting handling procedures." — L98

It is issued in support of OMB M-20-32 (L98). The deadlines are relative to issuance: within 30 calendar days, update the .gov registrar security-contact and Organization fields (L112-L114); within 180 calendar days, publish the policy and the handling procedures (L117, L143).

## Claim 2 — the policy's required elements, including anonymous reporting and an explicit authorization commitment

The element list runs L119-L128 under "The policy must include:". It requires scope with a floor:

> "At least one internet-accessible production system or service must be in scope at the time of publication." — L120

> "The types of testing that are allowed (or specifically not authorized)" — L121

and, in the submission description, an anonymity guarantee:

> "A clear statement that reporters may submit a report anonymously." — L125

plus a legal-action commitment:

> "A commitment to not recommend or pursue legal action against anyone for security research activities" — L126

a statement of acknowledgement expectations (L127) and an issuance date (L128).

## Claim 3 — the prohibited terms: no PII requirement, no vetted-only or citizens-only scope, no gag beyond a time limit, no VEP route

The list at L130-L134 is what a policy "must not" do. It may not

> "Require the submission of personally identifiable information." — L131

may not

> "Limit testing solely to “vetted” registered parties or U.S. citizens." — L132

(that item then fixes the affirmative: "The policy must provide authorization to the general public.", L132), may not

> "restrict the reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a reasonably time-limited response period." — L133

and may not

> "Submit disclosed vulnerabilities to the Vulnerabilities Equities Process" — L134

(the item continues "or any similar process", L134). A policy that pre-clears reporters, requires identity, or forbids disclosure outright is outside this element set.

## Claim 4 — scope must grow on a schedule, to everything

> "the scope of the VDP must increase by at least one internet-accessible system or service" — L139

every 90 calendar days after the 270-day mark (L139), and

> "At 2 years after the issuance of this directive, all internet-accessible systems or services must be in scope" — L140

The checklist prints the resulting dates — 2020-10-02, 2021-03-01, 2021-06-01, 2022-09-02 (L186-L196) — and adds that newly launched systems must be in scope after the 180-day mark (L191-L192). Shrinking scope is not provided for in the directive's text; the FAQ warns against removing systems and asks for notice to cyberdirectives@mail.cisa.dhs.gov (L267-L270).

## Claim 5 — handling procedures must exist, but a fix deadline is expressly not mandated

The procedures must describe tracking, internal coordination, impact evaluation, out-of-scope handling, communication and incident assessment, and must set targets for acknowledgement, initial assessment and resolution (L144-L155). The FAQ states the limit of that requirement:

> "The directive does not mandate resolution timelines for addressing vulnerability reports generally" — L301

and the footnote on the resolution target repeats it:

> "Target timelines guide organizational actions and priorities; they are not mandatory remediation dates." — L380

CISA's own recommended targets are 3 business days for acknowledgement, 7 days for assessment and 90 days for resolution (L381-L383). Separately, the BOD 19-02 FAQ says that directive's 15/30-day critical/high clocks apply to Cyber Hygiene-scan findings, not generally to VDP reports (L311-L313).

## Claim 6 — the 45-90 day public-disclosure norm is described as community practice, not as a rule

> "Many in the security research community consider public disclosure of a vulnerability to be appropriate between 45 to 90 days" — L305

The same paragraph warns that a longer imposed delay "may not be unreasonable – and anything more than 90 days begins to veer away from what is reasonable" (L305), and it records that the directive lets an agency require a defined window but not an unreasonable one. So 45-90 days is CISA's description of community expectation for a VDP reporter relationship, distinct from any coordinator's own disclosure clock (F02) and from CISA's CVD program floor (S023 L151).

## Claim 7 — reporting duties: immediate CISA notification, then quarterly CyberScope metrics

After publication, an agency must "immediately report to CISA" certain newly discovered or not-publicly-known vulnerabilities in commercial software or services affecting other parties, coordination needs, and other situations (L157-L160). After 270 days it must report ten metrics through CyberScope:

> "After 270 calendar days following the issuance of this directive, within the first FISMA reporting cycle" — L161

the metrics being report counts, valid counts, open/valid counts, median ages, counts older than 90 days by risk level, and median times to validate, remediate and respond (L162-L171). On CISA's side, it will begin scanning agency .gov sites at the policy path after 180 days (L174) and

> "CISA will not submit any vulnerabilities it receives or helps coordinate under this directive to the Vulnerabilities Equities Process." — L179

## Claim 8 — a VDP is not a bug bounty, and payment is not required

> "A VDP is similar to, but distinct from, a “bug bounty.”" — L107

The paragraph contrasts the two — bounties pay for valid findings and may raise report volume or low-quality submissions (L107) — and the element list says an agency "should consider stating in its policy that reporters will not receive payment" and that

> "reporters will not receive payment for submitting vulnerabilities and that by submitting, reporters waive any claims to compensation" — L129

A linked bounty policy is permitted but not required (L129). So this directive's floor is an authorized intake and response process, not a reward ladder.

## Claim 9 — the element list is a floor, and the template follows DOJ's framework

> "The required actions in this directive are merely the mandated elements of your policy; they are the minimums required, not the ceiling." — L204

CISA's template was "written to align with the Department of Justice's Framework for a Vulnerability Disclosure Program for Online Systems" (L198) — the document this lane holds as S020 — so the two are a pair: S020 is the 2017 design rubric, S021 the 2020 compulsory element set built on its template.

## What a reviewer does with it

- Use the element list (Claim 2) and prohibited terms (Claim 3) as a checklist against a federal VDP: anonymity, public authorization, no PII requirement, disclosure not gagged beyond a reasonable window, no VEP route.
- Do not read approval into the directive's silence: a policy that fixes no remediation deadline is conformant (Claim 5); a program's own timeline claim must come from the program's text.
- Treat 45-90 days as community expectation as CISA describes it (Claim 6), not as a legal deadline; a coordinator's floor (S023) and CERT/CC's figure (F02/S004) are separate statements.
- Re-check instrument status before citing: the same page's related-directives block now lists "BOD 19-02 … (Revoked)" and "BOD 22-01 … (Revoked)" (L398, L401). This entry quotes BOD 20-01's own text only.

## Falsifiable rule and checks

**Falsifiable rule.** Any S021 capture in which (a) the issuance date or compulsory-direction sentence changes, (b) the element list lacks the production-system floor or the anonymous-reporting statement, (c) any of the four "must not" items in Claim 3 disappears, (d) the 2-year all-systems sentence disappears, (e) the FAQ starts mandating a resolution deadline, or (f) the 45-90 day paragraph is stated as a rule rather than community practice, makes the claims above false. Run from the lane root.

- **FC-1 — issuance date.** `grep -c 'September 02, 2020' corpus/source-snapshots/round-40/S021.txt` → `1`.
- **FC-2 — compulsory direction.** `grep -c 'compulsory direction' corpus/source-snapshots/round-40/S021.txt` → `1`.
- **FC-3 — the addressee carve-out.** `grep -c 'national security systems' corpus/source-snapshots/round-40/S021.txt` → `1`.
- **FC-4 — the policy path is named six times.** `grep -c '/vulnerability-disclosure-policy' corpus/source-snapshots/round-40/S021.txt` → `6`.
- **FC-5 — relative-deadline arithmetic.** `grep -c 'calendar days' corpus/source-snapshots/round-40/S021.txt` → `10` (30/180/270-day marks in the directive body and the checklist).
- **FC-6 — the bug-bounty contrast is present, four times.** `grep -c 'bug bounty' corpus/source-snapshots/round-40/S021.txt` → `4`; the word `reward` appears on one line (L107) and only inside that contrast, never as a VDP element.
- **FC-7 — VEP appears only as a prohibition.** `grep -c 'Vulnerabilities Equities Process' corpus/source-snapshots/round-40/S021.txt` → `2` (L134 for the agency, L179 for CISA).
- **FC-8 — anonymity is required twice (element plus FAQ).** `grep -c 'anonymous' corpus/source-snapshots/round-40/S021.txt` → `2`.
- **FC-9 — no mandated fix deadline.** `grep -c 'does not mandate resolution timelines' corpus/source-snapshots/round-40/S021.txt` → `1`.
- **FC-10 — every quoted anchor holds its quote.** `python3 -c 'n=lambda s:" ".join(s.split());L=open("corpus/source-snapshots/round-40/S021.txt").read().splitlines();qs=[(79,"September 02, 2020"),(92,"A binding operational directive is a compulsory direction to federal, executive branch, departments and agencies"),(95,"These directives do not apply to statutorily defined “national security systems”"),(94,"Federal agencies are required to comply with DHS-developed directives."),(98,"This directive requires each agency to develop and publish a VDP and maintain supporting handling procedures."),(120,"At least one internet-accessible production system or service must be in scope at the time of publication."),(121,"The types of testing that are allowed (or specifically not authorized)"),(125,"A clear statement that reporters may submit a report anonymously."),(126,"A commitment to not recommend or pursue legal action against anyone for security research activities"),(131,"Require the submission of personally identifiable information."),(132,"Limit testing solely to “vetted” registered parties or U.S. citizens."),(132,"The policy must provide authorization to the general public."),(133,"restrict the reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a reasonably time-limited response period."),(134,"Submit disclosed vulnerabilities to the Vulnerabilities Equities Process"),(139,"the scope of the VDP must increase by at least one internet-accessible system or service"),(140,"At 2 years after the issuance of this directive, all internet-accessible systems or services must be in scope"),(301,"The directive does not mandate resolution timelines for addressing vulnerability reports generally"),(380,"Target timelines guide organizational actions and priorities; they are not mandatory remediation dates."),(381,"CISA recommends no more than 3 business days from the receipt of the report."),(383,"CISA recommends no more than 90 days from the receipt of the report."),(305,"Many in the security research community consider public disclosure of a vulnerability to be appropriate between 45 to 90 days"),(161,"After 270 calendar days following the issuance of this directive, within the first FISMA reporting cycle"),(107,"A VDP is similar to, but distinct from, a “bug bounty.”"),(129,"reporters will not receive payment for submitting vulnerabilities and that by submitting, reporters waive any claims to compensation"),(179,"CISA will not submit any vulnerabilities it receives or helps coordinate under this directive to the Vulnerabilities Equities Process."),(198,"we’ve created a VDP template which has been written to align with the Department of Justice’s Framework"),(204,"The required actions in this directive are merely the mandated elements of your policy; they are the minimums required, not the ceiling.")];ok=sum(n(q) in n(" ".join(L[max(0,a-1):a+3])) for a,q in qs);print("anchors_ok",ok,"of",len(qs))'` → `anchors_ok 27 of 27`.

## Rejected over-generalizations

1. **"BOD 20-01 requires agencies to fix reported vulnerabilities within a set deadline."** Rejected: "The directive does not mandate resolution timelines for addressing vulnerability reports generally" (L301), and its target-timeline footnote says the dates "are not mandatory remediation dates" (L380). The 15/30-day clocks belong to BOD 19-02's Cyber Hygiene findings, not to VDP reports (L312).
2. **"A conformant VDP must pay bounties."** Rejected: the directive says a policy "must not" be limited to vetted parties and does require general-public authorization (L132), but payment is optional and CISA suggests stating that no payment is made (L129); the FAQ merely permits operating a bounty (L352).
3. **"45-90 days is the federal disclosure deadline."** Rejected: the paragraph attributes the window to what "many in the security research community consider … appropriate" (L305) and warns against delays beyond 90 days; the directive's compulsive verbs are about publishing a policy and procedures, not about a reporter clock.
4. **"The directive bans all restrictions on disclosure."** Rejected: it bans restrictions "except for a request for a reasonably time-limited response period" (L133), so a bounded window is expressly allowed.
5. **"VDP reports may go to the Vulnerabilities Equities Process."** Rejected: the policy "must not" submit disclosed vulnerabilities to VEP or any similar process (L134), and CISA undertakes not to do so either (L179).
6. **"The directive applies to every federal system."** Rejected: it excludes statutorily defined national security systems and certain DoD/Intelligence Community systems (L95), and its addressees are federal executive agencies (L92).
7. **"BOD 20-01 is current federal policy on VDPs as of this capture."** Rejected as stated: the capture's related-directives block lists BOD 19-02 and BOD 22-01 as revoked and BOD 26-04 as current (L389-L401); this entry therefore claims only what BOD 20-01's own text says, and does not assert its present in-force status.

## Honest limit

- **A web-friendly rendering, not the signed directive.** The capture is CISA's HTML rendering of the directive (L91), so footnote numbering is preserved as plain text ("13", "14", "18"-"21" at L132, L134, L152-L155) and the operative text and FAQ share one page; a claim about the signed instrument's layout cannot be made from these bytes.
- **The FAQ is guidance, not operative text.** Claims 5 and 6 rest on the FAQ section (L300-L305), which states what the directive does not require and what the community expects; the directive body's only clock statements are the 30/180/270-day action deadlines and the 2-year mark (L112-L143).
- **Dates are issuance-relative.** The directive prints absolute milestones for one issuance date (L186-L196); a different issuance date would move them, so they are evidence about 2020-09-02, not about any later directive.
- **A dated pin.** 58,004 snapshot bytes, sha256 72dbba57…e329 at 2026-10-26T21:15:57Z; nothing here describes the page after that fetch.

## Scope and limits

- Pin: `corpus/source-snapshots/round-40/S021.txt`, 432 lines, 58,004 bytes, sha256 `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329`, bound by the round-40 manifest record (id `S021`, path `S021.txt`, same digest, the directive URL, `fetched_utc` 2026-10-26T21:15:57Z, HTTP 200, `text/html; charset=utf-8`). Normalization as recorded by that record: `<script>`/`<style>` removed, block tags to newlines, remaining tags stripped, entities unescaped, whitespace collapsed, blank lines dropped.
- **Quotes spanning line breaks** (L92 is a single line; L98, L120, L129, L133, L139, L140, L161, L179, L198, L204, L301, L305, L380 are single lines or were verified across their wrap) are matched under whitespace collapse; FC-10 reproduces all 27.
- `verified-at: 2026-10-26` is the day this entry was written and its quotes re-located in the pin, not the directive's issuance date.
- Documentation only: the capture carries no credential, session or private URL, and this entry quotes none; the two contact addresses it names are public CISA inboxes. Nothing here authorises probing, scanning or submission against any target.
