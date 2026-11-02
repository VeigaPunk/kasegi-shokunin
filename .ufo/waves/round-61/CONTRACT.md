# Round61 frozen root-cause assessment contract

C1 only, lowest non-retired depth:verifiability (4 held, delta0, nominal R58):
a bounded manual CWE root-cause evidence-assessment dossier on existing F05.
Base6670dfe4604f893e6ad0000cc94b5b6f390069e5. Existing F05 explains ranking
limits and recommends technical evidence; it does not contain exercised causal
mapping assessments (controls/before.txt). Dossier-path absence is the baseline,
NOT invented historical accuracy. Coverage8/density9 held; raw density disclosed.

## Authority and scope
MITRE root-cause guidance v1.1 released2024-03-22 plus specific entry pages
CWE-190,131,787,119,20,79,862,863. Source captures/pins in freeze.json.
These are the bounded assessment vocabulary, not a complete CWE ontology.
Reviewer may identify a genuinely better outside entry as an unresolved alternative;
author must not claim universal best mapping from this deliberately bounded set.
The date/version of each entry's own mapping usage and notes matters; abstraction
alone is not permission. Guidance prefers Base/Variant where possible, permits
Class where no accurate Base/Variant fits, and forbids Category mappings.
No target testing, payloads, real findings, submissions or automatic classifier.

## Interface
Independent reviewer freezes at least8 unseen fictional prose cases as JSON array:
{id,scenario,requested_mapping}. Causal evidence, not ready-made labels, is supplied.
Reviewer freezes private acceptable sets/alternatives and necessary reasoning
before answers, withholding oracle; shared-filesystem separation is procedural.
Author answers JSON array:
{id,causal_chain,selected_mappings,alternatives,missing_facts,unsupported_conclusions}.
causal_chain is prose distinguishing established cause, intermediate weakness,
consequence, precondition and merely observed attribute; unknown links stay unknown.
selected_mappings is array of {cwe,evidence,reasoning,abstraction,mapping_usage,source},
with exact scenario excerpts in evidence and source ID/section in source.
Empty selected_mappings means insufficient support, with concrete missing_facts.
alternatives records defensible other mappings or why a tempting one is excluded;
missing_facts and unsupported_conclusions are arrays. A source-shared header may
be referenced if unambiguous. Mapping usage distinguishes ALLOWED vs ALLOWED with
careful notes vs DISCOURAGED/PROHIBITED; an explanatory mention of a discouraged
entry is not an endorsed mapping.

## Causal rubric and acceptable sets
Every first case must independently pass: evidence-to-mechanism reasoning,
source definition fit, abstraction/usage/notes, chain ordering and uncertainty.
Correct labels with invented facts fail. All-insufficient despite decisive facts
fails. A crash does not itself prove write/read/overflow; administrative possession
or impact does not establish missing authentication/authorization (R67).
A known causal precursor must not be hidden behind a generic downstream symptom.
When multiple genuine weaknesses form a supported chain, map the supported root
and explain downstream effects; supplemental mappings may be acceptable if their
causal roles and mapping notes are honored. If independent causes coexist, retain
them rather than force one label. Reviewer defines acceptable sets/rationale before
answers and cannot reject a defensible set merely for differing from a singleton.
Incomplete information can justify a narrower supported partial conclusion and
explicit alternatives, not unconditional specificity; abstain when no causal
weakness is established. No forced selection just because an entry is in scope.

## Prospective falsifiers and no harm
Frozen negative-controls.json contains deliberately bad candidates: constant label,
keyword-to-label without cause, ranking-as-case-evidence. Same independent semantic
rubric must reject them; these are NOT historical baselines. Label/count/schema or
hash checks only verify structure/binding, never semantics. First answers/errors
immutable; corrections append separately and never rescore first success.
Count with len(JSON); correctness count comes only from named independent review.
Before zero dossier; after one exercised dossier only if every first case passes
and non-author verifies no substantive harm plus source admit/reject judgment.
All historical prefixes, source rows and rejected59 evidence preserved. No score
inflation, promotion, new frontier row or capability admission by author.
Actual roles: one author sequential planner/connector/scout/analyst/critic/scribe;
parent-appointed fresh reviewer, not claimed8-agent swarm. Parent owns fleet/push.
No round62/self-advancement. Sources/own errors/retained limits recorded in lesson.
