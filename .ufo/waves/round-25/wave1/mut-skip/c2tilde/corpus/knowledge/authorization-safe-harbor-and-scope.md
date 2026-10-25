# Authorization, Safe Harbor, and Scope
source: S006 — https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq — “How to Enable Safe Harbors (Program Owners & Admins)”
verified-at: 2026-10-19
recheck: cd ~/Projects/shokunin/kasegi-shokunin && true

## Rule
For a program record, preserve safe-harbor language, the explicit asset scope, the testing grant, and prohibited methods as separate observations.
A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that the program’s policy excludes.
A reviewer can check this rule against the program’s policy text: every claimed asset and action must be supported by the observed scope and authorization terms, not only by a platform indicator.
Practical review checks:
- identify the actual program policy, not only the platform summary;
- list the assets that the policy explicitly includes;
- preserve the grant and prohibited-method wording separately;
- record partial or conditional safe harbor as described by its source;
- keep missing scope or authorization evidence marked unknown.
When a badge is the only observed fact, record the badge but do not infer an asset or action grant.
This check distinguishes a policy representation from a case-specific authorization decision.

## Evidence
- S006, “How to Enable Safe Harbors (Program Owners & Admins)”: “Adopting a Safe Harbor does not change the program scopes.”
- S006, “What is safe harbor?”: “a statement from an organization that security and AI researchers engaged in Good Faith Security Research and ethical disclosure are authorized to conduct such activity”. This is HackerOne’s description of its concept, not a universal legal conclusion.
- S007, “Disclose.io”, Scope bullet: “An exhaustive list of In-Scope properties that the organization is explicitly providing safe harbor for”. Bugcrowd presents this as a recommended program-owner commitment.
- S007, “Safe Harbor”: “does not represent the same level of commitment as full safe harbor.” This describes Bugcrowd’s partial-safe-harbor status.
- S008, “Introduction”: “what systems and types of research are covered under this policy”. The CISA page describes a template for agencies, not a blanket grant.
- S008, “Test Methods”: “The following test methods are not authorized:”. The template treats method prohibitions separately from its authorization section.

## Kasegi use
Apply SKILL.md’s “Program-rule checklist (step 1 of any mission)”: it records exact assets, a verbatim testing grant, prohibitions, and safe_harbor as observed, including null when absent.
Use SKILL.md’s “Policy access playbook (fleet-learned)” to distinguish a public policy artifact from evidence of scope or grant.
Keep platform terminology attributed to the platform; do not silently turn an indicator into permission.

## Rejected
Rejected: “A safe-harbor badge authorizes every asset and every testing method.”
HackerOne explicitly says its safe harbor does not change program scopes, while the other sources describe scope and method boundaries separately.

## Limits
S006 and S007 explain their respective platforms’ safe-harbor models; their terms are not interchangeable with every program’s policy.
S008 is a CISA template written to help agencies create a VDP aligned with BOD 20-01; it is not a universal policy or legal opinion.
These sources do not resolve third-party asset ownership, external legal protection, or whether an unlisted activity is authorized in a particular jurisdiction.
This entry is a documentation review rule and does not instruct anyone to test a system.

Round-23 recheck clarification: the command checks exact quoted support in pinned
captured-source excerpts, not current online freshness, a complete entry audit,
or a particular program's authorization. Re-open the actual policy before any
authorization decision. The S006 quote's location in this entry was already
correct; the filed r22 Gate location is corrected in the round-23 lesson.
