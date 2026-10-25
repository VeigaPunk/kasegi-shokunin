# CRA manufacturer reporting duties are not researcher disclosure deadlines
source: S029 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng — Regulation (EU) 2024/2847, OJ 20.11.2024; Articles 14, 15, 16 and 71
verified-at: 2026-10-20
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --selftest

## Rule

For local package review, distinguish a manufacturer's statutory reporting duties
from a researcher's program-specific disclosure arrangements. Article 14 covers
actively exploited vulnerabilities and severe incidents impacting the security of
a product with digital elements; it is not a universal clock for every newly
found bug. Record actor, trigger, awareness time, recipient, notification stage,
and the source of any stated deadline. Do not collapse the two Article 14 tracks.

Article 71 makes Article 14 applicable from 11 September 2026, earlier than the
Regulation's general application from 11 December 2027. This entry opened the
original official text on 2026-10-20; it does not claim a complete review of later
implementing acts, consolidated amendments, jurisdiction, or product applicability.
Actual compliance requires an authorized specialist's assessment of the full law.

## Two separate Article 14 reporting tracks

All durations below are Article 14 outer limits, subject to “without undue delay”
where stated; an outer limit is not permission to wait. The vulnerability and
incident tracks have different final-report triggers.

| Trigger and actor | Stage | Clock (paraphrase; exact wording in the quotes table) | Located support |
|---|---|---|---|
| Manufacturer becomes aware of an actively exploited vulnerability | Early warning | Without undue delay; within 24 hours of awareness | Article 14(2)(a) |
| Same vulnerability | Vulnerability notification | Without undue delay; within 72 hours of awareness, unless relevant information already provided | Article 14(2)(b) |
| Same vulnerability | Final report | No later than 14 days after a corrective or mitigating measure is available, unless relevant information already provided | Article 14(2)(c) |
| Manufacturer becomes aware of a severe incident impacting product security | Early warning | Without undue delay; within 24 hours of awareness | Article 14(4)(a) |
| Same incident | Incident notification | Without undue delay; within 72 hours of awareness, unless relevant information already provided | Article 14(4)(b) |
| Same incident | Final report | Within one month after submission of the incident notification under (b), unless relevant information already provided | Article 14(4)(c) |

Article 14(1) and (3) require simultaneous notification to the CSIRT designated as
coordinator under paragraph 7 and ENISA via the Article 16 single reporting
platform. This describes the statutory recipients, not a claim that a particular
platform is currently operating or a direction to submit anything.

## Exact located quotes

| Location in S029 | Quote (at most 25 words) |
|---|---|
| Article 14(2)(a) | “within 24 hours of the manufacturer becoming aware of it” |
| Article 14(2)(b) | “within 72 hours of the manufacturer becoming aware of the actively exploited vulnerability” |
| Article 14(2)(c) | “no later than 14 days after a corrective or mitigating measure is available” |
| Article 14(4)(a) | “an early warning notification of a severe incident having an impact on the security of the product with digital elements, without undue delay and in any event within 24 hours of the manufacturer becoming aware of it” |
| Article 14(4)(b) | “within 72 hours of the manufacturer becoming aware of the incident” |
| Article 14(4)(c) | “within one month after the submission of the incident notification under point (b)” |
| Article 71 | “Article 14 shall apply from 11 September 2026” |
| Article 71 | “This Regulation shall apply from 11 December 2027.” |

The 24-hour phrase in the first exact-quote row is not unique in the document: the
same words appear in the incident track at Article 14(4)(a) (`S029.txt:20`). The
location column carries the track attribution; a substring recheck cannot
distinguish the two rows, so read the attribution with the table, not from the
bare match.

## Falsifiable local check

Given an authorized synthetic worksheet that labels a severe incident's final
report “14 days after awareness”, reject it: that combines the vulnerability
track's duration with a different start event. The incident track starts its
one-month final-report clock at the submission of the incident notification under
Article 14(4)(b). Likewise reject a worksheet imposing Article 14's 24-hour duty
on every independent finder merely because a bug was found. Identify the actor
and statutory trigger before computing a date; do not infer missing facts.

## Rejected

Rejected: “CRA requires every researcher to publish a vulnerability within
24 hours, and therefore authorizes testing.” Article 14 concerns manufacturers'
notifications of specified events, not public disclosure or testing permission.
Article 15 separately allows voluntary notifications by other natural or legal
persons; it does not establish an asset-scope or testing grant. No legal
protection or compliance conclusion is inferred here.

## Limits

The captured excerpt carries no OJ date line: the `OJ 20.11.2024` attribution in
this entry's `source:` header rests on the ELI URL (`/eli/reg/2024/2847/oj/eng`)
and the 2026-10-20 opening, not on the excerpt bytes.

Documentation-only: no target contact, scanning, login, report submission, or
account operation. The recheck compares a pinned captured excerpt and exact
quotes; it cannot certify current online law, legal advice, applicability to a
specific product, or operation of the reporting platform. Re-open official text
and relevant current implementation material before a real compliance decision.
