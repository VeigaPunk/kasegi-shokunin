# R22 status and capability-placeholder history

Axes: **depth:verifiability** (commit-pinned text and provenance) and **coverage** (both requested historical surfaces). Inspection was read-only at repository HEAD `922a4dde90b60b465e2b8b241d1fe363f1f27e98`, matching the frozen round-23 base. No production/history files were changed; this report is the sole write. No tools were installed.

## Findings

### 1. R22 lesson line 5 is an initial filing, not the final adjudication

At `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md:5`, the committed text is: “**Status.** Claims declared, not measured; this file claims no score move and no verified-round credit.” `git blame HEAD -L 5,5 -- corpus/lessons/round-22.md` attributes that exact line to `c8b719d22882863ea7cd89b14c8bc078228001ed` (2026-10-19 19:27:48 -0300), the round-22 filing commit. The line remains unchanged at HEAD.

A subsequent, separate commit `13a51920068c48c0c5b3c8c81d5af0df6d4ea337` (2026-10-19 19:39:23 -0300; parent is `c8b719d...`) added `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22-verifier-spotcheck.md`. Its adjudication says C1 was `REJECTED-HONEST-STOP`: `resolve.py` and `anchorcheck.py` were unchanged and the score stayed at 4, so C1 did not move its axis; provenance/header work was not credited. It says C2 coverage was verified: five frontier entries admitted, map rows 25→33, `sources-registry` admitted with a 27-row census; it also records 5/5 spot-check agreement. The line is the filing-time declaration, not the latest adjudication; its “not measured” wording is broad relative to the same lesson's recorded gate evidence below and the later C2 verification. Its no-score/no-credit clause is consistent with the cited C1 result, but this does **not** establish an overall verified-round award.

The same R22 lesson's `## Gate` already records a 27-row census at lines 105–115 and five admitted entries at lines 125–131. This is further reason not to rewrite line 5 as though it were a claim that no work or measurements existed: preserve its filing-time context and append the later adjudication.

### 2. The old empty table row was not SCORECARD line 303

In `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md`, line 301 at HEAD contains the `sources-registry` capability row with first-working round `22`. Line 303 at HEAD is the separate sentence: “Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.” `git blame HEAD -L 299,304 -- SCORECARD.md` attributes lines 299–300 and 303 to `24cfce536192bf33020b9d985fe8291b1b5aed72` (2026-10-16), and the row at 301 to `c8b719d...` (2026-10-19).

The history resolves the apparent placeholder reference: commit `24cfce5` introduced a table row `| — none yet — | | | |` plus line 303's sentence during the protocol-conformance rollout. Commit `c8b719d` replaced the empty row with the round-22 `sources-registry` row but left line 303 unchanged. Therefore the placeholder was the **row at 301**, not the sentence at 303. The phrase “this rollout” originated in the earlier 24cf protocol-conformance change; do not treat it as saying the R22 capability was absent. This distinction is falsifiable by comparing `git show 24cfce5:SCORECARD.md` with `git show c8b719d:SCORECARD.md`.

The live worktree is dirty: `git diff HEAD -- SCORECARD.md` shows line 303 already replaced, without commit, by “The `sources-registry` capability entered in round 22; the preceding row replaces the rollout's empty repertoire placeholder. New rows require an exercised round demonstration (`AXES.md` §Capabilities).” That modified working-tree wording is not part of HEAD/history. It was not changed by this inspection. Other observed dirty entries were `corpus/QUALITY.md`, `.ufo/waves/`, `corpus/knowledge/multiparty-vulnerability-coordination.md`, and `corpus/source-snapshots/`; they were not inspected or modified.

## Append-only correction wording (proposed; not applied)

For `corpus/lessons/round-22.md`, append a new dated subsection rather than editing line 5:

> **Post-filing adjudication (2026-10-19; append-only).** The status above records the round author's filing at `c8b719d` (19:27:48 -0300). The later non-author verification, committed as `13a5192` (parent `c8b719d`), rejected C1 `depth:verifiability` because `resolve.py` and `anchorcheck.py` were unchanged and score 4 held; it verified C2 coverage (five frontier entries admitted, map rows 25→33, and `sources-registry` admitted with 27 rows). See `corpus/lessons/round-22-verifier-spotcheck.md`. This addendum supplements the filing and makes no broader verified-round-credit claim.

For `SCORECARD.md`, if a correction is needed, append a clarification instead of replacing its historical line:

> **Append-only capability-table clarification (2026-10-20).** The `— none yet —` capability row was introduced by the 2026-10-16 protocol-conformance rollout (`24cfce5`) and replaced by the R22 `sources-registry` row in `c8b719d` (first-working round 22). The sentence now at line 303 was introduced with that earlier rollout and was not changed when the row was replaced. This note clarifies the sequence; it does not rewrite the earlier sentence or either commit.

## Scope, falsifiability, confidence

The claim can be falsified by the cited commit contents/parents, line attribution, or worktree diff. Evidence chain used: `git show c8b719d:corpus/lessons/round-22.md`; `git show 13a5192:corpus/lessons/round-22-verifier-spotcheck.md`; `git show 24cfce5:SCORECARD.md`; `git show c8b719d:SCORECARD.md`; `git blame HEAD -L 5,5 -- corpus/lessons/round-22.md`; `git blame HEAD -L 299,304 -- SCORECARD.md`; and `git diff HEAD -- SCORECARD.md`.

Scope is limited to these committed records and the observed worktree delta. The verifier note itself summarizes its review; this inspection did not reopen its external fleet reports, re-run the R22 census, reevaluate source truth, or adjudicate a round-level score/award. Confidence: **high** for text, commit order, and placeholder-row lineage; **high** that line 303's wording predates and survived the R22 row replacement; **medium** for the intended semantic referent of “this rollout,” which is inferred from its 24cf protocol-conformance origin and chronology.