# R47ScoutEntrySpans — independent F29 quote audit

Axes: depth:verifiability; coverage.

## Findings

**Observed: 47/47 quotation occurrences re-locate exactly at their cited S076 lines; no wrong citation, missing quotation, out-of-range citation, over-12-line span, or over-25-word quotation.** There are 29 distinct quotation texts. Every cited span is one source line, inside numerical range 558–600; maximum quotation length is 22 whitespace-delimited words.

**One chrome hit must be disclosed:** `corpus/instruments/entry29-fixed-bytes.md:11` quotes “Copy markdown” and cites `S076.txt:559`. The citation is correct (2 words, 1 line), but source line 559 is page chrome, not prose. The draft explicitly labels it chrome; this is not evidence misrepresented as body prose. A literal requirement that *every* quoted span be non-chrome therefore fails once; a requirement that substantive evidence avoid chrome passes. No other quoted span lands on TOC/navigation/footer. Source lines 558 and 561 are genuine descriptive prose inside the surrounding chrome area, not TOC entries.

**Observed: exactly 145 lines**, including 145 newline bytes. S076 SHA-256 computed independently: `9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38`, matching the draft's source header.

## Three corrected sentences

- **D6a — supported, with range precision:** draft lines 11 and 89 acknowledge chrome rather than calling the complete capture prose. `corpus/source-snapshots/round-47/S076.txt:556` is “In this article”; :559 is “Copy markdown”; :562–565 are TOC items; :601–610 are footer/support material. “Prose spans 558–600” is an enclosing range, not a claim that every included line is prose. Line 566 repeats the section title at the TOC/body transition, so its exact classification is immaterial to quotations: none cite it.
- **D6b — supported:** draft :16 says the page states the CVE request before fix-version material and labels the entry numbering as its own. S076 :580–585 is CVE material, with request at :583; fix-version heading is :595 and recommendation :596. Source order is unambiguous.
- **D6c — supported as a conditional recommendation:** draft :110–113 identifies only :599–600 as publish-without-fix cases, versus :598 instructing “Imminently available, and you are able to, wait to disclose the issue when the fix is ready.” Source :599 explicitly permits editing after publication; :600 addresses no planned fix. The draft's word “forbids” should be read under :598's condition (“and you are able to”), not as an unconditional platform enforcement rule; :596 says “Whenever possible”. This is a wording limitation, not a third publish-without-fix case.

## Independent procedure and printed receipt

Read the full draft and S076 :556–610, including untruncated :583. A fresh Python Eval scan paired every curly-quoted span immediately followed by a parenthesized backticked `S076.txt:N` or `N-M` citation, folded whitespace, stripped Markdown emphasis/backticks and converted Markdown links to labels. Each quote was searched across every individual source line independently, then checked against its claimed inclusive range. All 47 matches had exactly one source-line location. Multi-line draft wrapping was normalized; source spans remained single-line. No fuzzy matching or citation-derived assumed location was used.

Printed output:

```text
draft_lines=145 newline_count=145
sha256=9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38
quote_occurrences=47 unique_quotes=29
all exact=True; all body_numeric_range=True; all source_span_lines=1
max_quote_words=22
violations=[entry:11, cite:559, words:2, lines:1, located:[559], chrome:True, quote:Copy markdown]
```

## Complete span inventory

Entry lines identify the opening quote (a wrapped quotation may close later). Every row has independently located source line equal to the citation and a one-line source span.

| Draft opening line | S076 citation / independently located line | Words | Classification |
|---|---|---|---|
| 11 | 559 | 2 | CHROME (explicitly identified) |
| 12 | 558 | 20 | OK |
| 13 | 561 | 14 | OK |
| 14 | 568 | 19 | OK |
| 18 | 570 | 20 | OK |
| 19 | 571 | 11 | OK |
| 20 | 596 | 17 | OK |
| 21 | 583 | 11 | OK |
| 21 | 582 | 15 | OK |
| 21 | 583 | 8 | OK |
| 24 | 594 | 16 | OK |
| 28 | 558 | 20 | OK |
| 29 | 561 | 14 | OK |
| 30 | 568 | 19 | OK |
| 31 | 570 | 20 | OK |
| 32 | 571 | 11 | OK |
| 33 | 572 | 16 | OK |
| 34 | 573 | 21 | OK |
| 35 | 575 | 12 | OK |
| 36 | 577 | 17 | OK |
| 37 | 577 | 21 | OK |
| 38 | 578 | 18 | OK |
| 39 | 582 | 15 | OK |
| 40 | 583 | 8 | OK |
| 41 | 583 | 11 | OK |
| 42 | 584 | 14 | OK |
| 43 | 589 | 22 | OK |
| 44 | 590 | 9 | OK |
| 45 | 594 | 16 | OK |
| 46 | 596 | 15 | OK |
| 92 | 575 | 5 | OK |
| 92 | 574 | 7 | OK |
| 93 | 592 | 5 | OK |
| 94 | 577 | 8 | OK |
| 96 | 581 | 16 | OK |
| 99 | 574 | 15 | OK |
| 107 | 591 | 11 | OK |
| 110 | 596 | 17 | OK |
| 112 | 598 | 17 | OK |
| 126 | 570 | 20 | OK |
| 129 | 571 | 11 | OK |
| 131 | 583 | 11 | OK |
| 133 | 582 | 15 | OK |
| 136 | 584 | 14 | OK |
| 139 | 596 | 15 | OK |
| 143 | 589 | 22 | OK |
| 144 | 590 | 9 | OK |

## Do-nothing control and limitations

The unchanged production entry `corpus/knowledge/github-repository-security-advisories.md` is the do-nothing control. Its :11 and :89 still say the whole S074 capture is body prose; :16 still says its numbering follows page order although its :20 fix-version item precedes :21 CVE item; :111–112 still call all three cases publish-without-fix cases. Those textual defects remain in the control and are corrected in the reviewed draft. This is a direct source/order comparison, not a counter run; no routed-defects counter, full battery, or live-page recheck was run. The supplied known mutation-survivor gaps remain unclosed by this audit.

No exported code contract was involved. `xd://lsp` is unavailable (“No such tool”); text location is literal evidence, not semantic LSP proof. This audit checks the specified pinned local capture, not GitHub's live policy, adjacent entry assertions, or manifest provenance. No production files, git/jj state, tools, or PATH directories were modified. No scratch files/directories were created, so no scratch remains. No tools were installed.

Report: .ufo/waves/round-47/w1/R47ScoutEntrySpans.md
