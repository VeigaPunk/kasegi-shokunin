# Candidate pinned quotes — FIRST PSIRT Services Framework v1.1 (candidate S098)

Source URL: https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1
Anchor space: `S098.candidate.txt` in this directory, captured by the lane's own
`corpus/instruments/capture-source.py --kind html` (the same instrument and the same
conversion the L1 integrator will use for the committed snapshot).
Snapshot sha256: cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2
Snapshot bytes : 170137   Lines: 1573   Fetched: 2026-11-04T19:26:42Z

Every `L<n>` anchor below is a 1-based line number in `S098.candidate.txt`. Every quote
is a verbatim substring of that line, whitespace-collapsed, and at most 25 words.

## Verification

Command actually run (from the seat directory):

```
python3 - <<'PY'
import re
C='S098.candidate.txt'
lines=open(C,encoding='utf-8').read().split('\n')
def norm(s): return re.sub(r'\s+',' ',s).strip()
for rec in open('quotes_draft.txt',encoding='utf-8'):
    qid,ln,q=rec.rstrip('\n').split('|',2); ln=int(ln)
    t=norm(lines[ln-1]); qn=norm(q)
    assert qn in t and len(qn.split())<=25, qid
print('all quotes verify')
PY
```

Result: 28 quotes checked, 0 failures (every quote a verbatim substring of its
pinned line; max quote length observed 25 words, under the <=25 cap).

## Quotes

| id | anchor | words | quote (verbatim) | why this line |
|---|---|---|---|---|
| Q01 | L219 | 24 | "The Services Frameworks are high level documents detailing possible services that computer incident response teams (CSIRTs) and product incident response teams (PSIRTs) may provide." | Title & purpose |
| Q02 | L223 | 24 | "A Product Security Incident Response Team (PSIRT) is an entity within an organization which, at its core, focuses on the identification, assessment and disposition" | Scope: what a PSIRT is |
| Q03 | L227 | 8 | "SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS" | Taxonomy spine |
| Q04 | L229 | 9 | "Service Areas regroup services related to a common aspect." | Service Area definition |
| Q05 | L231 | 25 | "A service is a set of recognizable, coherent actions towards a specific result on behalf of or for the constituency of an incident response team." | Service definition |
| Q06 | L244 | 24 | "The focus on products is the key differentiator between the PSIRT of an organization and other incident response teams represented in the same organization" | PSIRT vs CSIRT differentiator |
| Q07 | L248 | 13 | "However, three PSIRT models are used by most companies: Distributed, Centralized and Hybrid." | Organizational models |
| Q08 | L252 | 20 | "Creating policies, processes procedures and guidelines for the triage, analysis, remediation, and communication of fixes, mitigations or other advisory information" | Distributed model duties |
| Q09 | L289 | 25 | "Service Areas, Services, and Functions identify what is being done at different levels of details, while Tasks and Actions identify how it is being done" | Levels of detail |
| Q10 | L675 | 21 | "Maturity of a PSIRT may be measured via the availability and efficiency of the difference services prescribed in this service area." | Maturity measured via services |
| Q11 | L844 | 12 | "Vulnerability intake and triage comprise the case management function of a PSIRT." | Triage as case management |
| Q12 | L942 | 19 | "The delivery mechanism for a remediation should be determined based on impact of the vulnerability to stakeholders when exploited." | Remediation delivery basis |
| Q13 | L1146 | 24 | "It is important to create a transparent and collaborative environment where vendors, coordinators and finders can share information with their stakeholders and each other" | Disclosure collaboration |
| Q14 | L1510 | 16 | "how effectively an organization executes a particular capability within the mission and authorities of the organization." | Glossary: Maturity |
| Q15 | L1510 | 20 | "It is a level of proficiency attained either in actions or tasks or in an aggregate of functions or services." | Glossary: Maturity (cont.) |
| Q16 | L1573 | 15 | "Copyright © 2015—2026 by Forum of Incident Response and Security Teams, Inc. All Rights Reserved." | Copyright line |
| Q17 | L680 | 6 | "Service 2.1 Intake of Vulnerability Reporting" | Service 2.1 title |
| Q18 | L849 | 4 | "Service 3.1 Vulnerability Qualification" | Service 3.1 title |
| Q19 | L1145 | 5 | "Service Area 5 Vulnerability Disclosure" | Service Area 5 title |
| Q20 | L843 | 7 | "Service Area 3 Vulnerability Triage and Analysis" | Service Area 3 title |
| Q21 | L941 | 4 | "Service Area 4 Remediation" | Service Area 4 title |
| Q22 | L1309 | 6 | "Service Area 6 Training and Education" | Service Area 6 title |
| Q23 | L674 | 3 | "Service Area 2" | Service Area 2 title |
| Q24 | L402 | 3 | "Service Area 1" | Service Area 1 title |
| Q25 | L262 | 19 | "PSIRT Program Management Department: Creates policies, processes procedures and guidelines for the triage, analysis, remediation, and communication of fixes" | Centralized model: Program Management |
| Q26 | L844 | 23 | "While the order of operations is very similar among PSIRTs, there are variations, such as the exact point when a ‘case’ is created" | Triage variation |
| Q27 | L1195 | 4 | "Function 5.2.1 Bi-lateral Coordination" | Function 5.2.1 title |
| Q28 | L1236 | 4 | "Function 5.3.1 Release Notes" | Function 5.3.1 title |

## Anchor map by document section

| section | candidate lines | quotes |
|---|---|---|
| Purpose | 218-220 | Q01 |
| Introduction | 222-225 | Q02 |
| PSIRT Framework Structure | 227-241 | Q03, Q04, Q05, Q09 |
| PSIRT Organizational Structure | 246-277 | Q06, Q07, Q08, Q25 |
| What does the PSIRT do? | 278-287 | — |
| Definitions | 288-308 | Q09 |
| Operational Foundations (I Strategic / II Tactical / III Operational) | 309-401 | — |
| Service Area 1 (Stakeholder Ecosystem Management) | 402-673 | Q24, Q08 |
| Service Area 2 (Vulnerability Discovery) | 674-842 | Q23, Q10, Q17 |
| Service Area 3 (Vulnerability Triage and Analysis) | 843-940 | Q20, Q11, Q26, Q18 |
| Service Area 4 (Remediation) | 941-1144 | Q21, Q12 |
| Service Area 5 (Vulnerability Disclosure) | 1145-1308 | Q19, Q13, Q27, Q28 |
| Service Area 6 (Training and Education) | 1309-1497 | Q22 |
| Glossary | 1498-1548 | Q14, Q15 |
| Downloads + footer | 1550-1573 | Q16 |

