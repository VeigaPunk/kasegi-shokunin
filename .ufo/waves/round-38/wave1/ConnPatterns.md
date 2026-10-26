# ConnPatterns — round-38 wave-1 receipt

seat: ConnPatterns (leaf, patterns)
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin at base a173b0c2b98c5ae39599fa9be76027fbbead0b9e (claims freeze 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b)
item: cross-link F21 (OASIS CSAF v2.0 VEX) into the corpus — read F01/F18/F19/F20 entries and SKILL.md triage/prioritization and duplicate/not-applicable dispute sections; propose the cross-reference sentences the F21 entry should carry; assess whether any existing entry should gain a see-also in a later round (never edit now); name the pattern the four prioritization/status sources share and where VEX differs. Receipt only.
milestone: round-38 · judged on coverage · leaf seat, no subagent dispatch, no labrat probe

## Evidence read (all read-only)

- `.ufo/waves/round-38/claims.json` — C2: frontier F21 = CSAF v2.0 VEX product-status categories + machine-readable not-affected justification flags; registry S055 (tier A, kind spec, opened 2026-10-26); entry `corpus/knowledge/csaf-vex-product-status-and-justifications.md` (`source: S055`); before-state knowledge 49 → after 50; harness 23→24, binding 44→45; RE 49→50.
- `corpus/knowledge/cvss-v4-severity-and-vector.md` (F01, S001/S002) — severity, not risk; nomenclature labels; server is this external consumer context.
- `corpus/knowledge/cisa-kev-catalog.md` (F18, S052) — CISA catalog membership = exploitation-status signal with per-record remediation clock; claim 5 "not a severity ladder"; rejected #1 "KEV membership is a CVSS severity band".
- `corpus/knowledge/epss-exploit-prediction-scoring.md` (F19, S053) — 0–1 probability, 30-day horizon, per published CVE; claim 4 distinct axes; "combine EPSS with CVSS and KEV" (S053 L224); rejected #2/#3 (severity substitute; KEV membership).
- `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (F20, S054) — stakeholder-specific priority categories; "Sources overlap" section: axes stack rather than compete; EPSS fed into Exploitation (L93), KEV as decision point "In KEV" (L153), CVSS separate branches (L69-L70, L156-L157); Supplier example "does not use the vulnerable part of a library" → "probably not" risk (L245-L246); rejected #1/#5 (replaces CVSS; membership is KEV status).
- `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (F16) — citation precedent: sibling cited as `F13 (`knowledge/program-severity-ladders-and-reward-scales.md`, S043-S045)` (L244). No `see-also` mechanism exists anywhere in the corpus; cross-references are prose by F-id + source-id (F20's "Sources overlap" section is the template). `ground:` header ties each entry to its frontier id (F09/F10/F11/F12/F14/F16/F17/F18/F19/F20 present).
- `corpus/knowledge/` directory listing — 49 entries currently (matches C2 before-state; the F21 entry is not yet landed).
- `corpus/README.md` — frontier table has F01..F20 admitted rows; no F21 row yet.
- `corpus/SOURCES.md` — no S055 row yet; `corpus/source-snapshots/round-38/` not yet committed (pre-landing, per C2 "after" state).
- `corpus/QUALITY.md` — Q1–Q6, Q9 (quote exactly-once or verified anchor), Q10 (recheck line form).
- `SKILL.md` — see grep results below.
- `corpus/knowledge/triage-thresholds.md` §4.8 — claimability/duplication/blockers gates (prior submission; global duplicate; blockers; nested readiness).
- Wave sibling `ScribeEntryF21.entry.md` (F21 entry draft, 137 lines / 22,827 bytes / sha256 96899762d9d565ce32753ee3b4c80394aa64342b19c8bbe81e303fe15734f129) and `ScribeEntryF21.md` — the draft already contains a "Sources overlap — CSAF VEX against CVSS (F01), KEV (F18), EPSS (F19) and SSVC (F20)" section (lexical counts CVSS=73, EPSS/KEV/SSVC=0) and a "How a bounty or security researcher uses it" section; my proposal extends those sections with the issuer/subject framing, it does not restate them.

## Commands run, with output

1. Fetch of the S055 URL for independent grounding of the VEX facts (network rule; status/bytes/UTC recorded):
```
$ S=/fast/scratch/hyaku/kasegi-r38/ConnPatterns; mkdir -p "$S"; cd "$S"; start=$(date -u +%Y-%m-%dT%H:%M:%SZ); curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' -o csaf.html -w 'http_code=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html; date -u +fetched_utc=%Y-%m-%dT%H:%M:%SZ
http_code=200 bytes=414858 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
fetched_utc=2026-10-26T18:36:09Z
```
Extracted (Python, HTML→text normalization) and confirmed from the spec bytes: eight `product_status` properties (first_affected, first_fixed, fixed, known_affected, known_not_affected, last_affected, recommended, under_investigation); the contradiction groups (Affected / Not affected / Fixed / Under investigation); the VEX profile requirement 6.1.27.7 (at least one of fixed, known_affected, known_not_affected, under_investigation); tests 6.1.27.9 (impact statement for known_not_affected) and 6.1.27.10 (action statement for known_affected); 6.1.33 (one VEX justification code per product); the five flag labels with meanings (component_not_present; vulnerable_code_not_present; vulnerable_code_cannot_be_controlled_by_adversary; vulnerable_code_not_in_execute_path; inline_mitigations_already_exist); "The given values reflect the VEX not affected justifications."; and "semantic ... out of scope for this specification".

2. SKILL.md dispute-term grep (`grep -nE`): literals `not applicable`, `N/A`, `informative` occur **0 times** in SKILL.md. `duplicate` hits: L163 (global duplicate-submission scan), L560 (`no_duplicate_or_prior_submission` hard gate), L616, L695 (receipt-drift hazard), L723-L724 (closed_duplicate / not_established), L743 (duplicate scan blind spots), L755 (`duplicate_of` alias convention), L933 (duplicate attestation suppressed), L1054/L1067 (frontier duplicate-entry limbs).

3. SKILL.md triage/prioritization headings: `Finding-triage decision table` (L134+), `Triage economics` (L805+), `Submitted-state registry — the do-not-refile set` (L715+), `Disclosure anti-patterns` (L565+), `Intake surface` (L171+). The `DEDUPED` state appears in the rank stateOrder ladder (L911; canonical derivation triage-thresholds.md §4.8).

4. Knowledge dir count:
```
$ ls -1 corpus/knowledge/*.md | wc -l
49
```

5. Sibling-citation scan across knowledge entries: only F16 cites a sibling by path (`program-severity-ladders-and-reward-scales.md`, L244); no other entry cites a sibling by filename; F-id + source-id prose references are the established cross-link idiom.

## Findings

### 1. The shared pattern of the four sources (named)

The four prioritization/status sources F01/F18/F19/F20 are **single-axis, third-party status signals**: each is issued by an authority external to the reporting vendor (FIRST for CVSS and EPSS, CISA for KEV, CERT/CC for SSVC), each documents exactly one axis of the *vulnerability* (severity · known-exploited membership · exploitation likelihood over 30 days · stakeholder-specific priority category), each is machine-readable and scalar (score, membership, probability, category label), and the corpus's standing rule is that they **stack rather than compete** — F19's claim 4 ("combine EPSS with CVSS and KEV", S053 L224), F20's "Sources overlap" section ("the axes therefore stack rather than compete"), F18 claim 5, and the recurring rejected over-generalizations (F18 #1, F19 #2/#3, F20 #1/#5) all enforce non-conflation. The subject of every one is the CVE/vulnerability in the abstract, not a particular product build.

### 2. Where VEX differs

VEX (CSAF v2.0 profile 5) inverts both the issuer and the subject: **the issuing party is the supplier (vendor) or other party itself**, and the assertion is about **that party's own product versions** — "enables a supplier or other party to assert whether or not a particular product is affected by a specific vulnerability" (S055 L394); product_status "contains different lists of product_ids which provide details on the status of the referenced product" (L1855). So: (a) the four external signals answer questions about the vulnerability; VEX answers the question about the product; (b) the four external signals are computed/decided by independent bodies; VEX is a first-party statement that the standard validates only for shape, not truth — "any deep validation on a semantic level ... is to be ensured by the producer", "It is out of scope for this specification." (L516); (c) VEX carries the vendor's own machine-readable *reason* (the five justification flags for known_not_affected), a feature none of the four has; (d) a single VEX item can carry different statuses for different products in the same document.

### 3. The dispute mapping into SKILL.md

SKILL.md has no literal N/A/informative vocabulary; not-applicable-shaped outcomes are encoded as verdicts (`honest-zero` for bounded negatives, `positive-blocked`, `RETIRED auth-walled`) and the duplicate machinery (global duplicate-submission scan, `no_duplicate_or_prior_submission`, `closed_duplicate`/`DUPLICATE_OF_SUBMITTED`, `DEDUPED`). A vendor's VEX `known_not_affected` flag is a first-party assertion of non-affectedness — the machine-readable analogue of a "not applicable" reply — and the lane's rule (consistent with the F21 draft's use item 1 and the VEX semantics) is that it is evidence to dispute against the specific label (S055 L1763-L1769), never a gate that closes a finding or a submission.

### 4. Proposed cross-reference sentences for the F21 entry

Below, in the DELIVERABLE block, are the sentences I propose the F21 entry (`corpus/knowledge/csaf-vex-product-status-and-justifications.md`) should carry, to be inserted into its existing "Sources overlap" and "How a bounty or security researcher uses it" sections by the owning seat in a later round. They follow the corpus's established cross-link idiom (F-id + source-id prose, "lane analysis" marker where the claim is not a quote). Each sentence's S055 anchors are the ones already verified by the F21 draft; S054 L245-L246 anchors come from the F20 entry.

### 5. See-also assessment for existing entries (later round)

- **F20 SSVC — primary recommendation: gain a VEX pointer.** SSVC's Supplier worked example — a Supplier that "does not use the vulnerable part of a library" is "probably not" at risk (S054 L245-L246) — is the decision-side mirror of the VEX `component_not_present`/`vulnerable_code_not_present` labels (S055 L1763-L1764): SSVC supplies the decision model that consumes such evidence, VEX supplies the vendor's machine-readable affectedness assertion. A one-sentence addition to F20's "Sources overlap" section (marked lane analysis, as the section already is) completes the axes table with the fifth, first-party axis and closes the only gap in that section's otherwise exhaustive enumeration. Also worth distinguishing: SSVC's `Defer` ("do not act at present", L262) is time-based, VEX `known_not_affected` is intrinsic ("No remediation is required", L1890).
- **F19 EPSS — optional.** A low EPSS probability is an estimate about the CVE in the wild and neither implies nor is implied by a VEX `known_not_affected` declaration; this is the same conflation family as F19's rejected #3 ("EPSS membership is KEV status"). Recommend adding it to F19's rejected over-generalizations **only** if a later round touches F19 anyway (its capture never mentions VEX, so the sentence must stay lane-analysis and cannot claim S053 support).
- **F18 KEV — no see-also.** S052 never mentions VEX; F18 claim 5 and rejected #1 already draw the severity/membership boundary. The one true fact (a CVE stays in KEV regardless of a vendor's VEX) belongs in the F21 entry (proposal sentence 3), not in F18, which should not gain an anchor its capture cannot support.
- **F01 CVSS — no see-also.** The CVSS delegation is a property of CSAF (S055 L522, L2026-L2028), already captured in the F21 draft's Sources-overlap bullets; F01 has no capture-side hook for VEX.

## DELIVERABLE

```
## DELIVERABLE
- The four neighbour entries are third-party signals about the vulnerability itself, issued outside the reporting vendor: FIRST's CVSS scores severity (F01/S001), CISA's KEV lists known-exploited CVEs (F18/S052), FIRST's EPSS estimates a 30-day exploitation probability per published CVE (F19/S053), and CERT/CC's SSVC derives a stakeholder-specific priority category (F20/S054); each is one axis of the same CVE, and the corpus treats them as stackable, never interchangeable (F19 Claim 4; F20 rejected over-generalizations).
- VEX is the fifth, first-party signal, and it changes both the issuer and the subject: the supplier or other party asserts whether its own product versions are affected (S055 L394), so the subject is the product version, not the CVE — a single vulnerability item can carry different statuses for different products (S055 L1855).
- A vendor's VEX can disagree with all four external signals without invalidating any of them: the CVE remains listed in KEV (S052), still scored by CVSS (S001), still carrying an EPSS probability (S053) and an SSVC priority (S054), while the vendor asserts a particular build is known_not_affected for one of the five justification reasons (S055 L1763-L1769); the signals answer different questions, and none is proof against another.
- When disputing a not-applicable decision, the VEX flag names the vendor's asserted reason (component_not_present, vulnerable_code_not_present, vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path, inline_mitigations_already_exist, S055 L1763-L1769); semantic correctness is out of scope for the standard (S055 L516), so the dispute is argued against the specific label with code or dependency evidence, and the program's scope or duplicate decision stays with the program (SKILL.md Finding-triage decision table; triage-thresholds.md §4.8).
- SSVC's Supplier example — a Supplier that does not use the vulnerable part of a library is "probably not" at risk (S054 L245-L246) — is the decision-side mirror of the VEX component_not_present and vulnerable_code_not_present labels (S055 L1763-L1764): SSVC supplies the decision model, VEX supplies the vendor's machine-readable affectedness assertion the decision can consume (lane analysis, not a quote from either capture).
- Proposed see-also for a LATER round: F20 SSVC should gain one sentence in its "Sources overlap" section pointing at F21 (the fifth, first-party axis and the Defer-versus-known_not_affected distinction); F19 EPSS optionally gains a rejected over-generalization on low-probability vs. not-affected; F18 KEV and F01 CVSS should not gain a see-also (no capture-side support).
```
## Validation

- Receipt file: `ConnPatterns.md` — 94 lines, 16,117 bytes (measured at copy time; the receipt cannot carry its own sha256 without circularity).
- DELIVERABLE block (the only landable text): 7 lines including its `## DELIVERABLE` heading, 2695 bytes, sha256 `d38a8d4a03647838dc6532b3c370f178497757baaa852c46b42e386a2ee0e8de`.
- No edits made anywhere in the lane, fleet, sibling lanes, or source trees; no git/jj mutation; no installs (no tooling change; pacman untouched).
- Scratch `/fast/scratch/hyaku/kasegi-r38/ConnPatterns/` removed after copying this receipt into the wave dir (verified absent below).

## Touched surfaces

- Written: `.ufo/waves/round-38/wave1/ConnPatterns.md` (this receipt, the only write).
- Read-only: claims.json; corpus/knowledge/{cvss-v4-severity-and-vector,cisa-kev-catalog,epss-exploit-prediction-scoring,ssvc-stakeholder-specific-vulnerability-categorization,chinese-crowdsourced-testing-scope-and-rewards,triage-thresholds}.md; corpus/README.md; corpus/SOURCES.md; corpus/QUALITY.md; SKILL.md; .ufo/waves/round-38/wave1/{ScribeEntryF21.entry.md,ScribeEntryF21.md}; the OASIS CSAF v2.0 os page (network fetch above).
- Not edited: any other seat's deliverable, the capture/manifest, the registry, the frontier table, the entry draft, any lane source.
