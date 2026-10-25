# CWE Top 25 2025 Methodology
source: S013 — https://cwe.mitre.org/top25/archive/2025/2025_methodology.html — “Removal of CWE Mapping Normalization”
verified-at: 2026-10-19

## Rule
When a report cites the 2025 CWE Top 25, identify it as an aggregate ranking for that edition and map the reported root cause to a CWE using the technical evidence, not rank alone.
Do not treat a Top 25 rank as a target-specific risk score, exploitability finding, scope decision, or reward predictor.
Any year-over-year comparison must disclose the change from View-1003 normalization to the 2025 use of provided CWE mappings, and state that the ranking score used CVSS 3.0 or 3.1 records.
A reviewer can compare the report’s CWE, edition, and trend statement with the cited methodology; if the technical root cause or comparison basis is missing, mark the inference unsupported.
Practical interpretation checks:
- name the exact 2025 edition and its dataset window;
- support the report’s root-cause CWE with case-specific technical evidence;
- state the mapping-normalization change when comparing with earlier years;
- state the CVSS 3.0/3.1 limitation when describing the ranking formula;
- distinguish an aggregate rank from target-specific severity or exploitability;
- do not select a case’s CWE solely because it appears in the ranked list.
If a comparison does not disclose its basis, omit the trend conclusion rather than imply equivalence.
This keeps aggregate population evidence separate from a particular report’s scope and impact.

## Evidence
- S013, opening methodology summary: “This year’s dataset included 39,080 CVE Records for vulnerabilities published between June 1, 2024 and June 1, 2025.”
- S013, “Removal of CWE Mapping Normalization”: “For the first time in 2025, the Top 25 used the actual CWE mappings as provided, without normalizing them back to View-1003.”
- S013, “Scoring”: “only CVE Records that contain CVSS version 3.0 or 3.1 data were considered in the calculations.”
- S014, “Abstraction”: “For root cause mapping, CWE recommends that Base and Variant level CWEs should be used whenever possible”. This is MITRE’s mapping guidance.
- S014, “Possible Causes of Rank Shifts”: “The shift in scoring and the fewer CWE mappings in NVD data in 2024 also contributed to this.” MITRE lists methodology and data changes as possible contributors, not a single proven cause.
- S015, 2025 ranked list, first item: “Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')”. The list is an edition-specific population ranking, not a per-target assessment.

## Kasegi use
Use SKILL.md’s “Evidence-package anatomy”: the report’s vulnerability class and impact remain tied to observed evidence and the program’s severity language.
Use “Disclosure anti-patterns (all observed in fleet wrap review)” to avoid inflating severity from a label or rank.
A CWE mapping can make a root-cause explanation more precise, but it does not replace reproduction, affected-asset scope, or a program-specific impact assessment.

## Rejected
Rejected: “A weakness in the 2025 Top 25 is therefore likely to be exploitable or rewarded on this target.”
The ranking summarizes CVE records in a defined dataset and formula; it does not establish a particular package’s flaw, reachability, authorization, severity, or reward.

## Limits
S013 and S014 are MITRE’s published method and interpretation of its own 2025 analysis; the result is attributed to MITRE, not presented as an independent prevalence census.
The dataset window, mapped-record set, and CVSS versions bound the published result; the ranking is not a universal measure of current risk.
S015 supplies the ranked 2025 list but does not replace its methodology or a technically supported root-cause mapping.
This entry concerns interpretation of public documentation only and gives no instruction to inspect or test a target.

Round-23 recheck clarification: the command checks exact quoted support in pinned
captured-source excerpts, not current online freshness or a complete entry audit.
The 2025 edition is a dated methodology; re-open official material for current
ranking or cross-year comparison claims.
