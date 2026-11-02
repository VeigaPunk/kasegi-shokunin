# CERT/CC deployer priority: evidence before table lookup
source: S094, S095, S096 — official CERT/CC documentation, captures corpus/source-snapshots/round-60/; model S094 line514, table line880 onward; MI S095 line201; SI S096 line205
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S094 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S095 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S096

## One model, not generic SSVC

This deepens F20's explicitly unheld deployer paths. Model identity is
“ssvc:DT_DP:1.0.0” (S094:514); the decision is “priority of deploying a patch”
(S094:216). Use E1.1.0, EXP1.0.1, A2.0.0, HI2.0.2 and DSOI1.0.0, not a
single global SSVC version. Model/schema/input versions are different things.
The unit is remediation/mitigation paired with a deployed product instance.
Supplier development priority, CERT/CC coordination and CISA-specific models
answer other decisions. Matching outcome spelling does not establish identity.
The source calls this an example: selecting it is not declaring universal policy.

## Interpret evidence, then traverse

| Evidence question | Bound decision discipline |
|---|---|
| What exploitation evidence exists? | Public PoC is not active exploitation; require credible observed wild-use evidence for active. Mere omission is not none. |
| How can the adversary reach this deployed system? | Small, controlled and open describe actual access. A firewall name alone establishes no effective restriction. |
| Can the whole initial attack chain be reliably automated? | All four stages matter: reconnaissance, weaponization, delivery, exploitation. One automated step proves neither yes nor no. |
| Whose mission and safety are affected? | Bind to this deployer and deployed instance, not technical severity or another organization's mission. |
| Which table row follows? | Preserve input facts and zero-based row, not just a priority label. Unknowns retain every compatible row. |

Human Impact is the S094 combination of safety and mission, not a synonym for
technical impact. “ssvc:MI:2.0.0” (S095:201) distinguishes support crippled,
where “essential functions continue for a time” (S095:211), from a failed MEF
and whole mission failure. “ssvc:SI:2.0.1” (S096:205) includes physical,
operator/system resilience, environmental, financial and psychological harms;
catastrophic includes “Multiple loss of life” (S096:221), not any financial loss.
Use the actual category definitions rather than emotional severity adjectives.

HI composition: negligible/marginal safety with degraded/support-crippled mission
is low; those safety levels with MEF failure are medium. Critical safety with
degraded mission is medium, with support-crippled/MEF failure high. Catastrophic
safety OR mission failure is very high. These are the source's combinations;
an unsupported limb does not become true because the resulting label feels right.

## Counterfactual context matters

Holding exploitation active and automation yes, a small-exposure/low-HI instance
maps row52 scheduled while open/high-HI maps row70 immediate. Technical severity
need not change. These exact rows can be re-read in the pinned table; they are
not live remediation orders. Defer is a current priority, not proof of safety.

Missing information is an assessment state, not an extra SSVC input token.
With active/open/yes and unknown HI, rows68–71 yield out-of-cycle OR immediate:
no single evidence-supported priority. With none/small/no and unknown HI,
rows0–3 yield defer OR scheduled. Conversely a missing input whose compatible
rows all agree need not prevent that common priority; retain the unknown input
and explain the row-set reasoning, rather than invent a precise value.
The official component pages suggest defaults (MI support crippled; SI marginal)
on total ignorance. This evidence-only dossier does not silently use them.
A user of those suggestions must label them assumptions and assess sensitivity;
source suggestion does not turn an assumption into observed fact.

## Discrepancy is evidence too

S094:510's summary says none+very-high leads out-of-cycle, but Table of Values
rows3/7/11/15/19 are scheduled and only row23 is out-of-cycle. This dossier pins
and follows the explicit DT_DP1.0.0 table, discloses conflict and does not claim
all official prose agrees. Future source change requires a new pin and review.
The derived readable table in controls/source-table.txt is a convenience export,
not a separately authoritative or implemented reasoning engine.

## Falsifiable review and limits

Reject constant priority across divergent row52/70 contexts; reject a correct
row70 result called CISA; reject low HI inferred solely from omitted harm. These
prospective errors live in `.ufo/waves/round-60/negative-controls.json` and the
independent reviewer applies the same causal rubric as for first answers.
Rejected source use S097: this deployer table cannot establish supplier/CISA
priority, universal risk, bounty eligibility or truth of invented circumstances.
No target testing, contact, deployment, exploit, scoring engine or action authority
is supplied. This is source-grounded fictional assessment, not empirical accuracy
on real deployments. First-pass review and any correction stay distinct.
