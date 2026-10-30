# R47W2ZDITiers — integrated faulty-patch tier review

Axes: **depth:verifiability; coverage**.

Reviewed integrated commit `65e19bdb142c90a08103eb4b2af60c71218a920e`, base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. All paths below are relative to the kasegi-shokunin repository, not the fleet root.

## Findings by severity

**No actionable condition-preservation defect found in this bounded integrated review.** This is a recommendation about the documentation, not an admission or a claim that the frozen targets were met.

The actual committed addition `corpus/knowledge/zdi-disclosure-policy.md:20-22` retains:

- 30 days: **critical-rated**, faulty-patch disclosure, **detected active exploitation OR imminent exploitation**;
- 60 days: **critical OR high severity**, **some protection from the original patch**, **exploitation not imminent**;
- 90 days: **residual reports in the incomplete/faulty-patch category**, not a default for all bugs.

Authority is the full paragraph at `corpus/source-snapshots/round-47/S075.txt:25`, not merely the short quotation cells. The entry's owner/scope (`:9`), requirement to preserve branch conditions (`:36`), and explicit exclusion of the linked blog (`:32`) keep these statements bounded. F02's existing rule separately requires the patch/publication relationship and an evidenced clock trigger (`corpus/knowledge/coordinated-disclosure-timelines.md:7-17`). No generalization to all vulnerabilities is justified.

## 32 distinct post-integration static challenges

These are **32 documentary counterexample challenges, not executed mutants or runtime attacks**. Each result comes from comparing the committed entry with pinned S075:25. `E` means `corpus/knowledge/zdi-disclosure-policy.md`; `S` means `corpus/source-snapshots/round-47/S075.txt`. Rejected means the challenged claim contradicts the cited documentation, not that a program was observed rejecting it.

| # | Challenged claim or boundary case | Static result and evidence |
|---|---|---|
| 01 | Every critical bug gets 30 days. | Rejected: faulty-patch category and exploitation condition both required, E:20,36; S:25. |
| 02 | A high-severity faulty-patch bug with detected exploitation automatically gets the 30-day tier. | Rejected: critical rating retained, E:20; S:25. |
| 03 | A medium-severity faulty-patch bug with imminent exploitation automatically gets 30 days. | Rejected: critical rating retained, E:20; S:25. |
| 04 | Critical faulty patch, detected active exploitation, but no proof of imminence: 30 days cannot apply. | Rejected: “detected or imminent” retains the disjunction, E:20; S:25. |
| 05 | Critical faulty patch, imminent exploitation, but no detected active exploitation: 30 days cannot apply. | Rejected: imminence is independently sufficient for that stated condition, E:20; S:25. |
| 06 | Critical faulty patch, neither detected nor imminent exploitation: severity alone supplies 30 days. | Rejected: E:20 retains the exploitation condition; S:25. |
| 07 | Critical faulty patch with imminent exploitation needs partial protection to qualify for 30 days. | Rejected: partial protection belongs to the 60-day statement, not the 30-day statement, E:20-21; S:25. |
| 08 | A hypothetical possibility of exploitation can replace detected active exploitation or imminence. | Unsupported: neither E:20 nor S:25 defines mere possibility as either condition. |
| 09 | All faulty-patch cases get 60 days. | Rejected: severity, some protection and non-imminence are retained, E:21,36; S:25. |
| 10 | Critical faulty patch, some protection, no imminent exploitation: critical severity excludes 60 days. | Rejected: critical is expressly included, E:21; S:25. No exclusive selection is inferred if detected exploitation also exists. |
| 11 | High-severity faulty patch, some protection, no imminent exploitation: high severity excludes 60 days. | Rejected: high severity is expressly included, E:21; S:25. |
| 12 | Medium severity plus some protection and no imminence establishes 60 days. | Rejected: critical/high condition retained, E:21; S:25. |
| 13 | Low severity plus some protection and no imminence establishes 60 days. | Rejected on the same explicit severity boundary, E:21; S:25. |
| 14 | Critical faulty patch with zero original-patch protection and no imminence establishes 60 days. | Rejected: “some” original-patch protection required, E:21; S:25. |
| 15 | High-severity faulty patch with zero protection and no imminence establishes 60 days. | Rejected: same protection boundary, E:21; S:25. |
| 16 | Critical faulty patch with some protection and imminent exploitation establishes 60 days. | Rejected: non-imminence required; the critical/imminent 30-day statement is separately retained, E:20-21; S:25. |
| 17 | High-severity faulty patch with some protection and imminent exploitation establishes 60 days. | Rejected: non-imminence fails; critical-only 30-day language cannot be borrowed, E:20-22; S:25. |
| 18 | Protection supplied solely by an unrelated mitigation proves the original patch offers protection. | Unsupported: E:21 and S:25 specifically identify the original patch. |
| 19 | Unknown original-patch effectiveness is enough to assert the positive 60-day condition. | Unsupported: missing evidence is not “some protection”; E:21,36. |
| 20 | Unknown imminence establishes “not imminent” for the 60-day branch. | Unsupported: the negative condition is retained, E:21,36. |
| 21 | The 60-day branch requires complete protection from the original patch. | Rejected: source and paraphrase require “some,” not complete, protection, E:21; S:25. |
| 22 | A critical, partly protective faulty patch with detected active but non-imminent exploitation has an unambiguously exclusive 60-day classification. | Not established: S:25's literal predicates can overlap; E:20-21 reproduces them without inventing an exclusivity rule. See residual risk. |
| 23 | A critical faulty patch with neither exploitation condition and no protection is nevertheless forced into 30 or 60 days. | Rejected: neither stated positive predicate holds; E:20-22 preserves the residual category; S:25. |
| 24 | A high-severity faulty patch with imminent exploitation must get 30 days because 60 is unavailable. | Rejected: eliminating one branch does not remove the critical-only condition of another; E:20-22; S:25. |
| 25 | The residual 90 days applies to all new, never-patched vulnerabilities. | Rejected: E:22 expressly says not all reports; S:25 restricts “this category.” |
| 26 | The residual 90-day rule covers only critical/high bugs. | Rejected: severity restrictions belong to the preceding branches; residual “all other reports in this category” is retained, E:22; S:25. |
| 27 | An incomplete patch is excluded unless separately called a regression. | Rejected by the consequence text: E:22 expressly includes incomplete or faulty patches, matching S:25, notwithstanding the short row label. |
| 28 | A faulty patch outside the two named positive tiers has no stated remaining interval. | Rejected: residual 90 days retained, E:22; S:25. |
| 29 | All three intervals are business days. | Unsupported: S:25 says days; E:20-22,36 do not transplant the business-day units of S:23. |
| 30 | The 30-day statement guarantees public release exactly on day 30. | Unsupported: S:25 gives time to produce a new patch or other corrective measure; E:9,36 and F02:7-17 require publication conditions separately. E:20 does not promise publication. |
| 31 | The 120-day rare-extension discretion automatically applies to the faulty-patch tiers. | Unsupported: E:19,24 and S:24 attach it to the 120-day timeline; S:25 supplies no such automatic transplant. |
| 32 | A green quotation/counter check proves complete branch semantics, F30 admission, or both frozen targets achieved. | Rejected: E:32 limits the recheck to pinned support; `corpus/lessons/round-47.md:59-61,65-69` expressly leaves C1 incomplete and C2 unmet; `corpus/README.md:699-702` labels F02 enrichment and admits no F30. |

## Residual risk and verification gaps

1. **Source-level overlap, not a demonstrated repair defect.** S075:25 does not explicitly resolve the critical/detected-active/non-imminent/partly-protective case: its 30-day and 60-day predicates can both read true. E:20-21 preserves those predicates; it does not promise a deterministic classifier. Do not report this review as proving exclusivity, total classification under unknown inputs, or an operational date computation. Additional blog detail is explicitly outside the admitted evidence (E:32).
2. **Short quote checks do not prove paraphrase semantics.** Manifest Q7 binds the critical/exploitation part (`corpus/source-snapshots/round-47/manifest.json:55-58`), whereas Q8 binds only the 60-day interval (`:60-63`) and Q9 binds the residual sentence (`:65-68`). `corpus/instruments/r47-f30-gate.py:113-119,334-347` checks located short cores, not the conjunction of every condition in table consequences. `corpus/instruments/source-recheck.py:156-212` binds source bytes and quote support, not the entry's paraphrases. Therefore preservation was reviewed directly against S075:25; no semantic guarantee is inferred from hypothetical green output. The source hash does still bind the complete captured paragraph; Q8's short span is not an unbound-source allegation.
3. **Honest claim failures remain.** C1's harmful S074 rejection was not performed; C2's new-frontier claim was not met. Those are explicit integrated decisions at `corpus/lessons/round-47.md:59-60`, not defects repaired by tier fidelity. This seat neither rerolls nor independently judges those targets.
4. **Static only.** Executed read-only Git inspection: base→integrated scoped diffs and `git show 65e19bdb142c90a08103eb4b2af60c71218a920e:corpus/knowledge/zdi-disclosure-policy.md`. Pinned files, final lesson, F02, caller links and W1 reports `R47RevEntryQ.md` / `R47RevEntryQuotes.md` were read. No policy runtime, counter, fixture, selftest, battery, live fetch, domain action, canonical judgment or alternative runtime was invoked. Thus the milestone here is 32 distinct static challenges, **not 32 executed post-integration attacks**, and no dynamic rejection result is claimed.
5. **LSP unavailable.** The initial `read xd://lsp` returned “No such tool.” No status/references/definition/diagnostics service was available; textual inspection is explicitly not semantic caller proof. This is documentation-only scope; runtime identity, rerouting, saturation and resume-continuity are not asserted by this report.

## Hygiene and self-evaluation

Read `/home/vgpnk/.omp/agent/RULES.md` before tool decisions. No tools installed/updated; no pacman transactions, service restarts, production edits, Git/JJ mutations, delegation, or scratch creation. Only this report was written; no scratch remains to remove.

Self-evaluation: accuracy **4/5** (pinned and committed evidence, no live freshness); completeness **4/5** (32 scoped static challenges, execution deliberately unrun); clarity **4/5** (overlapping source predicates require a separate caveat); actionability **4/5** (precise limits/citations, no operational classifier claimed); conciseness **4/5** (full challenge matrix retained for auditability). Mean **4.0/5**. Highest-impact improvement for a separately authorized executor is bounded semantic counterexample checking against the exact integrated bytes, not a new full battery. The user should agree this is a static review rather than execution evidence.

Report: .ufo/waves/round-47/w2/R47W2ZDITiers.md
