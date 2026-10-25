# Coordinated Disclosure Timelines
source: S003 — https://www.cisa.gov/resources-tools/resources/establishing-coordinated-vulnerability-disclosure-program-work-security-researchers — PDF p. 6, “Establish Reasonable Time Frames for Remediation and Disclosure of Reported Vulnerabilities”
verified-at: 2026-10-19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S003 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S004 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S005

## Rule
A disclosure timeline in a report or case record must name the policy or coordinator, the event that starts its clock, the stated interval, the patch/publication relationship, and any documented extension or exception.
Do not describe one interval as the universal researcher deadline.
A reviewer can check the cited policy against each recorded trigger and date; if the applicable policy or its trigger is not identified, mark the timeline unknown.
For each recorded timeline, check:
- the policy or coordinator is named;
- the clock trigger and its date are stated;
- the patch and publication conditions are not conflated;
- any extension names its documented condition;
- the record distinguishes a fixed deadline from a negotiated starting point.
If a policy states an interval without an identifiable trigger, record the date as unknown.
Do not transplant CERT/CC or Project Zero intervals into another policy record.

## Evidence
- S003, PDF p. 6, “Establish Reasonable Time Frames for Remediation and Disclosure of Reported Vulnerabilities”: “A time frame may be a fixed period, a minimum or maximum, or a negotiated default starting point.”
- S003, same section: “Suppliers and researchers should work collaboratively to adjust embargo periods” as necessary; this is supplier-facing best-practice guidance, not a universal clock.
- S004, opening paragraph, “Vulnerability Disclosure Policy”: “Vulnerabilities reported to the CERT/CC will be disclosed to the public 45 days after the initial report”. This is CERT/CC’s stated policy and trigger.
- S004, same paragraph: “may result in earlier or later disclosure.” CERT/CC attributes adjustments to extenuating circumstances.
- S005, “What is Project Zero’s 90-day disclosure deadline policy?”: “this bug report will become public 30 days after the fix was made available.” This is Project Zero’s policy when a fix is available before its deadline.
- S005, “What happens if a patch isn’t broadly available after 90 days?”: “we grant a 14-day grace extension only when there’s a commitment by the developer to ship a fix within the 14-day grace period.”

## Kasegi use
SKILL.md’s “Evidence-package anatomy” requires the report to carry a disclosure timeline; SKILL.md’s “VDP disclosure packages (sibling format)” records disclosure routes and timestamps as part of its separate package shape.
Use “Program-rule checklist (step 1 of any mission)” to retain the actual policy record, and bind any timeline to that record rather than importing another coordinator’s interval.
Keep the policy’s own exceptions and patch trigger visible in the report; an unobserved date stays unknown.

## Rejected
Rejected: “All vulnerability reports use a 90-day disclosure deadline.”
CISA’s supplier guide allows several ways to define a timeframe, while CERT/CC and Project Zero state different, attributed policies and conditions.

## Limits
S003 is joint supplier guidance about program design; it does not prescribe a single deadline for every researcher or coordinator.
S004 describes CERT/CC’s own policy, and S005 describes Project Zero’s own policy; neither establishes a general legal requirement.
A policy may change after this verification date, so do not reuse a stale timeline without reopening its source.
This entry describes policy review only and does not direct disclosure or contact with any target.

Round-23 recheck clarification: the command checks exact quoted support in pinned
captured-source excerpts, not current online freshness or a complete entry audit.
Re-open the applicable official policy before using its current timeline.
