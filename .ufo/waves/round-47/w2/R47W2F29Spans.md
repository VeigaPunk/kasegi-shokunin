# R47W2F29Spans — integrated F29 span review

Axes: depth:verifiability; coverage.

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; frozen contract `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Bounded assignment: every quoted S076 span in the F29 entry, exact locators and ≤25 words. This is a recommendation, not admission or judgment.

## Findings, by severity

### Medium — frozen chrome kill-rule is ambiguous for an explicitly labelled negative example

`corpus/knowledge/github-repository-security-advisories.md:11` quotes **“Copy markdown”** and locates it exactly at `corpus/source-snapshots/round-47/S076.txt:559`. It is correctly labelled **page chrome**, not substantive policy evidence. The quote has two words, is exact, and does not masquerade as lifecycle guidance.

However, `.ufo/waves/round-47/claims.json:14` makes “a re-anchored span citing a chrome line” a semantic kill condition without an explicit exception for labelled chrome examples. A broad any-cited-span reading therefore catches this occurrence; a narrower re-anchored-policy-evidence reading does not (this label was added during correction, not substituted for an old policy quote). The numeric body window cannot resolve that distinction: `manifest.json:92-95` includes 559 inside 558–600 although the capture itself identifies the text as chrome. Do not call this policy-evidence contamination or silently waive/rewrite the frozen rule. Record the ambiguity alongside the already-unmet frozen C1 target. The safe correction and honest boundary statement need not be undone to manufacture a pass.

No wrong locator, altered quote wording, or >25-word quotation was found in the scoped inventory below.

## Complete span inventory

Abbreviations: **E** = `corpus/knowledge/github-repository-security-advisories.md`; **S** = `corpus/source-snapshots/round-47/S076.txt`. Every row was compared to the cited source line, including all repeated occurrences. Counts split whitespace-separated words; line wrapping in E is treated as whitespace, not as inserted source punctuation. Titles are link labels, not claims that sibling bodies were opened.

| Quoted text (identifying opening or full short label) | Every E occurrence | Exact S line | Words | Result |
|---|---|---:|---:|---|
| Copy markdown | 11 | 559 | 2 | Exact; labelled chrome, not policy |
| You can use repository security advisories to privately discuss… | 12, 28 | 558 | 20 | Exact |
| Repository security advisories and private vulnerability reporting… | 13, 29 | 561 | 14 | Exact |
| Repository security advisories allow maintainers of public repositories… | 14, 30 | 568 | 19 | Exact |
| Create a draft security advisory, and use the draft… | 18, 31, 126–128 | 570 | 20 | Exact |
| Privately collaborate to fix the vulnerability… | 19, 32, 129–130 | 571 | 11 | Exact |
| Whenever possible, you should add a fix version… | 20, 110–111 | 596 | 17 | Exact; includes qualification |
| Requesting a CVE identification number doesn't make… | 21, 41, 131–132 | 583 | 11 | Exact |
| GitHub is a CVE Numbering Authority (CNA)… | 21, 39, 133–134 | 582 | 15 | Exact |
| GitHub usually reviews the request within 72 hours. | 21, 40 | 583 | 8 | Exact |
| This process can take up to 72 hours… | 24, 45 | 594 | 16 | Exact |
| Publish the security advisory to alert your community… | 33 | 572 | 16 | Exact |
| You can also use repository security advisories to republish… | 34 | 573 | 21 | Exact contiguous prefix, no invented period |
| You can give credit to individuals… | 35 | 575 | 12 | Exact |
| If you created a security advisory in your repository… | 36 | 577 | 17 | Exact |
| We publish security advisories for any of the ecosystems… | 37 | 577 | 21 | Exact |
| If a security advisory is specifically for npm… | 38 | 578 | 18 | Exact |
| GitHub cannot assign CVEs to your project… | 42, 136–137 | 584 | 14 | Exact |
| Anyone can see the current version of the advisory data… | 43, 143–144 | 589 | 22 | Exact |
| Collaborators can view the conversation history of the advisory. | 44, 144–145 | 590 | 9 | Exact |
| you should add a fix version to a security advisory… | 46, 139–140 | 596 | 15 | Exact substring; surrounding source qualification remains relevant |
| Creating a repository security advisory | 92 | 575 | 5 | Exact link label |
| REST API endpoints for repository security advisories | 92–93 | 574 | 7 | Exact link label |
| Editing a repository security advisory | 93–94 | 592 | 5 | Exact link label |
| Editing security advisories in the GitHub Advisory Database | 94–95 | 577 | 8 | Exact link label |
| The security advisory form on GitHub is a standardized form… | 96–97 | 581 | 16 | Exact |
| You can also use the REST API to create, list, and update… | 99–100 | 574 | 15 | Exact |
| The URL of a security advisory does not change after publication. | 107–108 | 591 | 11 | Exact |
| Imminently available, and you are able to, wait to disclose… | 112 | 598 | 17 | Exact; includes ability qualification |

Inventory: **47 quote occurrences, 29 distinct quoted strings; maximum 22 words.** Of these, 46 occurrences are source-body prose or expressly identified sibling link labels; the remaining occurrence is the labelled chrome example. Bare references to S076:599/600 and navigation/footer ranges are not quotations. They are not additional quoted spans, and the manifest's Q11/Q12 are not quoted in this entry.

## Residual risk and verification gaps

- Exact quotation is not semantic entailment. In particular, omission of “Whenever possible” from the short substring at E:46/139–140 does not invalidate its textual match, but cannot prove an unconditional fix-version duty. Claims review owns that inference. Qualification at S:598 likewise survives the quote but not necessarily surrounding paraphrase.
- The source header E:3 and limits E:89 use the enclosing 558–600 interval as prose shorthand even though 559 and 562–565 contain chrome; both locations explicitly acknowledge chrome. No policy quote in this inventory relies on those chrome lines.
- C1 remains not fully met because S074 stays mined historical rather than undergoing the harmful frozen mined→rejected transition; C2 remains unmet because ZDI is F02 enrichment and there is no F30 admission. These are preserved decisions in `corpus/lessons/round-47.md:57–69`, not rerolled targets. This span audit neither repairs nor overrides either outcome.
- No live reopening, counter, source-recheck, mutation battery, selftest, application runtime, or domain-target action was executed. No canonical-runtime/resume behavior is affected by this documentary slice; no runtime or saturation claim is made.

## Evidence and method

Executed read-only Git commands: integrated diff stat; base→integrated diff restricted to E; `git show 65e19bdb142c90a08103eb4b2af60c71218a920e:<E>` and the corresponding committed S076 capture. Numbered file reads supplied exact line references; static comparison covered S:558–600 and all E:1–145. Read the round-47 lesson and W1 `R47SrLesson.md` for historical decision boundaries. This was manual static review, not an executed automated word-count/quote validator.

LSP availability: `read xd://lsp` returned **No such tool**; no LSP server/device was mounted, so status/references/definition/diagnostics could not run. Narrow text search located the entry; it is not offered as semantic proof. No tools installed or updated; no scratch created, hence no scratch cleanup required. Only this assigned report was written; no production/capture/history edits, service changes, delegation, or git/jj mutations.

Self-evaluation (not a gate): accuracy 4/5 (manual counts, no independent automated recount); completeness 4/5 (all 47 scoped occurrences, live drift intentionally untested); clarity 4/5 (opening-text identifiers require the cited E lines for full wording); actionability 4/5 (explicit frozen-rule ambiguity needs closure interpretation, not a local contract edit); conciseness 4/5 (full occurrence inventory is necessarily repetitive). Mean 4.0/5. Improvement priority: any later permitted independent recount should preserve the distinction between textual exactness and policy entailment.

Report: .ufo/waves/round-47/w2/R47W2F29Spans.md
