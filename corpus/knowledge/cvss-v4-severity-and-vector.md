# CVSS v4 Severity and Vectors
source: S001 — https://www.first.org/cvss/v4.0/user-guide — “CVSS Base Score (CVSS-B) Measures Severity, not Risk”
verified-at: 2026-10-19
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S002

## Rule
For every report or package that publishes a CVSS v4.0 number, publish the CVSS vector string and a nomenclature label identifying the metric groups used: CVSS-B, CVSS-BE, CVSS-BT, or CVSS-BTE.
If only Base metrics were assessed, label the score CVSS-B; do not present that score alone as a complete risk assessment, program severity decision, or reward decision.
A reviewer can check each number against its vector and label; if the vector is missing or the label does not match the metric groups, the published score is incomplete.
Practical review checks:
- confirm that the displayed score and vector use the same CVSS version;
- confirm that the CVSS-B, CVSS-BE, CVSS-BT, or CVSS-BTE label matches the vector’s groups;
- keep the nomenclature beside every numerical score display;
- identify the consumer context for any selected Threat or Environmental values;
- describe Supplemental metrics as context, not as score-changing inputs;
- keep a Base-only value labeled CVSS-B rather than implying contextual groups.

## Evidence
- S001, “CVSS Nomenclature”: “Numerical CVSS Scores have very different meanings based on the metrics used to calculate them.”
- S001, “CVSS Nomenclature” table row CVSS-B: “Base metrics”.
- S001, “CVSS Nomenclature” table row CVSS-BE: “Base and Environmental metrics”.
- S001, “CVSS Nomenclature” table row CVSS-BT: “Base and Threat metrics”.
- S001, “CVSS Nomenclature” table row CVSS-BTE: “Base, Threat, Environmental metrics”.
- S001, “CVSS Nomenclature” > Additional Notes: “This nomenclature should be used wherever a numerical CVSS value is displayed or communicated.”
- S001, “CVSS Base Score (CVSS-B) Measures Severity, not Risk”: “CVSS Base (CVSS-B) scores are designed to measure the severity of a vulnerability and should not be used alone to assess risk.”
- S002, “Assessment”: “This vector string is a specifically formatted text string that contains each value assigned to each metric, and should be displayed with the vulnerability score.”
- S002, “Assessment”: “Assessment of the Threat and Environmental metrics is not required, but is highly recommended for more meaningful results.”
- S002, “Introduction”: “These factors are outside the scope of CVSS.” This refers to additional organizational factors such as regulatory requirements and monetary losses.
- S002, “Supplemental Metrics”: “No metric will, within its specification, have any impact on the final CVSS score”. The source continues “(e.g. CVSS-BTE).”; the quoted fragment is not a complete sentence.

## Kasegi use
Use this alongside SKILL.md’s “Program-rule checklist (step 1 of any mission)” and “Disclosure anti-patterns (all observed in fleet wrap review)”.
The checklist preserves a program’s observed rules; the anti-pattern record warns against substituting an internal severity label for the portal’s language.
Keep the report’s technical score and vector distinct from the program’s own severity, eligibility, and reward criteria.

## Rejected
Rejected: “A high CVSS-B value is the target’s risk rating and determines the bounty tier.”
FIRST defines Base as severity and says environmental and threat context belongs to consumers; a program’s reward or severity rubric is not established by CVSS alone.

## Limits
CVSS is a severity-scoring framework, not proof that a reported behavior exists, is reachable, or is in scope.
A vector and nomenclature make the assessment legible; they do not independently validate the analyst’s metric choices.
FIRST’s official guide and specification define the framework, not a particular program’s reward policy or an organization’s complete risk decision.
This entry is documentation-only and gives no instruction to test a target.

Round-23 recheck clarification: the command checks exact quoted support in pinned
captured-source excerpts, not current online freshness or a complete entry audit.
Re-open the official documents on release/change before claiming current guidance.
