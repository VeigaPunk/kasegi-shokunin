# R47CritSever — causal separability audit

Axes: **depth:verifiability; coverage**. Static critic findings, not a judgment, admission or integration.

## Result and evidence boundary

**No landing-dependence leak is established by the inspected predicates.** The two claimed deltas are mechanically separable with the frozen captures/manifest held as shared substrate. The strongest local counterexample is instead **false admission provenance in the stock C1-only fixture lesson**. There is also a shared whole-manifest integrity dependency, which must not be confused with independent source provenance.

Constructed both cross-check recipes and the complete predicted limb matrix in `R47CritSever.draft/crosschecks.md`. No fixture tree or runtime was invoked: the canonical critic role forbids invoking another runtime. Thus cross-counter execution is **unrun**, not a pass. Existing positive/control receipts are cited below as existing evidence, never as this seat's new measurements. Current working-tree state was not substituted for historical base/freeze.

All instrument paths below are relative to `corpus/instruments/` unless expanded.

## (a) Only C2 landed

Construction: historical base plus precisely the S075 registry row, F30 README row and F30 entry, with the frozen round-47 captures/manifest available. `r47-counters-selftest.py:320-342` already builds this synthetic tree without D5-D8 edits. It adds S075 using `add_registry_row`, not `land_bullets`; the former inserts after the last registry row (:127-136), while scaffold removal/landing is a distinct operation (:79-102).

**[INFERENCE] C1 remains 0/11; all L1-L11 stay red:**

- L1/L2: the four scaffold phrase types and four fences remain; the three fenced bullets are not landed. C1 predicate evidence: `r47-routed-defects.py:153-173`.
- L3: no round-46 Corrections section (:176-183).
- L4/L5/L6: F29's false prose/order/two-case assertions are unchanged (:190-223).
- L7: neither lesson receives the dropped-findings names (:226-231).
- L8: no S076 registry row (:234-267). Providing S076's frozen capture alone does not satisfy the row predicate.
- L9: F29 retains its 59 S074 citation instances, causing the early red return (:270-297).
- L10: no REST-API lead is added (:300-309).
- L11: no round-47 lesson is added (:312-318).

**[INFERENCE] C2 reaches 7/7 without C1:** existing peer receipt `.ufo/waves/round-47/w1/R47ExecSelftestReplay-selftest.txt:21` records the synthetic c2-green fixture at 7/7. The construction above is explicitly independent of C1's builder; this supports the forward grade but does not constitute a newly run reverse-counter check.

### H6 does not force C1

`r47-f30-gate.py:350-370` checks 67 entries, all 66 historical names, and historical content except the declared exemptions. `EXEMPT_CONTENT` names F29 and the ledger (:99 in the inspected source definition; the exemption contract is also explicitly documented at :53-62). F29's original bytes and its C1-corrected bytes are both permitted. C1 changes F29 in place, not the directory inventory (`r47-counters-selftest.py:220`). No round-47 lesson belongs under knowledge. Thus C2 alone supplies the 67th entry; C1 is not required to satisfy H6.

### H7 accepts the existing scaffold; H3 does not require 76 rows

H7 requires exactly one Registry heading and a successful census over the supplied SOURCES path (`r47-f30-gate.py:373-382`), not scaffold removal, S076, or a registry-row count of 76. H3 checks the one S075 row and its linked entry/capture (:261-293), not S076 or C1 lesson content. C2 alone has 75 registry rows; integrated round has 76. Neither H3 nor H7 demands the integrated count.

Fleet census evidence: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:608-624` processes level-two headings and pipe rows, skipping other lines. The existing scaffold comprises prose, fences and bullets, not new source rows. Its path validator checks mined registry rows only (:538-570). The new S075 used-by path exists in the C2 fixture; there is no need for the C1 fixes to make it exist. Warning-only duplicate URLs do not produce a failed census (:638-649,737-745).

Most decisively, the unchanged historical SOURCES scaffold already has observed H7 green in `.ufo/waves/round-47/controls/c2-base.txt:7`. The scaffold is a rendering/provenance defect that this census does not reject; it is not evidence of C1 closure.

## (b) Only C1 landed

Construction: `r47-counters-selftest.py:212-228` supplies only D5-D8 edits plus shared frozen captures. It never adds the F30 entry or README row or S075 registry row. Existing peer receipt `R47ExecSelftestReplay-selftest.txt:1` records its own C1 positive grade as 11/11; this is a synthetic fixture, not production closure.

**[INFERENCE] C2 stays 2/7, exit 1:** H1 red (29 frontier rows; :193-217); H2 red (entry absent; :220-223); H3 red (S075 registry row absent; :261-270); H5 and H6 red (entry absent; :321-324,350-357). H4 remains green because the frozen S075 capture/manifest are present (:296-318); H7 remains green because C1's valid registry edits neither add a duplicate Registry heading nor create a missing mined used-by target (:373-382). Removing the scaffold is not a census requirement. Adding S076 is compatible with the census's supersession/duplicate rules, cited above.

C1's own predicates do not read F30's README row or its new entry. Its only new registry-row predicate names S076, not S075 (:234-267); its reference to ZDI is a lesson-text predicate, not a requirement to admit C2 (:312-318).

## Strongest counterexamples and smallest safe corrections

1. **False provenance in the C1-only positive fixture.** The builder writes `LESSON47_STUB` (:222), whose text says the ZDI reservation is resolved by 'this round's admission' and 'ZDI is admitted as F30 with S075' (`r47-counters-selftest.py:195-196`). Yet that builder does not create F30 or its entry. A C1-green fixture therefore need not be truthful about C2 admission. Impact: **depth:verifiability**, with **coverage** overstatement if copied into a report. Smallest safe correction: in the C1-only counterfactual state that ZDI's S075/F30 reservation is held for the separate C2 proposal and that C1 alone makes no admission. L11's literal predicate still holds without asserting admission. Do not copy this synthetic lesson into production as historical evidence. This is a fixable fixture/provenance defect, not evidence that C1 mechanically needs C2.

2. **Shared whole-manifest pin.** C1 L8 pins the entire manifest (`r47-routed-defects.py:259-266`); C2 H4 also pins the entire manifest (`r47-f30-gate.py:296-306`). The builders copy manifest plus BOTH captures in both trees (`r47-counters-selftest.py:223-227,337-341`). A purported only-C1 fixture that deletes S075's manifest record can make L8 red despite no C1 prose/registry regression; symmetrically deleting S076's manifest record breaks C2 H4. Impact: **depth:verifiability; coverage attribution**. Smallest safe correction: name and preserve the full frozen capture package as common substrate in both cross-checks; do not claim source-package independence or mutate the frozen pin. This shared freeze dependency is not a demonstrated landing-delta leak, because neither claim's landing changes that manifest.

## Controls, limits and hygiene

Named do-nothing control: historical base export `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; existing control C2 is 1/7 with only H7 green (`controls/c2-base.txt:1-9`). The assignment's unchanged-freeze control is C1 0/11 and C2 2/7 (shared capture H4 is already present). Do not call a synthetic positive tree a do-nothing control. Predicted only-C1 and only-C2 reverse grades remain unrun and require an authorized executor/L1, using the recipes and explicit scratch paths.

This audit establishes static dependencies, not live-source freshness, semantic novelty, actual production closure, full mutation sensitivity, or canonical admission. Known battery limits remain C1 16 and C2 18 uncaught mutants, 34 total; no battery was run and no survivor was called equivalent.

Only this report and own draft recipe were written. No scratch directory or clone was created, so none remains to remove. No git/jj mutation, delegation, production write, PATH write, installation or host change occurred. The required disk-status command printed /fast/scratch/hyaku 376.2G free, /tmp 96.7G, /var/tmp 532.8G; its consumer-list phase timed out at 30s and the harness automatically backgrounded that synchronous call. No background work was deliberately requested.

Self-evaluation: accuracy 4/5 (predictions are distinguished from executions); completeness 3/5 (role forbids requested runtime cross-probes); clarity 4/5 (shared substrate versus landing delta explicit); actionability 4/5 (both exact builder recipes and corrections supplied); conciseness 4/5 (limb-specific evidence retained). Overall 3.8/5. Highest-impact completion step for the authorized executor is recording the two reverse-counter outputs, not another full battery.

Report: .ufo/waves/round-47/w1/R47CritSever.md
