# CVSS v4 evidence assessment, not vector transcription
source: S092 — https://www.first.org/cvss/v4.0/specification-document — document v1.2, PR/UI, Impact Metrics, Tables 7/9/11
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092

## Decision procedure
Treat a scenario as assumed training evidence, not proof of a real finding. Record
what the attacker could do before, what changes after, and whose actions enable it.
For PR, distinguish required prior authority from resulting privilege gain. Do not
translate every login into L: examine self-service and nonunique-default credentials.
For UI, distinguish attacker actions, ordinary victim participation, and deliberate
special actions or protection overrides. Explain why the action is necessary.

Draw the functional/policy boundary before assigning subsequent impact; an exclusive
support component may be part of the vulnerable system. Name additional loss in each
CIA dimension separately. N needs supported absence, not silence. H need not mean
all data: limited loss with direct serious consequence can qualify. If evidence cannot
discriminate values, answer insufficient and name the missing fact; this is not a CVSS
vector value. Do not abstain on established metrics because another metric is unknown.

## Located source support
All quotes together are 20 words: PR line478 “privileges an attacker must possess prior”; UI line502 “other than the attacker”;
boundary line548 “coherent function”; impact line527 “Only an increase in access”;
SC Table7 line589 “direct, serious impact”. The manifest pins exact capture bytes/anchors.

## Rejected inference and limits
An attacker ends with administrator control: PR:H does not follow. A second host or
company is named: subsequent impact does not follow. A complete-looking partial vector
does not establish full score, reward, authorization or actual exploitability. Source
recheck verifies captured wording, not current online freshness or analyst correctness.

Assessment workflow: `.ufo/waves/round-59/CONTRACT.md`. Independent scenarios and first
answers will remain in that wave's dossier; a human independent judge must evaluate
causal reasons, not merely compare enums. This documentation-only exercise deepens F01;
no target testing, scanner, automatic natural-language classifier or total CVSS calculator.

## Round-59 independent-review refinement
PR requires evidence of necessity, not just prior possession. K59-10 states an
attacker has ordinary account rights; it does not say exploitation needs them.
The first PR:L answer is unsupported. Correction01 reports insufficient and asks
whether that authority is necessary; only if confirmed does L follow. This is an
actual failed inference, preserved in the dossier, not a fabricated bad baseline.
