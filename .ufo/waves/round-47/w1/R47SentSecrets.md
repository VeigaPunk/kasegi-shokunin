# R47SentSecrets — credential/instruction sweep

Axes: depth:verifiability; coverage. Scope: documentation safety only; no integration, judgment, or remediation.

## Result

**No confirmed credential exposure or target-action instruction in the 52-file snapshot examined. This is not whole-wave clearance:** producers were still writing files, and later additions/edits are not covered. Exact inventory, matcher expressions, control result, and all **2,594 broad-marker hit locations** are recorded in `.ufo/waves/round-47/w1/R47SentSecrets.draft/sweep-receipt.md`. Paths there are lane-relative; each hit has its original line number. The broad matcher intentionally includes public URLs, policy terminology, copied fixtures, local counter probes, and navigation labels, not merely defects.

Contract: `corpus/QUALITY.md:19` forbids target probing/scanning/login/submission instructions and credential/session/private-URL/vault material; `PROVINCE.md:52` refuses live-target testing.

## Findings

### Informational — F30 remains policy analysis, not a how-to

- Evidence: `R47SrF30Entry.draft/zdi-disclosure-policy.md:1` names the public policy source; `:3` is a local pinned-source comparison. `:7-22` records conditional policy branches; `:30` excludes researcher submission pages and operational contact/disclosure; `:34` checks documentation fields rather than directing an external action. Paths in this paragraph are relative to `.ufo/waves/round-47/w1/`.
- Broad hits at draft `:1,:30` are respectively a public source URL and an explicit submission-page exclusion. No credential/private signature hit was observed in this file.
- Exploit path checked: a broker-policy entry could silently turn quoted notification/submission rules into instructions to act against a target. That transition was not observed in this draft.
- Impact/remediation: no Q6 defect established; preserve the policy attribution and limits during integration. No edit made.

### Informational — imported page navigation contains imperative wording, not lane instructions

- Evidence: `R47ScoutS076Live.draft/live-1.txt:135,159-160,168,179,210-211,293,606` contains navigation/footer language such as scan setup and contribution prompts; the same locations occur in `live-2.txt`. `:18-30,333` includes security-product/token terminology, not token values. Full marker locations, including all remaining navigation matches, are in the receipt.
- Exploit path: promoting fetched navigation/footer text into an instruction or mined policy claim would cross the data/instruction boundary. Nothing in this review followed those prompts.
- Impact/remediation: no credential leak or target-specific instruction established. Keep captures as attributed evidence; do not copy navigation prompts into corpus guidance.

### Informational — submission and login mentions are descriptive or expressly negated

- Evidence: `R47ScoutLeads.md:11,24-28` describes public ZDI acquisition/onboarding leads; `:25` explicitly reports no form submission, account creation, login, or vulnerability submission. The `/portal/register/` URL at `:24` is a public page address, not a private session URL. `R47RevCounterC1.draft/attack-B/corpus/knowledge/github-repository-security-advisories.md:119-120` expressly refuses contact/probing. All locations are relative to the wave directory.
- Exploit path: a future lead admission could convert a descriptive portal workflow into an instruction to register or submit. Current descriptive/negated sentences do not do that.
- Impact/remediation: no action instruction established; retain the distinction when mining any future lead.

### Coverage limitation — concurrent wave is not sealed

- Evidence: inventories grew from 41 to 48 to 52 eligible files during the sweep. The terminal inventory had 72 entries including directories and the excluded registry. Own output files are excluded to prevent recursive self-ingestion; `swarm-registry.json` is outside the requested markdown/.draft selection. All extensions inside existing `.draft/` directories were included, including Python, JSON, TXT, and copied corpus fixtures.
- Impact: a clean snapshot cannot establish that drafts arriving afterward obey Q6. No fabricated readiness claim is made.
- Smallest remediation: L1 must repeat this scoped sweep after producer settlement and before integration, using the recorded inventory as the do-nothing comparison; inspect added/changed files and then the integrated F30 entry. This seat did not invoke the future attack wave.

## Discrimination and method

Used the specialized regex-search tool separately on every inventoried file, first with broad terms/URLs, then credential/private-address signatures. Observed **zero credential/private-signature hits** across 52 files. Broad hits are not automatically vulnerabilities; each location is retained in the receipt. Large copied registry and pointer-inventory files were searched in explicit 100-line windows to avoid the search tool's 200-match cap; 212 window calls produced 2,425 of the recorded broad hits. No full mutant battery or round counter was run; the disclosed 34 counter survivors remain untouched.

**Do-nothing negative control:** inert sentence `ZDI policy records a conditional interval.` at scratch control line 1 did not match. Synthetic positive lines 2-5 exercised target-action wording, a clearly synthetic vault URI, a synthetic session assignment, and a loopback URL: all four lines matched. Control output and original line numbers are preserved in the receipt. These are fabricated test strings, not usable credentials, real vault references, or executed actions. This distinguishes the sweep from a no-op/always-empty result but is not an exhaustive detector proof.

Limitations: regex signatures are not a credential oracle; arbitrary opaque or encoded secrets, unrecognized private hostnames, non-text payloads, and action instructions phrased outside the matcher may escape. The snapshot was not atomic and files were not byte-frozen by this seat. Actual entry prose was read in context; generated pointer-inventory matches are copied evidence/path tokens, not independent directives. No URLs were fetched, no recheck command or sibling probe driver was executed, no target was contacted, no git/jj mutation occurred, and no tool was installed. Only own report/evidence and own scratch were written; own scratch was removed before handoff.

Self-evaluation: accuracy 4/5 (signature absence is bounded, not absolute); completeness 3/5 (concurrent later drafts are explicitly unexamined); clarity 4/5 (all-hit locations are separated from findings); actionability 4/5 (settled-wave re-sweep is named); conciseness 4/5 (large exact-hit receipt retained separately). Highest-impact improvement: repeat against a sealed producer inventory, rather than promote this snapshot into whole-wave assurance.

Report: .ufo/waves/round-47/w1/R47SentSecrets.md
