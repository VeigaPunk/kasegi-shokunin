# A rules-of-engagement document is the test authorisation, and its scope is an exclude list too
source: S032 — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf — NIST SP 800-115, Technical Guide to Information Security Testing and Assessment, September 2008; Appendix B (printed B-1–B-3), §1.4 (printed 1-2), glossary (printed F-2)
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S032 (
ground: F09 (new frontier item; extends F03, which holds the platform-side safe-harbour statement only)

## Rule

Before a security test begins, the parties sign one document that both **grants**
authority and **bounds** it. NIST SP 800-115 gives that document a name — the
rules of engagement (ROE) — and a template (Appendix B). For package review, treat
a claim as authorised only against the ROE's written scope and constraints for the
specific engagement; a resume, a chat message or a platform's safe-harbour badge is
not that document.

The ROE's scope section is not a permission list. NIST's own template pairs an
in-scope statement with an **exclude list**, and names out-of-scope actions and
expected outcomes as the boundary the test is measured against. A finding produced
outside that boundary is unauthorised even when the target is "obviously" the
customer's.

## What the template actually contains (and what it does not)

Appendix B is a template with labelled sections, not a mandate. Its own footnote
says the template is "intended to be illustrative": an ROE that omits a section is
not defective for that reason alone.

| Appendix B area | What it asks the parties to state | Printed page |
|---|---|---|
| 1. Introduction | Purpose, scope, assumptions/limitations, risks, document structure | B-1 |
| 1.2 Scope | Test boundaries as actions and expected outcomes; in-scope list plus exclude list | B-1 |
| 2. Logistics | Personnel, schedule, test site, **source/destination location from which testing is authorised** | B-1–B-2 |
| 3. Communication Strategy | General communication; incident handling and response | B-2 |
| 4. Target System/Network | What is under test | B-3 |
| 5. Testing Execution | Nontechnical/technical components; **data handling** for sensitive test data | B-3 |
| 6. Reporting, 7. Signature Page | Deliverables and the parties' signatures | B-3 |

Measured absence, checked against the capture: Appendix B contains **no**
"authorization letter", **no** "escalation" label and **no** evidence/chain-of-custody
section. Conferral of authority is stated in the glossary and in the body's §6.5/§7.2,
not inside Appendix B. Do not cite Appendix B for those.

## Exact located quotes

| Location in S032 | Quote (at most 25 words) |
|---|---|
| Glossary (F-2) | "Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information security testing." |
| Glossary (F-2) | "The ROE is established before the start of a security test" |
| Glossary (F-2) | "authority to conduct defined activities without the need for additional permissions" |
| §1.4 (1-2) | "Appendix B provides a template for creating Rules of Engagement (ROE)." |
| App. B §1.2 (B-1) | "Identifies test boundaries in terms of actions and expected outcomes." |
| App. B §2.3 (B-2) | "Identifies the location or locations from which testing is authorized." |

## Falsifiable local check

Given an authorized synthetic claim package, ask one question: does the cited
authorisation name the **actions** and the **destinations** the tester used? If the
package cites an ROE whose scope section lists only assets and no excluded actions
or source locations, reject the "authorised" label and ask for the missing scope
statement — NIST's template asks for both, so their absence is a package defect,
not a stylistic choice. The same test rejects a package that cites a platform
policy as its engagement authorisation: a platform policy is a third party's
position about its own assets, not the customer's grant for this engagement.

## Rejected

Rejected: "an ROE, once signed, authorises anything the customer owns." The
glossary ties authority to *defined activities*; Appendix B §1.2 defines the
boundary by actions and expected outcomes and includes an exclude list. A signed
ROE that names a narrower activity set therefore narrows, not widens, the grant.

## Limits

This entry does not restate F03 (`authorization-safe-harbor-and-scope.md`), which
holds what a platform's safe-harbour statement does and does not add to asset
scope; read it first. It adds the owner-side engagement instrument and the
template's shape.

The capture is a `pdftotext` render of the PDF NIST serves today (fetched
2026-10-25, sha256 pinned in the manifest); the PDF's embedded ModDate is later
than its 2008 printed date, so the pinned bytes are a re-save, not necessarily the
2008 original. Quoting is by printed page marker; page numbers in a rendered PDF
may differ.

Documentation-only: no target contact, scanning, login, report submission or
account operation. This is a published method document, not legal advice and not a
statement that any particular engagement was authorised.
