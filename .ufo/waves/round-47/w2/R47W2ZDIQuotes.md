# R47W2ZDIQuotes — integrated quoted-span review

Axes: **depth:verifiability** (verbatim text, exact location, manifest binding); **coverage** (all ten entry quotations, without substituting an F30 claim).

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Read the committed scoped diff and committed S075 with read-only git commands, the numbered entry/manifest/capture, round-47 lesson, QUALITY Q3/Q9, and W1 `R47CritNovelty.md`. Recommendation only; no admission or canonical judgment.

## Findings, by severity

### Low — manifest description still calls this a new F30 frontier

`corpus/source-snapshots/round-47/manifest.json:3` describes S075 as a “new frontier row F30.” The integrated entry's title (`corpus/knowledge/zdi-disclosure-policy.md:1`), its overlap explanation (:28), and final decision (`corpus/lessons/round-47.md:59-65`) instead retain ZDI as F02 enrichment and explicitly leave C2 unmet. The manifest's unqualified description is stale current-facing metadata, not evidence of coverage. Preserve historical capture material; explain its pre-decision wording in current decision documentation rather than treating it as an admitted row or rewriting frozen targets.

No defective, uncited, or over-25-word quotation was found among the ten entry spans.

## Complete span accounting

Word counts below are manual whitespace-token counts of the text inside quotation marks, excluding the citation. Every span is a verbatim contiguous substring of the indicated S075 line and carries that exact citation in the entry. All are within the manifest's S075 body window, lines 20–27 (`manifest.json:20-23`).

| Entry line | Quoted span | Words | S075 line | Manifest assertion coverage |
|---|---|---:|---:|---|
| 13 | Simultaneous to the vendor notification, protection filters may be distributed | 10 | 22 | No quote assertion contains this span |
| 14 | within five business days | 4 | 23 | No quote assertion contains this span |
| 15 | an additional five business days following the second notification | 9 | 23 | No quote assertion contains this span |
| 16 | fifteen business days after the initial contact | 7 | 23 | Q2, anchor 23 (`manifest.json:31-33`) |
| 17 | four months (120 days) to address the vulnerability | 8 | 24 | Q3, anchor 24 (:36-38) |
| 18 | publish a limited advisory including mitigation | 6 | 24 | Q5, anchor 24 (:46-48) |
| 19 | granted only in rare circumstances | 5 | 24 | Q6, anchor 24 (:51-53) |
| 20 | active exploitation is detected or imminent | 6 | 25 | Q7, anchor 25 (:56-58) |
| 21 | a disclosure window of 60 days | 6 | 25 | Q8, anchor 25 (:61-63) |
| 22 | a time of 90 days | 5 | 25 | Q9, anchor 25 (:66-68) |

The manifest's ten Q ids are not the entry's ten spans: Q1 establishes policy scope, Q4 pins the publication condition, and Q10 pins non-suppression. They must not be reported as ten matching entry quotations. Static inspection also finds all S075 Q1–Q10 strings at their declared source lines, with no overlong manifest quote (largest: Q1, 24 whitespace-separated words).

Surrounding conditions are preserved: :16 and :24 keep exhausted-contact publication permissive; :17, :24 and :36 do not invent the 120-day start; :18 and :24 retain the nonresponse/explanation condition; :19 retains ZDI discretion; :20–22 confine the 30/60/90-day cases to faulty patches and preserve severity/exploitation conditions. No domain action is proposed.

## Residual risk and verification gaps

- Entry :13–15 are **cited but not separately quote-asserted in the manifest**. This is a coverage distinction, not an uncited-source finding. The manifest digest pins the full source, but its explicit assertion list omits those three particular spans. A claim that the existing manifest individually verifies all ten entry quotations would be unsupported.
- The canonical local recheck loop (`corpus/instruments/source-recheck.py:182-211`) iterates manifest assertions against source text; it does not read the knowledge entry. Thus even the seven contained spans are not a runtime entry-to-manifest binding. This report supplies a static comparison only, not a new execution claim.
- LSP unavailable: reading `xd://lsp` returned “No such tool.” No semantic-reference/definition/diagnostics result is claimed; literal inspection was the fallback. This assignment concerns Markdown/JSON/text, not code-callsite proof.
- Executed: read-only committed diff and `git show` inspection. Unrun: source-recheck, hashes, mechanical gates, mutants, selftests, network fetches, or any runtime. No installs, service changes, production edits, git/jj mutations, or scratch artifacts.
- C1 remains not fully met and C2 remains unmet under `corpus/lessons/round-47.md:59-65`; no favorable quotation result rerolls either target. No saturation or whole-corpus novelty claim.

Self-evaluation: accuracy 4/5 (manual/static comparison, no runtime receipt); completeness 5/5 (all ten requested spans and manifest mapping enumerated); clarity 4/5 (manifest Q numbering differs from entry order, explicitly explained); actionability 4/5 (metadata discrepancy and assertion gap located, historical evidence preserved); conciseness 4/5 (table retains every span for auditability). Overall 4.2/5. Improvement: a separately authorized entry-aware check could automate the three unasserted spans; not executed here. User agreement expected on bounded coverage and explicit execution limits.

Report: .ufo/waves/round-47/w2/R47W2ZDIQuotes.md
