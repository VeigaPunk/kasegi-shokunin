# DOJ CCIPS Framework for a Vulnerability Disclosure Program for Online Systems (v1.0, July 2017) — scoping the program, the third-party authorization limit, the CFAA "authorized conduct" frame, and the consequences a policy may publish

source: S020 — https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline= — capture corpus/source-snapshots/round-40/S020.txt (319 lines, 16,693 bytes; sha256 8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c): title and version L6-L8, purpose and non-prescription L19-L24, CFAA purpose sentence L40-L42, footnote 1 third-party limit L25-L27, footnote 3 "assistance, not authority" L35-L38, footnote 4 CFAA elements L72-L79, footnote 5 counsel L80-L83, Step 1 scope factors L45-L65, third-party interests L133-L137, cloud-provider passage L139-L151, Step 2 reporting and accidental-violation handling L167-L227, Step 3 plain-language authorization L229-L245, scope listing forms L246-L260, consequences L279-L293, coordination centre L297-L304, Step 4 L307-L318
verified-at: 2026-10-26 (capture fetched this day by the lane's `corpus/instruments/capture-source.py --id S020 --kind pdf` from a 140,909-byte `application/pdf` response, HTTP 200, raw sha256 d0cfa766a29328e120be7187435d09e5aef374c80bcbf0b1bd7a167c16e51ee7 at 2026-10-26T21:16:10Z; this entry's quotes were re-located in that capture with a whitespace-collapsing matcher, each `occurrences=1`)
ground: F09 — the United States statutory/guidance arm of authorisation that exists outside a platform's safe-harbour text; extends F03 (a platform's own safe-harbour statement) and sits beside the Japanese statutory arm (S032-S035), adding DOJ's own CFAA frame, its third-party-authorisation limit and the commitments a policy may publish
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S020   # prints S020:sha256 OK then S020:Q1 OK with occurrences=1 and anchor=142-ok (the cloud-provider passage at L142-L145); exits 2 when the manifest or capture is absent and 1 when the digest differs or that assertion moves; the remaining quotes below are anchored claims, each counted by FC-1 to FC-8

## Attribution

A guidance document by the U.S. Department of Justice, Criminal Division, Cybersecurity Unit of the Computer Crime & Intellectual Property Section (L1-L4). It states its own genre twice: it "has prepared this framework to assist organizations interested in instituting a formal vulnerability disclosure program" (L19-L20) and it "provides a rubric of considerations that may inform the content of vulnerability disclosure policies" (L20-L21). Footnote 3 disclaims authority in terms:

> "This guidance is intended as assistance, not authority." — L35

The version is fixed at "Version 1.0 (July 2017)" (L8), and footnote 1 narrows the subject matter: third-party vulnerability disclosure and hands-on examination "may raise legal issues not addressed by this guidance" (L25-L26). So anything below is DOJ's 2017 guidance about online systems and services, not a statute, not a charging policy, and not a safe harbour.

## Claim 1 — the framework is deliberately non-prescriptive about form and objectives

> "The framework does not dictate the form of or objectives for vulnerability disclosure programs" — L21

The next sentence concedes variety — "different organizations may have differing goals and priorities for their vulnerability disclosure programs" (L23) — and the framework then offers only a four-step process (Steps 1-4 at L44, L167, L229, L307). A reader looking for a required element list will not find one here; S021's federal directive supplies that, and its own template is written "to align with the Department of Justice's Framework" (S021 L198).

## Claim 2 — in DOJ's frame the policy's job is to reduce CFAA exposure by describing authorised conduct

The process is introduced by one sentence that carries the document's purpose:

> "substantially reducing the likelihood that such described activities will result in a civil or criminal violation of law" — L41

The clause's subject is the policy that "will clearly describe authorized vulnerability disclosure and discovery conduct" (L40); the statute named at the end of the sentence is the Computer Fraud and Abuse Act, 18 U.S.C. § 1030 (L42). Footnote 2 defines "vulnerability" by reference to the Common Weakness Enumeration definition rather than inventing one (L29-L33).

## Claim 3 — scope is a set of design decisions, and the framework names the one it cannot settle

Step 1 begins by asking whether to include all network components and data or a subset (L45-L46), then lists the factors that may influence the answer: information sensitivity (L50-L53), existing safeguards such as encryption at rest (L57-L58), the organisation's ability to segment its network (L60-L61), and restrictions imposed from outside:

> "Regulatory, contractual, or other restrictions placed on disclosure of protected classes of information in an organization’s possession" — L63

Footnote 5 adds that an organisation weighing sensitive information "should consider consulting with legal counsel when making its scoping decisions" (L82-L83). Step 3.B then requires the policy to name the included components "as specifically as possible" (L248-L249) and offers four listing forms — white listing by domain, black listing of exclusions, only public systems, or any publicly accessible system (L251-L260).

## Claim 4 — third-party interests are an authorization limit, not a scoping preference

This is the passage the registry row asks about, and it is stated as a limit on the organisation's power to authorize:

> "Absent an agreement with the cloud service provider, the organization implementing the vulnerability disclosure program may lack the authority to authorize others" — L142

The paragraph's example is a cloud storage provider whose servers hold the organisation's data alongside other tenants' data (L139-L142). It then points at the contract rather than at the policy:

> "A service-level contract between an organization and its cloud storage provider may address questions regarding authorization" — L147

with counsel "best situated to determine whether this issue is addressed by contract" (L149-L151). The general rule is stated one step earlier — components that "implicate[] third-party interests" should either be excluded "or require the organization to obtain additional authorization before including them" (L133-L137).

## Claim 5 — the CFAA frame: without authorization or in excess of it, and not only domestic conduct

Footnote 4 is the only place the capture states the statute's elements:

> "without authorization or in excess of authorization and obtaining information from such a computer" — L73

It defines "protected computer" by 18 U.S.C. § 1030(e)(2) and "damaging" by § 1030(e)(8), then addresses reach:

> "The CFAA’s scope is not limited to purely domestic conduct." — L76

The footnote's example is symmetric — a U.S. computer accessed from abroad, or a foreign computer accessed from the United States (L76-L79). Nothing in the capture states an enforcement threshold, a prosecutorial policy, or a penalty.

## Claim 6 — the policy must say in plain terms what is and is not authorised

Step 3.A opens with the instruction the whole document turns on:

> "Describe authorized and unauthorized conduct in plain, easily understood terms." — L232

The sub-items make it concrete: identify techniques or tactics the organisation does not authorise (L234-L235), explain limits on accessing, copying, using or retaining its data (L237-L238), consider a prohibition on destructive conduct (L240-L242), and "Avoid using vague jargon or ambiguous technical language" about acceptable and unacceptable conduct (L244-L245).

## Claim 7 — the consequences section: three example commitments, and what they are not

Step 3.D frames the following as examples — "For example, a policy might state that—" (L281):

> "The organization will not to pursue civil action for accidental, good faith" — L283

(the source's own wording, including "not to pursue", is quoted verbatim), and

> "The organization considers activities conducted consistent with the policy to constitute “authorized” conduct" — L287

and, for a third-party suit:

> "If legal action is initiated by a third party against a party who complied" — L290

The third example continues that the organisation "will take steps to make it known, either to the public or to the court, that the individual's actions were conducted in compliance with the policy" (L291-L293). These are policy sentences an organisation may adopt; the framework's own footnote 3 says it creates no enforceable rights, so a package must quote the program's policy for the commitment, never the framework.

## Claim 8 — decide accidental-violation handling before launch, and name a coordination route

Step 2.D sets a pre-launch decision:

> "decide how it will handle accidental, good faith violations of the vulnerability disclosure policy, as well as intentional, malicious violations" — L226

and Step 3.F asks for a route out of single-party handling:

> "a process for contacting a coordination center in case a vulnerability also affects others organizations’ services or systems" — L298

naming US-CERT, CERT/CC and ICS-CERT as examples that "can make additional notifications to affected parties" (L301-L304).

## What a reviewer does with it

- When a program claims scope over supplier-hosted or cloud-hosted assets, ask for the provider agreement or the contract clause the framework points at (Claim 4). The framework does not let the program's own policy substitute for the provider's authorization.
- When a policy says activity is "authorized" but names neither techniques nor data-handling limits, it is not the plain-language description Step 3.A asks for (Claim 6).
- Read the framework as a design rubric: it prescribes no element set, no clock, no payment and no disclosure deadline (Claim 1; FC-6 shows no bounty, payment or reward vocabulary at all).
- For the binding federal element list built on this framework's template, read S021; for the platform-side safe-harbour statement, read F03; for the Japanese statutory arm, read F09's S032-S035.

## Falsifiable rule and checks

**Falsifiable rule.** Any S020 capture in which (a) the version line is not "Version 1.0 (July 2017)", (b) the "assistance, not authority" disclaimer is absent, (c) the step count is not four, (d) the cloud-provider passage no longer conditions authority on an agreement with the provider, or (e) the CFAA footnote no longer states the excess-of-authorization and non-domestic-conduct elements, makes the claims above false. Run from the lane root.

- **FC-1 — version line.** `grep -c 'Version 1.0 (July 2017)' corpus/source-snapshots/round-40/S020.txt` → `1`.
- **FC-2 — the disclaimer.** `grep -c 'assistance, not authority' corpus/source-snapshots/round-40/S020.txt` → `1`.
- **FC-3 — four steps.** `grep -cE '^Step [1-4]:' corpus/source-snapshots/round-40/S020.txt` → `4`.
- **FC-4 — the statute is named three times.** `grep -c 'Computer Fraud and Abuse Act' corpus/source-snapshots/round-40/S020.txt` → `3` (L40-L42, L287-L288, plus the footnote-4 expansion at L72-L73).
- **FC-5 — the third-party limit is stated once.** `grep -c 'implicates third-party interests' corpus/source-snapshots/round-40/S020.txt` → `1`.
- **FC-6 — no money vocabulary anywhere.** `grep -ciE 'bounty|payment|reward' corpus/source-snapshots/round-40/S020.txt` → `0`; the framework prices nothing and promises no compensation.
- **FC-7 — every quoted anchor holds its quote.** `python3 -c 'import re,sys;n=lambda s:" ".join(s.split());L=open("corpus/source-snapshots/round-40/S020.txt").read().splitlines();qs=[(8,"Version 1.0 (July 2017)"),(35,"This guidance is intended as assistance, not authority."),(21,"The framework does not dictate the form of or objectives for vulnerability disclosure programs"),(41,"substantially reducing the likelihood that such described activities will result in a civil or criminal violation of law"),(63,"Regulatory, contractual, or other restrictions placed on disclosure of protected classes of information in an organization’s possession"),(142,"Absent an agreement with the cloud service provider, the organization implementing the vulnerability disclosure program may lack the authority to authorize others"),(147,"A service-level contract between an organization and its cloud storage provider may address questions regarding authorization"),(73,"without authorization or in excess of authorization and obtaining information from such a computer"),(76,"The CFAA’s scope is not limited to purely domestic conduct."),(232,"Describe authorized and unauthorized conduct in plain, easily understood terms."),(287,"The organization considers activities conducted consistent with the policy to constitute “authorized” conduct"),(283,"The organization will not to pursue civil action for accidental, good faith"),(290,"If legal action is initiated by a third party against a party who complied"),(226,"decide how it will handle accidental, good faith violations of the vulnerability disclosure policy, as well as intentional, malicious violations"),(298,"a process for contacting a coordination center in case a vulnerability also affects others organizations’ services or systems")];ok=sum(n(q) in n(" ".join(L[max(0,a-1):a+3])) for a,q in qs);print("anchors_ok",ok,"of",len(qs))'` → `anchors_ok 15 of 15`.
- **FC-8 — the subject-matter carve-out is present.** `grep -c 'may raise legal issues not addressed' corpus/source-snapshots/round-40/S020.txt` → `1`.

## Rejected over-generalizations

1. **"The DOJ framework authorizes testing."** Rejected: it says of itself "This guidance is intended as assistance, not authority" (L35) and creates no enforceable rights (L35-L37). The authorisation, if any, comes from the organisation's published policy and, for third-party assets, from the third party (Claim 4).
2. **"A cloud-hosted asset can be put in scope like any other."** Rejected: Step 1.C makes inclusion of third-party-implicated components depend on exclusion or "additional authorization" (L133-L137), and states that without a provider agreement the organisation "may lack the authority to authorize others" (L142-L145).
3. **"The framework's non-prosecution sentence binds DOJ."** Rejected: it is offered as an example policy sentence ("a policy might state that—", L281) for the organisation to adopt, and the document disclaims creating rights or benefits (L35-L37).
4. **"The CFAA reaches only conduct inside the United States."** Rejected: footnote 4 states the opposite — "The CFAA’s scope is not limited to purely domestic conduct." (L76) — with a two-direction example (L76-L79).
5. **"A VDP is a bug bounty, so it needs a payment ladder."** Rejected: the capture contains no bounty, payment or reward token at all (FC-6) and sets no money terms; its consequences are the civil-action and "authorized" statements in Claim 7.
6. **"The four 2017 steps are the current federal process."** Rejected: the capture is "Version 1.0 (July 2017)" (L8) and says nothing about later federal directives; the binding element list is S021's, read there.

## Honest limit

- **Guidance, not law.** The document disclaims authority (L35-L38) and addresses only online systems and services, carving out third-party disclosure and hands-on examination (L25-L27). It contains no case law beyond a citation in that disclaimer (L36-L38) and states no current DOJ charging policy; the 2022 policy is a different document and is not in this capture.
- **"May", not "must".** The framework's verbs are "consider" and "should" (L133-L137, L225-L226, L298); the only near-prescriptive sentences are the plain-language and specific-scope instructions in Step 3 (L232, L248-L249), and even those are framed as what the policy should do.
- **One quote is the source's own typo.** "The organization will not to pursue civil action…" (L283) is quoted as captured; a cleaner sentence is not in the bytes.
- **A dated pin.** This is the July 2017 v1.0 PDF as served on 2026-10-26T21:16:10Z (16,693 snapshot bytes, sha256 8fc334be…5458c); the entry says nothing about the document after that fetch.

## Scope and limits

- Pin: `corpus/source-snapshots/round-40/S020.txt`, 319 lines, 16,693 bytes, sha256 `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c`, bound by the round-40 manifest record (id `S020`, path `S020.txt`, same digest, the PDF URL above, `fetched_utc` 2026-10-26T21:16:10Z, response `application/pdf`, `content-disposition: inline; filename=csu-vulnerability-program-framework-final.pdf`). The capture is `capture-source.py pdf_to_text()` output: `pdftotext -enc UTF-8`, whitespace collapsed, blank lines dropped — so page furniture ("1|Page" … "8|Page") survives at L39, L84, L172, L214, L261, L305, L319 and footnotes are interleaved with body text where the PDF places them.
- **Quote matching is whitespace-collapsed.** Several quoted sentences span line breaks (L41, L63, L73, L142, L147, L226, L287, L290, L298); each was verified with a collapsing matcher, and FC-7 reproduces that check.
- `verified-at: 2026-10-26` is the day this entry was written and its quotes re-located in the pin, not the document's own date.
- Documentation only: the capture carries no credential, session or private URL, and this entry quotes none. Nothing here authorises probing, scanning, or submission against any target.
