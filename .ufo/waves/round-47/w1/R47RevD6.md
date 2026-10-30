# R47RevD6 — corrected F29 sentence review

Axes: **depth:verifiability**, **coverage**. Scope: `corpus/instruments/entry29-fixed-bytes.md` against pinned `corpus/source-snapshots/round-47/S076.txt`, with the unchanged admitted `corpus/knowledge/github-repository-security-advisories.md` as do-nothing control. Recommendation only; no admission or integration.

## Findings, severity first

### Low — chrome example range includes the article's own section heading

`corpus/instruments/entry29-fixed-bytes.md:89` labels `S076.txt:562-566` page chrome. The capture has `In this article` at :562, TOC labels at :563-565, then a second `About repository security advisories` at :566 immediately before the article paragraph at :567 and definition at :568. [INFERENCE from captured ordering] :566 is the article section heading, not the TOC occurrence at :563. Thus this newly introduced range overstates chrome by one line. Recommend :562-565 instead; preserve the existing line count. The explicit `Copy markdown` example at draft :11 / source :559 is genuinely chrome and needs no change. The counter accepts the draft despite this distinction (receipt below).

## Correction-by-correction disposition

- **Chrome claim, draft :11 and :89:** the old assertion that the whole capture is prose is removed. S076 contains navigation before :558, `Copy markdown` at :559, TOC at :562-565 and footer at :601-610. Saying prose “spans” :558-600 does not say every intervening line is prose. The only identified new precision defect is :566 above. Source :556 is literally `In this article`, so that example is located too.
- **CVE-before-fix-version ordering, draft :16:** supported. CVE section heading is source :580, request mechanics :583, fix-version heading :595 and recommendation :596. Explicitly attributing the numbered ordering to the entry rather than the page corrects the old false attribution without adding a new sequence requirement in that sentence.
- **Two of three cases, draft :110-113:** supported as a conditional reading. Source :597 introduces the cases; :598 says `Imminently available, and you are able to, wait to disclose the issue when the fix is ready.` :599 expressly contemplates editing after publication; :600 contemplates no planned fix and mitigation. The word “forbids” must retain the quoted “and you are able to” qualification; it is not a universal prohibition for every imminently available fix. The draft includes that qualification, so no additional finding here.
- **New citation locations:** source :559 is exactly `Copy markdown`; :598 is exactly the sentence quoted above. Manifest `corpus/source-snapshots/round-47/manifest.json:143-146` also pins :598 as Q10. Both citations locate.
- **Line-count invariant:** satisfied for the reviewed bytes. `wc -l corpus/instruments/entry29-fixed-bytes.md corpus/knowledge/github-repository-security-advisories.md corpus/source-snapshots/round-47/S076.txt` printed respectively **145**, **145**, **610** (total 900). Python `splitlines()` independently printed `draft splitlines= 145 trailing_newline= True`.

## Bounded control receipt

Executed the frozen instrument's `l4`, `l5`, `l6` functions through Python import with bytecode writing disabled, substituting only `entry_text` in memory with each file's actual text. No fixture root, CLI, full battery, git operation or source-tree write was involved.

```text
Axes: depth:verifiability; coverage
Counter functions: L4/L5/L6 only; read-only entry_text injection, no fixture tree or counter CLI
do-nothing admitted entry [('l4', (False, 'false-phrases=2')), ('l5', (False, 'order-phrase-still-present')), ('l6', (False, 'two-cases-absent'))]
corrected draft [('l4', (True, 'prose-claims-corrected chrome=present')), ('l5', (True, 'order-claim-corrected')), ('l6', (True, 'fix-version-cases-corrected'))]
draft splitlines= 145 trailing_newline= True
S076 sha256= 9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38
located 559= 'Copy markdown'
located 598= 'Imminently available, and you are able to, wait to disclose the issue when the fix is ready.'
```

Counter definition evidence: `corpus/instruments/r47-routed-defects.py:190-223`. L4 requires absence of two old phrases and presence of `chrome`; it does not classify the cited lines. L5 checks the corrected ordering text. L6 checks `two cases` and the waiting quote. Therefore these passing limbs discriminate against the do-nothing control but do not prove sentence-level entailment or saturation.

## Residual risk and verification gaps

- Unchanged draft :139-140 still makes a fix version an unconditional conformance gate, in tension with its corrected :110-113 and source :596-600. This is inherited, not introduced by the three corrections. Likewise draft :79 still says neither service clock starts at publication despite source :594 describing review of each published advisory. These unchanged issues are not counted as new D6 regressions.
- The pinned plaintext establishes wording and ordering, not original HTML DOM roles. The :566 classification is explicitly marked inference; no live fetch or raw HTML was used. The capture digest printed above matches draft :3 and manifest :88.
- `read xd://lsp` returned `No such tool: xd://lsp`; semantic status/references/definition/diagnostics were unavailable. Review used literal source and diff evidence, not semantic-reference proof.
- Full counter CLI, full mutation battery, source-recheck CLI and integrated-tree checks were not run. Assignment-disclosed mutation survivors remain unresolved: C1 16, C2 18. No zero-survivor claim is made.
- No tools installed. No scratch files/directories created, so no scratch remains. Only this scoped report was written; production files were unchanged.

Self-evaluation: accuracy 4/5 (heading role inferred without DOM); completeness 4/5 (bounded D6 review, not integrated-tree verification); clarity 5/5 (each requested correction and citation has a disposition); actionability 5/5 (one-line range correction identified); conciseness 4/5 (retains receipts and inherited-risk distinctions). Overall 4.4/5. Highest-impact improvement is DOM-backed heading confirmation if original HTML becomes available; the present inference is not presented as DOM proof.

Report: .ufo/waves/round-47/w1/R47RevD6.md
