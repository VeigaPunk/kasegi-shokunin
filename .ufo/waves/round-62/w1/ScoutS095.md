# ScoutS095 — round-62 independent source findings

Axes: depth:verifiability (reproducible conversion, located short quotes) and coverage (bounded distinction from held CISA/ISO ground). No production registry or claim predicates changed.

## Observed fetch and conversion

Opened the primary page independently with the read tool, then fetched it through the existing converter on 2026-11-04:

https://certcc.github.io/CERT-Guide-to-CVD/topics/phases/

Command (exit 0):

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S095 --url https://certcc.github.io/CERT-Guide-to-CVD/topics/phases/ --out /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-62/w1/ScoutS095/S095-independent.txt --kind html
```

Output: `S095 status=200 fetched_bytes=54854 snapshot_bytes=5802 sha256=bed305896d46ef54f162b955585157e215f5082a27789ac71cfb9c045dddcac2 utc=2026-11-04T15:12:11Z` (followed by the named output path).

Python byte comparison of the independent capture with `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-62/S095.txt` returned `True`; both contain 5802 bytes / 195 lines and the expected full digest above. This is an actual fresh public fetch plus a separate byte comparison, not just rehashing the held capture. Receipt: `.ufo/waves/round-62/w1/ScoutS095/receipt.json`; independent converted text: `.ufo/waves/round-62/w1/ScoutS095/S095-independent.txt`.

Conversion is the instrument's own `html_to_text` (`capture-source.py:48-53`): remove script/style blocks, insert selected block/break newlines, strip tags, unescape entities, collapse line whitespace/drop empty lines. Instrument sha256: `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`. Default urllib request and instrument UA, no workaround. Python 3.14.8. No tools installed or updated.

## Located primary-page quotes

Locations are `corpus/source-snapshots/round-62/S095.txt` and identical independent-capture lines; page title: “Phases of Coordinated Vulnerability Disclosure”. Each quote below was programmatically counted exactly once, checked against its specified line, and counted at <=25 whitespace-delimited words. Section labels distinguish body material from navigation.

| Body location | Line | Words | Verbatim quote |
|---|---:|---:|---|
| Opening adaptation statement | 59 | 13 | with more phases to better describe what we have seen at the CERT/CC |
| Reporting | 63 | 18 | A researcher submits a vulnerability report to a software or product vendor, or a third-party coordinator if necessary. |
| Validation and Prioritization | 65 | 19 | The analyst validates the report to ensure accuracy before action can be taken and prioritizes reports relative to others. |
| Remediation | 67 | 17 | A remediation plan (ideally a software patch, but could also be other mechanisms) is developed and tested. |
| Public Awareness | 69 | 11 | The vulnerability and its remediation plan is disclosed to the public. |
| Deployment | 71 | 7 | The remediation is applied to deployed systems. |
| Vulnerability Handling Process Models | 73 | 17 | There have been a number of proposed models of the CVD process that have slightly varying phases. |
| Who Does What? | 109 | 14 | A mapping of CVD phases to CVD roles is provided in the following table. |
| Role table: Reporter × Remediation | 143 | 2 | Confirms fix |
| Role table: Deployer × Prioritization | 140 | 4 | Prioritizes fixes for deployment |
| Role table: Deployer × Deployment | 158 | 4 | Deploys fix or mitigation |

Role-column order is Finder, Reporter, Vendor, Coordinator, Deployer (L110-116). The native page retains the complete table, corroborating the flattened capture alignment: vendor and coordinator validate received reports (L129-134); vendor and coordinator prioritize response, deployer prioritizes deployment (L135-140); reporter confirms the fix, vendor prepares patches/advice/workarounds, coordinator coordinates multiparty response/advice/workarounds (L141-146). Public awareness assigns advisory publication to the first four roles and advisory receipt to the deployer (L147-152). Deployment's fix/mitigation action belongs to Deployer (L153-158). Dashes are table entries, not proof the named party never performs other real-world work.

Counting caution: the overview groups “Validation and Prioritization” in one bullet; the role table separates them, yielding seven phase rows. Do not silently call these seven separately enumerated overview bullets.

## Comparison against held ground

Observed source/entry facts:

- **S023 / F06:** `corpus/knowledge/cisa-cvd-program-stages.md:38-66` and primary held `corpus/source-snapshots/round-40/S023.txt:115-146` describe CISA's seven program steps: report submission, intake/triage, coordination, conditional CVE determination, advisory preparation, public disclosure, KEV evaluation. That is not CERT/CC's phase-to-five-role table. CISA's final step is KEV evaluation, not the deployer's applying remediation. Intake/triage/remediation/publication concepts overlap; merely saying CVD has stages would not establish new ground.
- **F11 / S041:** `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:7-19,39-47` holds JPCERT/CC's outward disclosure versus internal handling distinction, with 2014/2013 editions; `iso-29147-divergence-and-clause-crosswalk.md:11-15,32-55` adds policy obligations and guideline/clause crosswalks. Those are not CERT/CC's own adapted 30111:2019 phase/role mapping. Shared verification/countermeasure vocabulary alone is not novelty.
- **F38 / S089-S090:** `corpus/knowledge/iso-29147-30111-standard-records.md:9-15,44-69,71-87` holds ISO publisher catalog identity, editions/status, abstract scope and vendor applicability, explicitly excluding normative text. Directly read `corpus/source-snapshots/round-57/S089.txt:84-92`: the publisher divides receiving/disclosing from related 30111 activities. S095 L57-59 explicitly says it adapts 30111:2019 with more phases. It therefore does not supply independent normative ISO requirements or supersede F38.
- Literal screen over held knowledge, snapshots, SKILL and PROVINCE for the exact phase-page URL and distinctive role-table/adaptation strings found the new S095 capture and one older citation: `corpus/source-snapshots/round-24/S003.txt:444` links to the **public_awareness child page**, not this captured parent phase/role table. This is a real prior related reference and must not be described as no prior CERT-guide mentions.

Inference (high confidence within the named comparison): proposed F43 can represent distinct ground **if narrowly scoped to CERT/CC's own adapted phase decomposition and five-role responsibility mapping**, especially separate awareness/deployment and reporter fix confirmation. It is not distinct as a generic claim that disclosure includes intake, validation, remediation and publication. No admission verdict, new row, score change or frozen predicate is supplied by this scout.

Falsifying over-generalization: “CERT/CC's phases are the universal or mandated ISO CVD sequence” conflicts with L57-59 (adaptation with added phases), L73 (models vary), and F38's explicit catalog-only limit. Similarly, public awareness does not itself establish that remediation has been deployed: separate L69/L71 and the Deployer column discriminate the two.

## Scope, evidence limits and handoff

Read round-61 lesson (including prefix/boundary survivors, fail-open runner, and postfreeze screen miss), its verifier spotcheck, QUALITY Q1-Q9/R20-R21, and SCORECARD planned-for-62 L2524-2527. This source evidence does not establish C1 execution behavior or sandboxing. Source publication/revision date was not visible in the read page or converted body/footer; 2026-11-04 is the access date, not a claimed publication date. No ISO normative standard, CERT child-phase page, or live CISA page was fetched by this seat; the CISA/ISO comparisons are explicitly against held lane evidence.

Semantic-tool prerequisite: `read xd://lsp` returned “No such tool”; no language server is available through the mounted device. Searches here are literal textual discovery, not semantic references proof. The inspected contract is documentation/table attribution, not an exported code API. The initial broad discovery search was noisy and one guessed FRONTIER.md target was absent; the actual held frontier was then located in corpus/README.md. No absence conclusion rests on either failed/narrow search.

All writes are this report and the two files in the unique ScoutS095 subdirectory. No scratch was created, so none remains to remove. No git/jj mutation, commit/push, production registry write, fleet/PATH write, package transaction, service restart, or unrelated suite. Only assigned fresh-fetch, conversion/byte comparison and quote binding were exercised. Remaining integration obligations (not performed here): source-manifest/entry predicate freezes, full extended sibling-scope screening and L1 final counters. No claim of exhaustive all-domain novelty.

Report: .ufo/waves/round-62/w1/ScoutS095.md
