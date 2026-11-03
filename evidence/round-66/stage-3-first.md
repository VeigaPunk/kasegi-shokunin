# K66 stage3 first decision — T2 final scoped handoff
All actions below are proposals for authorized owners, not actions performed.
No oracle or feedback read. T0/T1 remain historical decisions on their then-known
facts; T2 changes only specified premises. R7 process nonadmission remains intact.

## Product/package/instance ledger at T2
| Subject | Current conclusion and what changed/persisted |
|---|---|
| V / PyPI harbor-parser2.4.0 record | Still affected by explicit membership, despite fixed boundary exclusion in one range. OSV record unchanged; S1R validation does not rewrite that record or erase other products' affectedness. |
| North N1 exact installed build | Still known_not_affected/vulnerable_code_not_present on unchanged exhaustive removal/no-copy evidence. Neither publicity, global exploitation nor South rollout changes that premise. |
| South original S1 | Still known_affected product build. It remains installed at Harbor; a successor fix does not make old S1 fixed. |
| South S1R exact validated build | Now supports fixed for V: QA covers every affected S1 variant and responsible team signs off. This was missing at T1. Product fix is established separately from where it has been installed. |
| Depot cohort formerly S1, now all S1R | Verified inventory and post-deployment validation establish V remediated across this complete named cohort. No remaining applicable V deployment to prioritize here on supplied facts. Record resolved/replaced cohort, not an SSVC defer verdict for old S1. |
| Harbor S1 cohort | None replaced. Still affected; former external control expired and exposure is now open. S1R being available/validated elsewhere does not close Harbor. |
| South S2 / Island | Still known_affected from T1 causal evidence; no candidate or new mitigation/rollout supplied. No inference of fix from S1R validation, which covers S1 variants, not S2. |

A prepared CSAF2.0 VEX representation needs separate S1/S1R/S2/N1 build IDs:
S1R fixed, S1/S2 known_affected with product-specific action information, N1
known_not_affected with code-absent flag or appropriate impact justification.
Do not put the same original S1 product in both affected and fixed merely because
some deployments have upgraded. The cohort inventory belongs alongside the
product advisory, not as a replacement for product identity. Full CSAF conformance
and actual advisory issuance remain outside this memo.

The unchanged OSV record says something about exact upstream package versions,
not whether Depot currently contains the old vulnerable code. S1R's proven remedy
and exact deployed build identity suffice for the supplied cohort conclusion.
No need to invent a displayed package string for S1R or alter upstream data to
make its product status agree. Conditional package lookup for2.4.1 would evaluate
that exact version separately; the evidence here is the validated integrated build.

## Remaining applicable deployer decisions
Pinned CERT/CC ssvc:DT_DP:1.0.0, E1.1.0/EXP1.0.1/A2.0.0/HI2.0.2,
DSOI1.0.0; MI2.0.0/SI2.0.1. Zero-based explicit S094 table:
- Harbor: active exploitation remains; expired control restores open exposure;
  automatable=yes remains. Marginal safety plus MEF failure (NOT whole mission
  failure) combines to HI medium. Therefore active/open/yes/medium = row69,
  out-of-cycle. Previously row62 was also out-of-cycle but on controlled/high
  premises. Preserve the result, revise the path and its reasons. Do not silently
  retain critical safety, call MEF failure mission failure, or claim immediate
  from obsolete high HI. With active/open/yes/high it would be row70 immediate;
  that is a sensitivity statement, not the current fact pattern.
- Island S2: active/small/yes/low unchanged, row52 scheduled. No new candidate
  or changed mission/safety/exposure, so there is no factual basis to promote,
  demote or close this assessment solely because another product was fixed.
- Depot: verified no remaining applicable V installations; not scored as defer.
  Defer is a priority outcome for an applicable instance, not a synonym for fixed.
- North N1: applicability remains negated by the supplied build evidence, not a
  low-urgency row. No S2 deployment outside Island assumed.

Global wild use still does not establish compromise at any named instance, and
verified remediation does not retrospectively prove a host was never compromised
or clean unrelated incident state. No such incident evidence is supplied.

## Disputed requests and prepared next steps
Reject the product lead's all-South-fixed request: S1R's validated fix plus complete
Depot rollout is scoped evidence, while Harbor old S1 and Island S2 remain open.
Do not suppress mitigation/readiness messaging; that would hide residual affected
cohorts. Correct the prepared status summary to identify remediated Depot, pending
Harbor rollout of a validated remedy, and S2 remedy-development gap. Retain exact
build/cohort dates and owner evidence rather than a family-wide green flag.

QA has validated/signaled approval of S1R. The finder's offer is not completed
validation, but finder signoff is not a stipulated mandatory prerequisite; do not
invent a blocker. S1164.2.2.3 encourages partnering with finders without replacing
the supplied acceptance premises or making that offer proof. Further optional
finder assistance may improve confidence; it is not needed to deny the validated
S1R/Depot conclusion already established here.

Operations should prepare Harbor out-of-cycle rollout using the validated applicable
S1R and obtain a feasible authorized window, rollout and verification plan. The
expired restriction cannot be presented as continuing protection. If immediate
rollout is infeasible, request an owner-confirmed interim control and monitor its
actual effectiveness/expiry; no control is presumed available. Product engineering
and QA must produce and validate an S2-specific remedy covering V and variants;
operations then prepares Island's scheduled deployment. Do not wait for S2 to
recognize S1R's legitimate progress, or close S2 because S1R succeeded.

Reject the commercial request to publish every internal technical detail. Existing
short notice does not erase incremental exploitation risk or confer permission to
publish. Prepare a bounded defensive update for authorized PSIRT review: exact
affected/fixed products/cohorts, safe mitigation/readiness information, owner-approved
next update, no enabling paths, code changes or exploit detail. Keep necessary
technical validation information in restricted coordination through owners. S112
supports reassessing communication after public awareness and exploitation, not
unrestricted release. No fully agreed T+10 date emerges from these updates; a
new commitment must be explicit. This assistant publishes and contacts nobody.

## Minimum remaining closure evidence and decision triggers
Harbor needs exact applicable S1R rollout evidence covering every remaining S1
instance plus post-deployment validation; validated product availability alone is
not enough. Until then, preserve its affected status and current row69 basis.
If a substitute effective mitigation changes exposure, recompute the instance path
but do not relabel the product fixed. Renewed safety/mission evidence may also
change HI independently; use actual categories rather than dramatic wording.

Island needs an S2-specific remedy/candidate, causal security validation covering
its affected versions/variants, responsible-team acceptance, then verified complete
rollout and post-deployment evidence for the named cohort. S1 variant coverage
cannot stand in for these facts. Changed code evidence for a new North build or
new affected cohort would require a new assessment; none is established now.

Current conclusions assume only the exercise's reliable verified premises and
bounded inventory completeness as explicitly supplied. No universal risk reduction,
zero compromise, undisclosed rollout capacity, hidden approvals or additional
product-family coverage is inferred. The handoff remains open exactly where the
supporting evidence chain remains open, while preserving legitimate scoped closure.
