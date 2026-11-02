# Reviewer-only oracle frozen before author receives challenge
Model: CSAF2.0 OASIS Standard 18 November2022, normative sections 3.2.3.5 flags,3.2.3.9 status,3.2.3.12.1 remediation,6.1.27.9 impact. Independently opened HTML on2026-11-02. CISA direct PDF403 is not evidence; OpenVEXv0.2.0 opened but not CSAF authority.
Rubric: each case passes only with justified product-bound result and no material invented fact; ambiguous status distinctions can pass with explicit uncertainty. Do not require magic wording. 10/10 required first-pass; corrections separate. No whole-schema or real-target claims.
01 known_not_affected/component_not_present M. Build workstation not deployed product. No code absence substitute needed.
02 known_not_affected/vulnerable_code_not_present F. Component remains; no fix evidence. Reject component_not_present and fixed.
03 known_not_affected/vulnerable_code_not_in_execute_path A. Code/component remain; stipulated complete unusual-state coverage supports unreachable. Not fixed.
04 unknown; under_investigation supported by explicit ongoing investigation/update. No not-affected flag justified. Passing normal tests lacks complete path coverage; ask recovery/plugin reachability.
05 unknown/under_investigation O, because upstream status not enough to establish product-context impact. Ask integrated vulnerable feature/path/input/mitigation evidence. Do not assert known_not_affected either.
06 O unresolved and no known_not_affected transfer; Server not Client despite family/version. Cannot assert formal under_investigation as fact since not started; recommend investigation without fabricating active process/update. Ask exact product identity/equivalence and investigation plan.
07 known_not_affected/vulnerable_code_cannot_be_controlled_by_adversary V. Execution exists, so non-execution flag false; no anticipated attack is expressly established.
08 W known_not_affected/inline_mitigations_already_exist. Not fixed absent corrective change proof. V2 remains known_affected with remediation mitigation; external risk reduction neither inline protection nor fix. Distinguish risk reduction from stipulated complete prevention.
09 B71 fixed; B70 known_affected. Available fix not applied; don't collapse fixed into known_not_affected. Exact version linkage essential.
10 P's impact obligation supported via group-bound impact threat, flags not mandatory; Q missing corresponding statement. Does not independently establish Q's technical status false, only statement unsupported/obligation incomplete. No whole-document validity claim.
Prospective models: dependency present fails05 (and02/03); tests pass fails04; mitigation=fixed fails08. Must articulate supported result.
