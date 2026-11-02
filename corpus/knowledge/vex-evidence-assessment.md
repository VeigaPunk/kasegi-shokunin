# CSAF2.0 VEX evidence assessment: justify the product, not the dependency alert
source: S108 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.md — OASIS Standard2022-11-18 sections3.2.3.5,3.2.3.9,3.2.3.12.1,4.5,6.1.33; capture corpus/source-snapshots/round-62/S108.txt
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-62/manifest.json --source S108 # pinned captured bytes only; absent/corrupt source fails; not upstream freshness

## Scope and evidence discipline
This deepens F21, not a new VEX format or scanner. The standard defines an assertion
about a particular product and vulnerability; the analyst must establish its factual
basis separately. A source-valid token is not proof of the fictional scenario.
Use only supplied harmless evidence; no real-target probing or scanner suppression.
Source claim anchor: S108 section4.5 line3034, “state that and why a certain product
is, or is not, affected by a vulnerability”. Treat the assessment below as a
bounded manual workflow, not certification of complete CSAF documents or real products.

## Decision table

| Established evidence about the exact product/vulnerability | Supported direction | Shortcut to reject |
|---|---|---|
| Vulnerable component absent from the shipped product | known_not_affected, component_not_present | Build-time dependency proves shipped inclusion |
| Component present, but defect-bearing code absent | known_not_affected, vulnerable_code_not_present | Component absent merely because one function was removed |
| Code exists but cannot execute, including unusual states | known_not_affected, vulnerable_code_not_in_execute_path | A clean test trace exhausts all paths |
| Code executes but use prevents adversarial control needed for any anticipated attack | known_not_affected, vulnerable_code_cannot_be_controlled_by_adversary | Authentication or trusted-input label proves no control |
| Built-in inline protection prevents exploiting the flaw | known_not_affected, inline_mitigations_already_exist | Optional external protection is built-in |
| Product has a verified fix | fixed for that product build | Unchanged upstream version string proves patch absent |
| Product vulnerability established with risk-reducing external control | known_affected plus product-specific action information | Mitigation necessarily resolves the vulnerability |
| Applicability/causal premise unknown | Insufficient judgment; under_investigation only with an investigation or as explicit workflow proposal | No observed exploitation proves no impact |

Source anchors for the five distinctions: S108 section3.2.3.5 lines2461–2467:
“component is not in the product” (2461); “code underlying the vulnerability is not
present” (2462); “an attacker cannot mount any anticipated attack” (2464);
“including non-anticipated states of the product” (2465); “Built-in inline controls
or mitigations prevent an adversary” (2467). These are distinct reasons, not a
ranking of confidence. Exclude unsupported alternatives, but record plausible
alternatives conditionally rather than pretend one label is uniquely mandatory.

S108 section3.2.3.9 line2652 says fixed versions “contain a fix for the vulnerability”;
line2667 says investigation means “it is not known yet whether these versions are or
are not affected”. Reason from verified build identity, not a generic product family.
A prior-version assessment or one configuration cannot automatically cover another.
An external mitigation can matter operationally without becoming a product fix:
section3.2.3.12.1 line2744 says mitigation “does not resolve the vulnerability on the
affected product”. Neither the proposed status nor this fictional analysis grants
authority to test a deployment or publish a vendor advisory.

## Package obligations and collisions
For known_not_affected, provide the product-specific machine-readable flag OR
human-readable impact justification; the latter uses threats category impact and
explains why exploitation is not possible. For known_affected, provide product-specific
remediations action information; lack of a fix does not erase affectedness.
Anchors: S1084.5 lines3053–3055, “an impact statement SHALL exist”, “as an action
statement”, and “no_fix_planned”/“none_available”. These requirements are necessary,
not a complete validation recipe.

Only one VEX justification flag per product within a vulnerability item, including
group-derived membership: S1086.1.33 line4576, “not member of more than one Flag
item with a VEX justification code”. Competing valid explanations can be discussed
in prose; do not emit multiple conflicting/duplicate flag memberships to express
uncertainty. The frozen contract's draft once allowed flag(s); this is corrected
before freeze and the draft retained. Do not borrow OpenVEX not_affected or
justification fields as CSAF product_status/flags: S109 is excluded for that use.

## Checklist and falsifiable exercise
1. Bind product version/build/configuration, vulnerability and evidence date.
2. Separate component inclusion, code inclusion, reachability, adversary control,
   and protection. List precisely what establishes each needed premise.
3. Give exact scenario excerpts and source anchors; disclose missing facts.
4. Select status and at most one flag; keep alternatives conditional.
5. Explain product-specific impact/action obligations and unsupported conclusions.
6. Compare against independent causal review under .ufo/waves/round-62/CONTRACT.md.

A case with only ordinary-path tests falsifies an unconditional unreachability
answer. A component-present/code-absent case falsifies the component-absent answer.
The three prospective bad policies are in .ufo/waves/round-62/negative-controls.json;
manual semantic review, not word-count or label-matching, judges their rejection.
First answers, when landed, remain immutable; post-review learning cannot rescue a
failed first-answer condition. Chousa owns research method; kagi owns secrets;
kasegi owns this security claim-evidence judgment only.
