# R47RevRow — registry/schema review

Axes: **depth:verifiability; coverage**. Recommendation only; no admission, integration or production edit.

## Findings by severity

### P2 — frozen H3 does not enforce its documented Registry/body boundary

`corpus/instruments/r47-f30-gate.py:264-268` searches all live source-file lines, not the `## Registry` section. Its locator predicate at :283-285 permits `20 <= start <= end <= 60`, rather than requiring the locator inside policy body 20-27. Consequently a chrome-only `lines 28-60 of corpus/source-snapshots/round-47/S075.txt` anchor also passes. The contract documentation at :38-42 promises Registry-only placement and body-bound location; manifest `corpus/source-snapshots/round-47/manifest.json:20-23` establishes that body range.

Bounded execution of the unchanged canonical `h3()` against its frozen positive-fixture row (`corpus/instruments/r47-counters-selftest.py:105-113`) printed:

```text
do-nothing: false, row-S075=absent-or-malformed-or-not-registry-only hits=0
positive-row: true, row-S075=ok
outside-registry: true, row-S075=ok
out-of-body-end (20-60): true, row-S075=ok
chrome-only-range (28-60): true, row-S075=ok
```

Receipt: `.ufo/waves/round-47/w1/R47RevRow.draft/boundary-receipt.json`. Fixtures used the same pinned capture and an explicitly H3-only entry-existence sentinel, not a fabricated claim of entry acceptance. These are H3 false positives, **not evidence that the whole seven-limb gate accepts these trees**. Do not change frozen predicates silently; independent placement/body review remains necessary. The reviewed amended draft itself avoids both holes.

### Resolved before handoff — initial row lacked H3's literal locator binding

Initial `R47SrRegistry.md:19` read `... body lines 20-27; ...`, with the capture path earlier in the anchor. The regex requires `lines N-M of <capture-path>` in that order (`r47-f30-gate.py:283-286`). Reported to the owner; owner amended the row to start its anchor `lines 20-27 of corpus/source-snapshots/round-47/S075.txt`. The subsequently exercised row passes H3. No unresolved defect found in amended blocks A-C within this seat's scope.

## Exact H3/schema cross-check of amended block A

Reviewed `.ufo/waves/round-47/w1/R47SrRegistry.md:19`; exercised row SHA256 `856af2bfc7dcb8efc3d21bd23c2dd0e3200eafa681c1406604f32876087a7af5`.

| Predicate | Observed |
|---|---|
| Unique S075 row, eleven cells | 11 cells; 12 delimiters; no literal/escaped pipe inside any cell |
| kind/tier/status | `docs` / `A` / `mined`, matching exact H3 and census enums |
| opened / recheck | `2026-10-30` / `90d`; exact H3 date and cadence regex |
| scope / teaches word minima | 23 / 20 regex words, each >=8 |
| source URL | Exactly one URL: `https://www.zerodayinitiative.com/advisories/disclosure_policy/`; therefore first and every URL canonical, no redirector |
| anchor | Literal `lines 20-27 of corpus/source-snapshots/round-47/S075.txt`; full pinned SHA256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1` |
| used-by | Exact `corpus/knowledge/zdi-disclosure-policy.md` |
| actual H3 result | `(True, 'row-S075=ok')` |

Note the executable is stricter than its prose on URLs: :289-290 rejects **any** noncanonical URL in the source cell, not only a noncanonical first URL. The amended row satisfies both readings. Definitions/call behavior were inspected textually because `read xd://lsp` returned `No such tool`; no semantic LSP server/status/references/diagnostics device is mounted. Text search is not presented as semantic proof.

## Census, bullets and do-nothing discrimination

Executed the real fleet census read-only over a scratch copy of the current 74-row SOURCES plus block A inserted under Registry (the stated :9 position), copied existing knowledge files, and the explicitly labelled entry-path sentinel:

```text
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-30 --file /fast/scratch/hyaku/kasegi-r47/R47RevRow/draft/corpus/SOURCES.md
exit=0
W04 S028 duplicate url ... across scopes
W04 S029 duplicate url ... across scopes
W04 S072 duplicate url ... across scopes
file ok /fast/scratch/hyaku/kasegi-r47/R47RevRow/draft/corpus/SOURCES.md
```

Exact output, command, row and snapshot hashes: `.ufo/waves/round-47/w1/R47RevRow.draft/draft-receipt.json`. Census parser evidence: `scripts/sources-census.sh:635-666` schema/date/enums; :538-568 used-by existence; :619-621 rejects out-of-Registry source rows. This verifies row integration/schema only, not real F30 entry content.

Block B (`R47SrRegistry.md:25`) attributes 74→75 to S075 and 75→76 to C1's S076, correctly separating the two additions (`claims.json:45`; base measured registry rows=74). Its date/access/digest/60 lines/4701 snapshot bytes agree with manifest :6-23; its grounding quote text agrees with Q10 :71-73 and capture line 26. The original label incorrectly said 23 words: the quote has 20 whitespace words; owner reported correcting that label before handoff. The lesson-record assertion is explicitly integration-dependent at draft :80, not an exercised fact here.

Block C (:31) labels shell forms as unexecuted reproducible equivalents, not fabricated execution receipts. Independent bounded regex searches over knowledge, SOURCES and README found no matches for the combined broad/policy-text terms; `ZDI` found only `corpus/SOURCES.md:170` (the round-43 advisory-index sweep). This supports the stated search census, not semantic novelty or exhaustive absence. Search-log regex alternation pipes are prose, not cells of the registry row.

Do-nothing discriminator: own isolated absent-row control returns H3 false while amended block A returns true. Inherited `.ufo/waves/round-47/controls/c2-base.txt:1-9` records full base `fixed=1/7 exit=1`, H3 absent and H7 already passing: a green census alone cannot distinguish this admission from doing nothing. The full counter was not rerun.

## Residual risk and verification gaps

- Integrator must land A under Registry, B under Registry changes, C under Search log outside the D5 fences; placement instructions at draft :9-14 are correct but unapplied.
- Real entry existence/content, lesson Gate quote landing, 67-entry census, full integrated gate and live-page/overlap closure are not established by the sentinel fixture. No 7/7 claim.
- Disclosed mutation survivors remain C1 16 and C2 18; no full battery rerun or saturation/equivalence claim. The supplied 43-case pass is inherited evidence only.
- Disk guard printed `/fast/scratch/hyaku` free **374.8G**, then timed out during top-consumer enumeration; no heavy pass or ENOSPC occurred. All seat scratch removed by Python `finally: shutil.rmtree(...)`; receipts retained only in the seat draft directory. No tools installed; no git/jj mutation, background work, delegation, runtime switching or production writes.

Self-evaluation (1–5): accuracy 4, completeness 4 (bounded schema review, not integrated admission); clarity 4, actionability 4, conciseness 4 (retained exact predicate/fixture limitations). Overall 4.0. Improvement priority: integrated entry/section checks by L1; retain independent body-placement check despite H3 green. Would the user agree: evidence is bounded and explicitly non-admitting.

Report: .ufo/waves/round-47/w1/R47RevRow.md
