# R47W2Manifest — final integrated static review

Axes: depth:verifiability; coverage.

Reviewed integrated revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, with freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Scope: both round-47 manifest records, capture metadata/body windows, all 22 quoted anchors, producing-method and determinism claims. Recommendation only; no admission, integration or judgment.

## Findings, by severity

### P2 — The declared prose-only S076 window still contains chrome

`corpus/source-snapshots/round-47/manifest.json:3` asserts that chrome, including TOC, lies outside `body_lines`; S076's declared window is 558–600 (`:92-95`). But `S076.txt:559` is “Copy markdown”, `:562` is “In this article”, and `:563-565` repeat the three TOC entries before the real section starts at `:566`. These are inside the window, not outside it. The window also excludes the page title at `:557`, unlike S075's heading-inclusive 20–27 window; the definite defect is the chrome-exclusion assertion, not the choice to include or exclude a title.

Impact: the metadata used to separate source prose from capture chrome does not meet its advertised invariant. `corpus/instruments/r47-routed-defects.py:141-148` consumes the window directly; L8 requires the exact 558–600 locator at `:255-258`. Thus a mechanical pass cannot establish prose-only membership. The legitimate quoted anchors themselves are unaffected.

Recommendation: preserve historical captures and frozen counters. Record the exception explicitly in current interpretation; do not represent this pinned window as chrome-free. A future independently scoped metadata repair can define prose spans without claiming the frozen predicate already checked them.

### P3 — Manifest still claims a new F30 despite the final F02-only decision

`corpus/source-snapshots/round-47/manifest.json:3` calls S075 “(new frontier row F30)”. The integrated lesson explicitly says C2 is unmet and no F30 is added (`corpus/lessons/round-47.md:60,65`); `corpus/SOURCES.md:175` also explicitly says F02 coordinator case, not admitted F30.

Impact: the final evidence bundle contains a stale affirmative coverage claim in its central manifest. Treat it as pre-decision historical wording, not evidence of achieved coverage. The safe decision not to manufacture a new frontier topic is correct; C2 remains unmet. Because L8 pins the complete manifest (`r47-routed-defects.py:259-266`), silently changing it would also change a frozen diagnostic's result. Disclose the contradiction rather than rerolling either claim or editing the historical manifest.

### P3 — Unqualified “deterministic” overstates the recorded repeat-capture evidence

`corpus/source-snapshots/round-47/manifest.json:3` says the superseding capture “is deterministic” and supports that with two same-instant matching digests. The saved receipt provides only the two first/second digest pairs and one capture timestamp per source (`.ufo/waves/round-47/controls/capture-determinism.txt:1-4`). This supports observed byte equality for those runs, not perpetual live-fetch reproducibility.

The canonical implementation explicitly disclaims that the host will serve the same bytes again (`corpus/instruments/capture-source.py:15-18`), performs a fresh request per capture (`:73-89`), then hashes the normalized bytes (`:90-97`). Its same-input normalization is deterministic by static inspection (`:39-53`); the live remote response is not pinned. The final lesson's narrower “Same-instrument second capture was byte-identical” (`corpus/lessons/round-47.md:20-21`) is the defensible formulation.

Recommendation: interpret this as two observed matching captures, not a guarantee about future page bytes or stable line numbers. No evidence was found that the named HTML method is false: leaked comment text and navigation are consistent with the actual tag-stripping implementation. Nor does the method claim prove the historical fetch independently occurred.

## Metadata and quoted-anchor coverage

Executed only read-only local byte inspection: `sha256sum` and `wc -lc`, with these results:

| Record | SHA-256 of committed text | Lines | Snapshot bytes | Manifest result |
|---|---|---:|---:|---|
| S075 | `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1` | 60 | 4701 | Matches `manifest.json:16,18-19` |
| S076 | `9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38` | 610 | 19804 | Matches `manifest.json:88,90-91` |

The manifest's `bytes` values 25321 and 582877 (`:17,89`) describe fetched response bytes, not snapshot lengths: the producer prints separate fetched/snapshot byte counts (`capture-source.py:95-96`). The difference is not itself a defect. Raw HTTP bodies are not present in these captures, so those fetched lengths were not independently re-derived.

All 22 manifest quotes were compared statically against their exact stored source lines, including untruncated long lines. Each is a literal substring of its claimed line and inside its declared window:

| Record | Quote anchors checked | Result |
|---|---|---|
| S075 | Q1→21; Q2→23; Q3/Q4/Q5/Q6→24; Q7/Q8/Q9→25; Q10→26 | 10/10 located; window 20–27 in bounds |
| S076 | Q1→568; Q2→571; Q3→575; Q4→582; Q5/Q6→583; Q7→584; Q8→589; Q9→596; Q10→598; Q11→599; Q12→600 | 12/12 located; window 558–600 in bounds |

Context checks: S075 Q7–Q9 belong only to faulty/incomplete-patch disclosures (`S075.txt:25`), not the ordinary 120-day case; Q2's fifteen-day action is conditional on exhausted contact efforts (`:23`); no explicit start event is added to the 120-day statement (`:24`). S076 Q9 is a substring, but the full source begins “Whenever possible” (`S076.txt:596`); the quote's literal correctness must not erase that qualification. Q10 is a wait-for-ready-fix case, not a third permission to publish without a fix (`:597-600`). These context boundaries were checked, not broadened into new entry-level findings outside this seat.

## Residual risk and verification gaps

- No network, source re-fetch, corpus runtime, selftest, mutation driver or alternate runtime was invoked. No future-fetch stability or independently observed HTTP status is claimed.
- URL/capture_url/final_url agree within each record (`manifest.json:7-11,79-83`), but the producer returns only response status, not the resolved URL (`capture-source.py:73-79,95-96`). Consequently a no-redirect assertion is not independently established by that producer's printed receipt. This is an evidence limitation, not proof the recorded URLs are wrong.
- `xd://lsp` was unavailable (“No such tool”); semantic references/definition/diagnostics could not run. Literal search and direct code inspection were used as fallback, not presented as LSP proof.
- Both captures and manifest were introduced at the freeze revision according to read-only scoped history; the integrated diff retains them. The findings therefore concern historical assertions surviving final integration, not rewritten source evidence.
- C1 remains not fully met because S074 stays mined historical to avoid B3 harm (`corpus/lessons/round-47.md:59,67-69`; canonical B3 `capture-binding-check.py:44-47`). C2 remains unmet (`round-47.md:60,65`). Neither is rerolled here.
- This bounded leaf review does not assert the aggregate milestone of 32 distinct attacks. It covers both records and all 22 quote anchors without padding one issue into multiple findings.

## Operations and self-evaluation

Only this report was written. No scratch, installs, updates, package transactions, service restarts, production edits, delegation, git/jj mutation, commit or push. Historical captures are unchanged. Read-only git diff/history and local hash/count inspection were executed; application verification is unrun.

Self-evaluation (not a gate): accuracy 4/5 (historical HTTP provenance remains unobserved); completeness 4/5 (all assigned records/anchors covered, live re-fetch forbidden); clarity 4/5 (historical-versus-current distinction adds necessary length); actionability 4/5 (frozen pin prevents a silent local correction); conciseness 4/5 (coverage table avoids repeating 22 quotes). Mean 4.0/5. Improvement priority: independent closure should preserve the distinction between hash equality, extraction determinism and remote stability. The user should agree that none is substituted for another.

Report: .ufo/waves/round-47/w2/R47W2Manifest.md
