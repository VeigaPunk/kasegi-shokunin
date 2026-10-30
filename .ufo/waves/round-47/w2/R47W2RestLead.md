# R47W2RestLead — integrated REST lead review

Axes: depth:verifiability; coverage. Static review of integrated commit `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; frozen claim identity `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Recommendation only, not admission.

## Findings, severity order

### Low — integrated lesson still names a different REST page than the Leads repair

`corpus/lessons/round-47.md:39` names `https://docs.github.com/en/rest/security-advisories/repository-security-advisories`, while the actual Leads bullet at `corpus/SOURCES.md:124` names `https://docs.github.com/en/rest/security-advisories/repository-advisories`. This is an exact path mismatch, not merely a different label for the concept-page URL. Both statements purport to identify the same unopened REST sibling.

The held evidence supports the sibling's **link text and purpose**: `corpus/source-snapshots/round-47/S076.txt:574` says “create, list, and update” and names “REST API endpoints for repository security advisories”; historical `corpus/source-snapshots/round-46-a2/S074.txt:16` says the same. Those text-only captures do not preserve its href. The selected concrete route `/repository-advisories` is explicit in the W1 lead repair (`.ufo/waves/round-47/w1/R47SrD5Diff.md:28,69`) and corrected lesson draft (`.ufo/waves/round-47/w1/R47SrLesson.draft/round-47.md:48`). W1's owner-reported pointer closure (`.ufo/waves/round-47/w1/R47SrLesson.md:49-51`; `R47RevD8.md:16-18`) therefore does **not** establish consistency of the final committed lesson. The integrated commit's actual lesson still uses the other route.

Recommended correction: align the current lesson's lead URL with `corpus/SOURCES.md:124`, retaining its unopened/no-row qualification. Do not rewrite historical captures or grant source-row/coverage credit. No claim is made here that the differing route returns 404 or cannot redirect: neither destination was fetched.

Static mechanical blind spot: `corpus/instruments/r47-routed-defects.py:300-309` only requires a Leads bullet containing `docs.github.com/en/rest/security-advisories`; it neither compares the lesson URL nor checks the full endpoint-page path. Thus an L10 green would not refute this finding. This is source inspection, not a newly executed counter result.

## Residual risk and verification gaps

- The real lead is correctly inside `## Leads (unopened)` (`corpus/SOURCES.md:119-124`), explicitly “not opened this round; lead, not row.” The Search log excludes it from screened sources (`:117`), and the lesson preserves unopened status (`corpus/lessons/round-47.md:39,65`). No API source-row credit is warranted or awarded.
- Exact historical href provenance cannot be independently recovered from S076's link-text-only line. The `/repository-advisories` route is corroborated by the recorded W1 repair, not by a fresh href extraction. A future authorized opening/capture must establish destination, redirects and body separately; this review performs no domain-target action.
- C1 remains not fully met and C2 remains unmet, as recorded at `corpus/lessons/round-47.md:59-60`; this scoped finding does not reroll either target. Runtime identity, rerouting, saturation and resume paths are outside this document-only leaf scope.
- Executed: read-only `git diff --stat`, `git diff --name-only`, scoped committed diff, and `git show` of committed SOURCES/lesson, plus anchored local document reads/searches. No application runtime, tests, selftests, gates or mutant battery executed. W1 receipts were read, not rerun.
- LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; status/references/definition/diagnostics could not be requested. Literal searches are discovery evidence, not semantic proof.
- No installs/updates, service restarts, delegation, git/jj mutations, production edits or scratch artifacts. Only this report was written.

Self-evaluation: accuracy 4/5 (exact committed mismatch established; destination href unverified); completeness 4/5 (bounded comparison complete, live URL intentionally unrun); clarity 4/5 (route versus link-text evidence separated); actionability 4/5 (one current lesson correction identified); conciseness 4/5 (provenance caveats retained). Overall 4.0/5. User-agreement check: no unopened page was promoted into a source.

Report: .ufo/waves/round-47/w2/R47W2RestLead.md
