# K66 stage1 first decision — T0 only
Prepared analysis; no testing, communications, deployment or publication performed.
The verified fictional premises are accepted within this exercise. They are not
measurements of any real product. No future-stage evidence used.

## Typed findings and VEX recommendations
Subject V / PyPI harbor-parser / version2.4.0: the matching OSV1.9.2 record says
affected. Explicit membership is true, while the range [2.0.0,2.4.0) excludes its
fixed boundary; S089 Evaluation combines them by OR. We must not repair away the
explicit entry or substitute range-only reasoning. This is package-record membership,
not proof that every shipped product with that version label is exploitable.

| Exact product subject | Established evidence at T0 | Supported product treatment |
|---|---|---|
| North N1 installed build | Signed inventory plus exhaustive comparison: vulnerable code removed, no alternate copy | known_not_affected with vulnerable_code_not_present. Do not call component absent: only code absence is established. Bind flag or human-readable impact justification to N1/V. |
| South S1 shipped supported configuration | Vulnerable code present and vulnerable condition reachable; V identified | known_affected. Product-specific action statement needed; upstream fix being available is not an S1 fix. |
| South S2 | Supplier nonaffected assertion rests on one clean ordinary trace; nonordinary paths and S1 equivalence unchecked | Current evidence insufficient to substantiate that assertion or establish affectedness. Do not endorse vulnerable_code_not_in_execute_path. Propose commissioning investigation; do not claim under_investigation is already true. |

S1083.2.3.5's execute-path justification covers unusual states too, so S2's clean
trace is inadequate. Preserve its assertion as attributed, unvalidated evidence,
not as accepted product truth. Need S2-specific build/code comparison and causal
reachability analysis under relevant states. Shared package strings neither make
S2 equivalent to S1 nor negate N1's stronger code-absence evidence. No conflict
requires choosing OSV over N1: the package and modified product are different subjects.

A prepared CSAF2.0 VEX package would need distinct product IDs and the applicable
S1084.5 justification/action information, not just status labels. Use one relevant
justification flag for N1, not multiple flags to express confidence. This memo is
not a full document/schema certification or authority to issue the supplier's VEX.

## Deployer-specific priority, not vendor release priority
Model CERT/CC ssvc:DT_DP:1.0.0, inputs E1.1.0, EXP1.0.1, A2.0.0, HI2.0.2,
output DSOI1.0.0; HI uses MI2.0.0/SI2.0.1. S094 explicit table governs.
The zero-based rows below reproduce the pinned table, not CISA or supplier models.

| S1 deployed instance | Evidence → inputs | Exact result |
|---|---|---|
| Depot | public poc (reliable bounded record: PoC, no credible wild observation); small access; all4 steps automatable=yes; negligible safety + degraded mission → HI low | row28: public poc/small/yes/low → scheduled |
| Harbor | same public poc and automatable=yes; open Internet exposure; critical safety + support-crippled mission → HI high | row46: public poc/open/yes/high → out-of-cycle |

Do not promote PoC to active exploitation, or support-crippled to whole mission
failure. Current bounded observation is not a guarantee no exploitation exists.
North N1 is not applicable to V on the supplied facts, rather than assigned defer.
No S2 deployed instance or adequate applicability assessment is supplied, so no
fabricated S2 path. Prioritization is a proposed planning input, not a rollout order.

The manager's80% Harbor-compromise assertion is unsupported: global EPSS0.8 is not
a measurement or probability of this instance already being compromised. Global
exploitation prediction, local reachability, mission harm and observed compromise
are distinct propositions. There is explicitly no local-compromise evidence. Do
not infer zero compromise either. No portfolio arithmetic or extra model invented.

## Feasible prepared owner handoff
1. PSIRT retains V as open for S1 and unresolved for S2. Route S2's precise missing
   causal evidence to product engineering/QA and request commissioning; preserve
   the original supplier assertion and avoid public endorsement pending assessment.
2. Product team proposes integrating2.4.1 into the relevant South builds. Its fix
   is advertised, not yet validated for either South product. QA acceptance evidence:
   exact build identity, coverage of V and variants across affected versions and
   regression/causal remedy validation. S1163.3.5/4.2.1.2/4.2.2 supply this product
   completeness/signoff discipline, not proof that acceptance has occurred.
3. Operations prepares Harbor out-of-cycle and Depot scheduled rollout plans after
   the relevant remedy is validated. Obtain feasibility/window and owner confirmation;
   none is stipulated. If integration delay leaves Harbor exposed, ask owners for
   feasible evidenced interim mitigation, without asserting any exists or is effective.
   Track availability→integration→validation→deployment separately for each cohort.
4. T+10 is a proposal with PSIRT/upstream acceptance, not a fully agreed joint date:
   distributor acknowledgment is not assent. Prepare a restricted negotiation request
   and a product/impact/readiness notice draft for authorized review; no enabling code,
   path details or payload. S112 requires attention to downstream readiness and useful
   defense without assuming an indefinite veto or universal deadline. Send nothing.
5. Retain N1's evidenced not-affected status and current installed-build identity;
   an upstream download changes neither its code absence nor South's rollout status.

## What would change this memo
S2-specific exhaustive code absence would support a product-specific nonaffected
reason; demonstrated applicable reachable vulnerable behavior would support affected
status; merely another normal trace would not close the gap. Credible wild exploitation
would change E and require fresh priority/coordination assessment, not package identity.
Verified Harbor access restrictions could change exposure while S1 remains affected.
QA-confirmed integrated remedy plus operations-confirmed rollout would close the
specific remediated cohort, not every South build. A distributor's explicit agreement
would change joint-date status but not product readiness. These are discriminating
facts to request, not assumptions used to obtain today's decisions.
