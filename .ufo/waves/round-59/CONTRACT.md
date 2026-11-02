# Round 59 frozen assessment contract

C1 only: depth:verifiability, lowest non-retired axis. Bounded capability acquisition:
a source-grounded CVSS v4 partial assessment dossier, judged by a parent-appointed
non-author. Legacy citation-availability score stays 4 (nominal per R58); coverage
8 and density 9 stay held. No automatic classifier, full vector, numeric severity,
bounty eligibility, real exploit verification or promotion is claimed.

## Actual before
Base f17171eac43ce5df67870ef038dbe92273a3a5f3. controls/before.txt opens the actual
F01 entry: it teaches nomenclature and explicitly warns that vectors do not
validate metric choices. The bounded search over SKILL and CVSS knowledge found
no PR/UI/subsequent-impact assessment procedure. This is missing documented
repertoire, NOT a measured poor score by an earlier analyst or executable.
Source specification document v1.2 was reopened before this freeze. No unseen
reviewer scenario or expected answer has been received at freeze time.

## Interface
Reviewer delivers a JSON array of objects with id (unique string), scenario
(nonempty prose), questions (subset of PR, UI, SC, SI, SA). Cases are fictional,
contain no ready-made metric answers, and require no execution or live testing.
Author returns JSON array with matching ids and assessments mapping every asked
metric to {value, evidence, reasoning, missing}; value is N/L/H for PR and
SC/SI/SA, N/P/A for UI, or literal insufficient. evidence is an array of exact
scenario fragments; missing is an array of concrete unanswered questions, empty
for determinate judgments. Each answer also includes system_boundary (prose)
and unsupported_conclusions (array). Source anchors belong in reasoning.
Insufficient is an assessment-workflow state, NOT a CVSS vector value X.

## Frozen substantive rubric
FIRST specification Base Metrics: PR/Table4, UI/Table5, Impact Metrics/system of
interest, Tables7/9/11 govern. PR concerns prerequisite authority, not the
privileges gained; self-service provisioning and nonunique default credentials
must be considered rather than treating all logins as L. Victim authority is
not attacker prerequisite authority. UI asks about another human's required
participation; ordinary involuntary rendering differs from a conscious special
import or overriding protections. Attacker-only actions are not UI.
Impact requires a supported additional negative outcome; preexisting access is
not counted as newly lost confidentiality. Boundary follows coherent function
and policies; an exclusive supporting component can belong to the same system.
Different owner/process/host is not alone proof of subsequent impact. Each
subsequent CIA dimension is justified separately. Limited loss can still be H
where the source's direct-serious-consequence alternative applies. Missing facts
are not N, and missing unrelated facts do not erase a supported metric. Do not
invent exploit chains, service interruption, write capability or reward.

## Success, failure and measurement
The independent judge freezes scenarios and expected reasoning before reading
author answers; share only cases, never the oracle. At least 8 unseen scenarios
must jointly exercise PR timing, UI distinctions, boundary, impact extent and
insufficient facts. Every asked metric must receive correct value AND a causal
scenario/source rationale; label-only, copied labels, generic rubric, or guessed
facts fail. Judge evaluates boundary and unsupported conclusions too. All first
answers and disagreements remain immutable; fixes are separate artifacts, never
rescored as first-pass success. C1 acceptance requires every independent case to
pass or the claim is reported unverified under this frozen contract. Counting
command is a count of the independent judge's case verdicts, not an author
syntax validator. Results measure these cases only, not general accuracy.
Before count: zero documented dossiers at the named new path; absence is not
zero expertise. After count: one exercised dossier only if independently judged.
A copied-label answer, always-insufficient answer and unsupported post-exploit
PR:H interpretation are negative controls to be judged under the same rubric.
No author-created program will claim to grade natural-language reasoning.

## No harm and scope
Append existing SKILL/index/ledgers, preserve old sources. Show raw density
before/after, do not pad citations. Existing legacy host-bound failures stay
reported. Independent admit/reject source curation and substantive no-harm
review remain necessary. Same FIRST page is admitted for metric definitions
and rejected as proof that any invented scenario is a real vulnerability or
bounty-worthy. No second source is needed merely to inflate curation counts.
One author performs sequential specialist roles under approved adaptation;
independent reviewer appointed by parent. Public push held, private work only.
