# R47W2EntryBar — integrated ZDI entry admission review

Axes: **depth:verifiability**, **coverage**. Static recommendation only; no admission, integration, judgment, runtime, or domain-target action.

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e`, base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Executed read-only `git diff` and `git show` of the actual committed entry/manifest, plus textual source, registry, lesson and QUALITY inspection. This reviews the new committed entry, not the absent-entry fallback in W1 `R47RevEntryQ.md:7`.

## Findings by severity

### Medium — Q3 is incompletely satisfied: short true quotations do not cover all load-bearing conditions

`corpus/QUALITY.md:16` requires **each load-bearing claim** to carry a verbatim located quotation of at most 25 words. All ten quotations in `corpus/knowledge/zdi-disclosure-policy.md:13-22` are genuine short spans at their stated locations. That establishes quotation fidelity, not complete claim coverage:

- Entry `:21` quotes only “a disclosure window of 60 days”. Its package consequence adds three decisive conditions: critical/high severity, some original-patch protection, and no imminent exploitation. Those conditions are indeed present at `corpus/source-snapshots/round-47/S075.txt:25`, but none appears in this entry's quotation. The manifest's corresponding Q8 (`corpus/source-snapshots/round-47/manifest.json:60-64`) also quotes only the interval, so it does not fill the condition-quotation gap.
- Entry `:20` quotes the active-exploitation condition but leaves the critical rating and the number **30** only in its paraphrase. The fuller, already pinned quotation at `manifest.json:55-59` demonstrates that a short exact quotation containing both is available.
- Entry `:24` and `:28` introduce/repeat the acquired-vulnerability non-suppression rule without any quotation of line 26 in the entry. This is especially load-bearing because `corpus/SOURCES.md:81` chooses that rule as S075's teaches statement. Manifest Q10 (`manifest.json:70-74`) pins an appropriate 20-word quotation, but the entry does not carry it. The workarounds proposition in `:24` likewise remains paraphrase plus location only.

Impact: the text is not shown false; the admission evidence is weaker than the explicit Q3 bar. A green quote-location or five-core detector cannot establish that all conditions and the added disposition claim were quoted. W1 `R47RevEntryQuotes.md:17-32` proved ten quoted spans and five cores, and explicitly excluded branch semantics at `:58`; it did not close this completeness issue.

Smallest warranted correction: use short located spans that include the 30-day severity/count and the 60-day applicability predicates, and carry a located short non-suppression quotation beside that claim. Keep the existing correct attribution and boundaries; do not add a frontier row or change historical captures. Until then, recommend treating Q3 as incomplete rather than describing Q1–Q6 as wholly met. This is a static finding, not an executed mutation result.

## Q1–Q6 disposition

| Criterion | Evidence and recommendation |
|---|---|
| Q1 — H1 then provenance trio | Entry `:1` is H1; after the ordinary blank separator, `:3-5` are contiguous `source:`, `verified-at:`, `recheck:` lines, before any body heading. Source names S075, official URL, exact captured body range and digest; date is ISO; recheck is one lane-root-prefixed command with cadence in a shell comment. No intervening ground field or prose disrupts the trio. Static fail-closed support: `source-recheck.py:52-62,216-229` returns 2 for missing/invalid manifest or missing selection; `:156-174` returns 2 for absent capture and 1 for digest mismatch. Command execution unrun. |
| Q2 — scoped tier A/B support | `SOURCES.md:81` marks S075 docs/A/mined with exclusions matching entry `:32`; lesson `corpus/lessons/round-47.md:20` records this round's personal open, HTTP 200, timestamp and digest. `manifest.json:6-22` binds that source URL and body. The entry uses first-party policy text for policy assertions, not an advisory or reward page. Historical access is inspected evidence, not a live reopen by this reviewer. |
| Q3 — exact located quotations | All ten table quotations agree with their named capture lines 22–25 and are below the 25-word ceiling. No fabricated quotation identified. Completeness nevertheless fails as described above. The capture revision is pinned by the source header, not an assumed current webpage. |
| Q4 — attribution | Entry `:9,24,28,32` consistently attributes the policy to TrendAI ZDI, distinguishes a broker-set vendor-remediation deadline from a vendor's own policy, and refuses a universal researcher deadline. “May” for the fifteen-business-day fallback, sole-discretion extensions, and faulty-patch scope are preserved in prose. No first-party promise is presented as observed conduct. |
| Q5 — falsifiable rule and rejected generalization | Entry `:36` gives a concrete package test: owner, selected branch, preserved conditions/units and unknown 120-day start unless separately evidenced. It explicitly rejects publication exactly 120 days after acquisition, with source-based reasons. The full source `S075.txt:24` states a timely response as a branch selector but does not explicitly state that interval's origin; selecting a branch is not proof of a clock start. |
| Q6 — documentation-only | Entry `:9,32,36` confines actions to recording/checking a package. No instructions to probe, scan, log in or submit against a target; no credentials/session/private URL/vault reference found in the entry. Captured navigation includes “Log In” (`S075.txt:11,18`) but is outside the declared body and is not reproduced as an entry instruction. |

## Bounded adversarial checks — static, not executed mutants

1. **Universal deadline:** rejected by `:9,36`.
2. **Acquisition starts 120 days:** rejected by `:9,36`; source `:24` supplies no explicit start.
3. **Acknowledgement starts 120 days:** also rejected by the explicit unknown-start rule at `:9`.
4. **Exactly 120 days for every finding:** rejected by branch differentiation at `:14-22,36`.
5. **Fifteen calendar days:** contradicted by exact “business days” quotation at `:16`.
6. **Mandatory publication at fifteen business days:** prose `:16,24` retains possibility and exhausted-contact prerequisite.
7. **Unconditional deadline publication:** `:18,24` retains nonresponse/inadequate-explanation condition.
8. **Extension is an entitlement:** `:19,24` rejects it as ZDI's discretion.
9. **Thirty days for all critical reports:** `:20` retains faulty-patch scope and exploitation condition; Q3 quotation completeness still open.
10. **Sixty days without patch protection:** `:21` rejects that reading in prose; this is precisely a predicate not carried by the short quote.
11. **Ninety days is the ordinary policy:** `:22` limits it to the residual faulty-patch category.
12. **Customer filters equal public disclosure:** `:13` keeps them separate.
13. **Vendor refusal proves suppression:** `:24` rejects that reading, but the corresponding exact quotation is missing from the entry.
14. **The page establishes purchase/legal ownership:** `:28` expressly disclaims both; no acquisition-based trigger inferred.
15. **The policy proves an actual advisory was published:** `:32` rejects that inference.
16. **ZDI adds an independent frontier topic:** `:28` rejects it; F02 method comparison is accurately supported by `coordinated-disclosure-timelines.md:6-17`, and the F15 distinction by `vendor-third-party-finding-coordination.md:17-59,114-120`.

These are sixteen distinct textual challenges, not sixteen test executions, mutation kills, or a claim to have personally completed the wave's 32-attack milestone.

## Residual risk and verification gaps

- Frozen claims remain honest failures: `corpus/lessons/round-47.md:59` says C1 is not fully verified because rejecting S074 harms B3; `:60,65` says C2 is unmet and retains ZDI only as F02 enrichment. No F30 admission is recommended. A mechanically green counter would not cure either frozen target or the Q3 finding.
- The retained capture manifest's historical `note` at `corpus/source-snapshots/round-47/manifest.json:3` still calls S075 “new frontier row F30”. Current decisions at lesson `:60,65` and `corpus/README.md:699-702` override that description; do not quote the old note as evidence of admission. Prior capture metadata was not edited.
- No recheck, selftest, mutation battery, fixture driver, live fetch, or other runtime was invoked. Missing/corrupt handling above is code inspection, not newly exercised exit-code evidence. No fresh network validity or full-wave saturation is asserted. Runtime identity/rerouting/resume preflight contracts are not changed by this documentation entry and were not evaluated.
- LSP unavailable: `read xd://lsp` returned `No such tool`. No server/status/references/definition/diagnostics facility was available; literal grep/read and committed diff inspection are not semantic reference proof.
- No installs/updates, service restarts, git/jj mutations, shared production edits, historical-capture edits, delegation or scratch creation occurred. Only this scoped report was written.

Self-evaluation: accuracy 4/5 (static evidence only, no runtime or live freshness); completeness 4/5 (Q1–Q6 and all entry branches covered, execution forbidden); clarity 4/5 (separates true paraphrase from unmet quotation bar); actionability 4/5 (precise short-quote repair without changing policy or claims); conciseness 4/5 (retains attack inventory to distinguish review from tests). Mean 4.0/5. Highest-impact improvement: close the narrowly identified Q3 evidence gaps, then have the authorized main verifier exercise the existing canonical recheck without treating it as a novelty gate.

Report: .ufo/waves/round-47/w2/R47W2EntryBar.md
