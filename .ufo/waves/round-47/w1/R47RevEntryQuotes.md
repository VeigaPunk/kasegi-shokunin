# R47RevEntryQuotes — F30 quote-location attack

Axes: **depth:verifiability**, **coverage**. Recommendation only; no admission or integration performed.

## Findings by severity

**No remaining actionable quote-location finding in the reviewed draft.**

**Resolved, medium — original citation syntax could not satisfy frozen H5.** The original draft table at `R47SrF30Entry.draft/zdi-disclosure-policy.md:11-20` placed bare backticked locators after all ten quotations. Frozen `corpus/instruments/r47-f30-gate.py:328-346` requires a literal opening parenthesis before each locator. Independent extraction located all ten quotations, but re-deriving the frozen syntax matched zero. The author wrapped all ten locators in parentheses after notification; the second audit matched ten. This was a grader-compatibility defect, not fabricated/unlocated source text. No production file was edited by this seat.

Reviewed final draft: `.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md`; SHA256 `f7c037c25196d68d7c58203b77245adf0d517a007f5a30e943b0e0b80c1cadfb`.

Source: `corpus/source-snapshots/round-47/S075.txt`; observed SHA256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`.

## Complete quotation inventory

All ten spans below are live table text, have immediately following parenthesized backticked citations, are whitespace/markup-normalized substrings of the cited source line, and use one-line spans inside body 20–27 (limit 12). All are at most 25 whitespace-separated words. No other quotation requiring citation was found, including inspection of the complete draft rather than only table rows.

| Draft line | Exact quoted span | S075.txt line | Words | Result |
|---|---|---|---|---|
| 11 | Simultaneous to the vendor notification, protection filters may be distributed | 22 | 10 | located/live |
| 12 | within five business days | 23 | 4 | located/live |
| 13 | an additional five business days following the second notification | 23 | 9 | located/live |
| 14 | fifteen business days after the initial contact | 23 | 7 | located/live/core |
| 15 | four months (120 days) to address the vulnerability | 24 | 8 | located/live/core |
| 16 | publish a limited advisory including mitigation | 24 | 6 | located/live/core |
| 17 | granted only in rare circumstances | 24 | 5 | located/live/core |
| 18 | active exploitation is detected or imminent | 25 | 6 | located/live/core |
| 19 | a disclosure window of 60 days | 25 | 6 | located/live |
| 20 | a time of 90 days | 25 | 5 | located/live |

Thus each of the five frozen cores (`r47-f30-gate.py:113-119`) occurs inside a located live quotation, not solely in analysis, a comment, or a fence. Failure spans: **none** after correction. Required uncited quotations ≥4 words: **zero**.

## Exercised evidence and controls

Reproduce the bounded, read-only independent extraction (no grader import):

`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-47/w1/R47RevEntryQuotes.draft/audit.py`

Printed on corrected draft:

```text
summary quoted=10 located_live=10 failures=0 uncited_required=0 cores=5/5 frozen_H5_syntax_matches=10
control fabricated_quote located=0
control wrong_anchor_25 located=0
control do_nothing_missing_entry located_spans=0 cores=0/5
```

The fabricated control appends ` fabricated words` to the exact core `four months (120 days) to address the vulnerability` and tests source line 24; the wrong-anchor control tests that unchanged core against line 25. Both fail location independently of marker presence. These are bounded in-memory controls, not the full frozen gate controls.

Do-nothing control: read-only command `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin cat-file -e fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/knowledge/zdi-disclosure-policy.md` exited **128**, printing that the path does not exist in the base commit. An absent entry supplies zero located spans and zero cores, unlike this draft. No base export or claim counter was run.

Original draft digest `49b7d8b631d1badfec28db4278945ecbce566a484433950055cb392bb7bac361` printed `quoted=10 located_live=10 failures=0 uncited_required=0 cores=5/5 frozen_H5_syntax_matches=0`; this distinguishes source fidelity from syntax acceptance.

## Residual risk and verification gaps

- This review verifies the pinned capture, not a live URL re-open or integrated-tree H2/H5 execution. The L1 must exercise the frozen gate on the integrated tree; no full-counter pass is claimed here.
- Novelty, branch paraphrase semantics, registry schema, and the other C1/C2 limbs are outside this quote-location seat. Concurrent author changes outside quotes were observed; findings bind the final digest above.
- Frozen claims disclose 16 C1 and 18 C2 mutation survivors; none is resolved by this bounded audit, and no full mutation battery was rerun.
- `read xd://lsp` returned `No such tool`; no LSP server/status device was available. Literal extraction and source inspection here are not semantic caller/definition proof.
- No tools installed, no commits/index mutations, no shared production writes, no heavy pass. Own scratch directory removed before return; retained audit script is an evidence artifact under this seat's permitted draft directory.

Self-evaluation: accuracy 4/5 (pinned text verified; live freshness outside scope), completeness 5/5 (all ten quotes and five cores audited), clarity 4/5 (two draft digests necessary to distinguish resolved syntax), actionability 5/5 (exact defect, repair, and runnable evidence), conciseness 4/5 (full inventory retained for reproducibility); mean 4.4/5. Highest-impact remaining verification is integrated-tree H5 plus the independent live re-open, not another location-only extraction.
