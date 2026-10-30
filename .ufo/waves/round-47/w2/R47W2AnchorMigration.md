# R47W2AnchorMigration — integrated line-anchor review

Axes: depth:verifiability; coverage. Static review of integrated `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Recommendation only, not admission or judgment.

## Findings by severity

### LOW — migration documentation still omits a usable current-locator inventory

`corpus/lessons/round-46.md:155` explicitly declares the migration and correctly makes old lesson locators historical, but names neither affected citing files nor replacement locators. The frozen instrument's documentary claim at `corpus/instruments/r47-routed-defects.py:39-42` says the round-47 lesson records the shift **and names the files whose anchors moved**; the integrated `corpus/lessons/round-47.md` does not contain that inventory. The named-owner inventory exists only in the proposal report `.ufo/waves/round-47/w1/R47SrD5Diff.md:128-132`, not the canonical lesson note. This is an incomplete documentation promise, not a failed D5 payload landing or an instruction to modify a frozen counter.

Concrete remaining misleading present-tense locator: `corpus/SOURCES.md:150` says the round-35 Search-log bullet is “now at :79”; `:151` repeats `:79`. In the integrated file `:79` is S073, while the CISA KEV Search-log bullet is `:105`. These strings predate round 47, so this is inherited drift, not a new regression. The adjacent correction at `:153` supplies a historical base for its own `:79`; it does not supply the current locator for the earlier “now” wording. The migration note only explicitly historicizes old locations in **lessons**, not these in-file references.

Suggested bounded repair by the integration owner: append a version-pinned inventory to the migration note, explicitly classifying these old “now” locators as historical and supplying current section/text identities. Do not rewrite historical receipts or frozen instruments. No production edit made here.

## Current claims versus historical receipts

- **No new broken live caller found in the literal inventory.** `SKILL.md:1079` cites `corpus/SOURCES.md:55-56` for S049/S050; both registry rows remain at those lines because S075/S076 were inserted after S074. No moved SOURCES line-number citation was found in current knowledge entries, README, PROVINCE, plans or instrument implementations. This is text-inventory evidence, not semantic-reference proof.
- `corpus/lessons/round-46-verifier-spotcheck.md:179-182` describes the old scaffold at approximately `:115-123` and `:176-185`. It is a pre-repair defect witness, not a current locator. Preserve it; the appended `round-46.md:155` correctly corrects its temporal interpretation.
- `corpus/lessons/round-29.md:277-284` includes “current pointer ... :90”, but `:267-269` and `:292-304` explicitly bind that correction and its “now” column to round-34 base `014ee2d`, dated 2026-10-26. Treat it as historical, not an instruction to look at current SOURCES line 90. Its intended S043 change cell is currently `corpus/SOURCES.md:133`.
- `corpus/lessons/round-29-verifier-spotcheck.md:74`, `round-31.md:107,147`, `round-33.md:93,130`, and `round-34.md:495-498` record the evolving historical `:83` drift trail. They are not additional current-proof failures. Do not re-anchor those receipts in place.
- `SCORECARD.md:1239,1397` cites historical Search-log/Registry-changes positions in dated round-34/35 measurements, not current source locations. Its S051/S052 registry-row anchors remain unchanged. No score/admission conclusion follows from this review.
- The F29 Search-log bullet now at `corpus/SOURCES.md:115` retains embedded `:74` and `:157` locators attached to export `04af9bc92229232ea5cce8b32bfe59dd969eb26d`. Those describe the historical absence sweep; the latter now resolves to an unrelated rejected-row change note, but is not asserted as a current locator. Preserve the evidence rather than rewriting the sweep.
- Wave-1 proposal offsets are generation-specific: `R47RevD5.md:23-25,40` and `R47SrD5Diff.md:126,131` describe a proposal where Leads was `:117`, Registry changes `:124`, S074 bullets `:170-171`. Final integration adds a round-47 Search-log bullet and now places them at `:119`, `:126`, `:172-173`. Proposal receipts are not final-tree proofs.

## Integrated locator receipt (static)

Locations below are from committed SOURCES bytes, not a runtime gate:

| Identity | Base fc8e0af | Integrated 65e19bd |
|---|---:|---:|
| S074 registry row | 80 | 80 |
| Paths heading | 82 | 84 |
| Search log heading | 91 | 93 |
| F28 Search-log bullet | 111 | 113 |
| F29 Search-log payload | 122 (fenced) | 115 (section bullet) |
| Leads heading | 125 | 119 |
| Registry changes heading | 131 | 126 |
| S043 old→new change cell | 138 | 133 |
| S074 registry-change payload | 183 (fenced) | 172 (section bullet) |
| Capture-directory payload | 184 (fenced) | 173 (section bullet) |

Offsets are nonuniform: the two new rows shift early sections by +2; scaffold deletion and the new Search-log/Lead additions change later offsets. A single global line delta would be wrong. Stable section names, source ids and quoted payload identities are preferable current navigation handles.

## Residual risk and verification gaps

- Executed: read-only `git diff` and `git show` for the assigned commits; literal grep and bounded file reads for citation consumers; report write. Committed SOURCES and the two lesson files were read directly with `git show`, so final-generation conclusions do not rely only on worktree state or wave-1 descriptions.
- `read xd://lsp` returned `No such tool`. Therefore no LSP status, references, definition or diagnostics service was available. Grep is the literal fallback only; it cannot establish a complete semantic citation graph.
- Runtime execution, counters, selftests, mutation batteries, live-source fetches and domain-target actions: **unrun**. No canonical runtime, routing, resume-continuity or saturation behavior is certified by this document-only slice. No claim of 32 executed attacks or complete mutation coverage.
- C1 remains not fully met (S074 stays mined historical to avoid B3 harm); C2 remains unmet (no F30; ZDI retained as F02 enrichment), as `corpus/lessons/round-47.md:59-67` explicitly records. Anchor cleanup does not reroll either claim or turn mechanical green into semantic admission.
- No tools installed or updated; host rules read first. No pacman transaction, service restart, git/jj mutation, delegation, production edit or scratch directory. Nothing remains to delete.

Self-evaluation: accuracy 4/5 (committed source evidence; semantic server unavailable); completeness 4/5 (all identified citation classes separated, not a semantic graph); clarity 4/5 (current versus historical distinguished explicitly); actionability 4/5 (one bounded append-only documentation remedy); conciseness 4/5 (inventory retained to make the review independently usable). Mean 4.0/5. Improvement priority: integrate a short version-pinned locator inventory rather than treating proposal offsets as final measurements.

Report: .ufo/waves/round-47/w2/R47W2AnchorMigration.md
