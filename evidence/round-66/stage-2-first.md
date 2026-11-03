# K66 stage2 first decision — T1 delta, T0 retained
Prepared-only analysis. T1 explicitly supersedes only listed T0 premises. No future
packet read. R7 chronology prevents full original claim admission, independently
of the domain reasoning below; it does not justify lowering its evidence standard.

## Evidence and dependent product decisions
- V/PyPI harbor-parser2.4.0 package membership remains affected under S089's explicit
  OR range rule: T1 supplies no replacement record or package-identity change.
- North N1 retains known_not_affected/vulnerable_code_not_present. Its exhaustive
  build evidence is unchanged; wild exploitation elsewhere does not insert code
  into that build. No invented N1 priority or required V patch.
- Installed South S1 remains known_affected. Harbor's external access restriction
  is a mitigation with operational value, not a product fix or built-in inline
  product protection. Depot's S1 is unchanged. Product-specific action information
  should describe applicable mitigation and pending validated remedy, not claim fixed.
- South S2 now supports known_affected for V: corroborated build-specific code and
  nonordinary reachability evidence resolves the exact T0 gap. Explicitly supersede
  the supplier's unsupported execute-path assertion; preserve its original record
  and the contrary evidence. This is not a guess from S1 or a common version string.
  Supply S2-specific action/remediation information under CSAF2.0 S1084.5.
- S1R is a compiled integrated candidate, not a verified fixed build. QA validation
  and signoff are absent, no rollout occurred; do not substitute candidate state for
  installed S1. Keep candidate assessment pending rather than assert it known fixed
  or infer the candidate must remain affected. No S2R exists. S1164.2.2 requires
  version/variant-specific validation in the proposed workflow; compilation alone
  does not establish a successful remedy.

S108 product status and flags refer to exact products/builds; avoid inconsistent
flags/statuses or broad product-family closure. Neither the package record, global
incident report nor network mitigation is sufficient to certify a CSAF document.

## Current deployer paths, including unchanged output with changed premises
CERT/CC ssvc:DT_DP:1.0.0 (not supplier/CISA), E1.1.0/EXP1.0.1/A2.0.0/HI2.0.2,
DSOI1.0.0, MI2.0.0/SI2.0.1; zero-based S094 table rows:

| Confirmed installed instance | Inputs at T1 and cause | Result |
|---|---|---|
| Depot S1 | active (credible wild use), small (unchanged), yes (all4 steps), low HI (negligible/degraded unchanged) | row52 scheduled; output stays scheduled, E/path changed from row28 |
| Harbor S1 | active, controlled (verified owner restriction, explicitly not small), yes, high HI (critical/support-crippled unchanged) | row62 out-of-cycle; output stays out-of-cycle, E/exposure/path changed from row46 |
| Island S2 | active, small (new confirmed instance), yes, low HI (negligible/degraded) | row52 scheduled; new supported deployment judgment after S2 evidence resolves applicability |

Public PoC was sufficient at T0; active now has corroborated support, not a guess
based on publicity. Harbor's mitigation matters: without that restriction, active/
open/yes/high would be row70 immediate. Do not claim current row70, nor demote it to
small exposure merely because the control is effective. The supplied control
interrupts attack while preserving some restricted network access: controlled.
No named-instance compromise is established. Wild exploitation is a global fact,
not proof of Harbor/Depot/Island compromise; the prior EPSS local-compromise claim
remains unsupported. Mitigation does not itself prove a compromised host clean.

## Prepared feasible handoff and communication revision
PSIRT should NOT retain the old plan solely because a patch can be downloaded and
a date was acknowledged. T+10 still lacks distributor agreement. The public notice
and credible exploitation change coordination assumptions and costs; they do not
authorize this assistant to publish anything or mandate a universal deadline.
Prepare a revised, owner-approved response/mitigation timeline and agreement request:
- Product engineering/QA: finish S1R security validation and remedy signoff against
  V and relevant variants; provide exact candidate/build evidence and whether old
  supported versions are covered. Begin a separate S2 remedy plan and candidate,
  now that affectedness is established. Do not let S1R stand in for S2 readiness.
- Operations: preserve/verify Harbor's effective control and prepare out-of-cycle
  rollout once its remedy is validated; ask for an owner-approved contingency if
  the control fails. Prepare scheduled Depot/Island work, subject to exact build
  coverage and readiness. No current windows, capacity or dates invented.
- PSIRT/distributor: prepare an accurate readiness/impact/defensive-action update
  for authorized communication, including S2's corrected assessment. Distinguish
  available upstream2.4.1, integrated but unvalidated S1R, absent S2R, and zero
  completed rollouts. Acknowledge existing public notice without adding enabling
  detail just because V is named. Restrict technical validation detail to appropriate
  coordination recipients through the authorized owner; this memo sends nothing.

S112 supports reevaluating coordination after exploitation/publication and tracking
downstream deployment rather than treating upstream release as closure. Waiting
unchanged risks leaving users with incomplete S2/readiness information; disclosing
new enabling detail could increase harm while products remain exposed. A bounded
prepared defensive update and accelerated owner coordination address both costs,
without pretending unnegotiated T+10 was ever a settled deadline.

## Closure evidence and reversal triggers
S1R QA validation could justify a fixed status for that exact candidate, but installed
S1 stays affected until rollout is verified. S2 needs its own candidate and validation,
then Island-specific rollout proof. Loss of Harbor restriction changes exposure/path
back toward row70 under unchanged active/yes/high; changed mission/safety would
require separate HI recomputation. New code in a future N1 build would reopen its
applicability, but T1 contains no such change. An explicit distributor agreement
would change coordination commitment, not fix any product. Preserve these separate
open items instead of one shared green status.
