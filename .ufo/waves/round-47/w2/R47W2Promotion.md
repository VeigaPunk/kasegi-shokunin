# R47W2Promotion — integrated held-score review

Axes: depth:verifiability and coverage; depth:density is the non-target guard.

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Static review only; this recommendation is not admission, scoring or promotion.

## Findings, by severity

No new promotion/self-attestation defect found in this bounded diff. Two already-disclosed claim failures remain blocking for any full-success wording; green mechanical gates cannot close them:

1. **Blocking claim failure — C1 remains short of its frozen target.** `corpus/lessons/round-47.md:59,67-69` retains S074 mined as historical evidence instead of executing the frozen rejected transition. `LOG.md:2037` explicitly says this does not fully verify C1. Preserve that honest distinction; do not repair this failure by rejecting S074 or weakening B3. This is an acknowledged unmet target, not a newly introduced implementation bug.
2. **Blocking claim failure — C2 remains unmet, without coverage expansion.** The frozen target requires 30 admitted frontier rows (`.ufo/waves/round-47/claims.json:37,44`); integration instead retains 29 and places ZDI under F02 (`LOG.md:2038`; `corpus/lessons/round-47.md:60,65`; `corpus/README.md:695-702`). Useful enrichment does not satisfy F30 novelty or justify an 8→9 score. No reroll is recommended.

## Promotion-limb attacks and retained invariants

- **Strict green does not mean score 5.** The existing prework receipt reads `strict pass=66/66`, `executes=44 gated=22 broken=0`, and exit 0 (`.ufo/waves/round-47/controls/recheck-audit-before.txt:1-5`). The explicit score-5 conjunction is zero gated rechecks **and** a non-author 25/25-chain audit with zero unsupported current claims (`SCORECARD.md:1536-1541`). Thus the receipt itself is a concrete counterexample to promoting on exit 0. The 22 remain operator-blocked; the lesson routes around the unanswered L0 question rather than claiming it resolved (`corpus/lessons/round-47.md:47`).
- **Diagnostic repair is not denominator repair.** Source-capture replacement and eleven routed-defect limbs cannot be substituted for the 22 gated rechecks or independent audit. The reporter explicitly asserts no score move and reports even when gates are red (`corpus/instruments/score-gap.py:10-14,32-38`). Its implementation parses the audit's own gated token (`:117-139`), not the new repair counter.
- **Held scores remain 4/8/9.** The base-to-integrated diff is empty for `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `density.py`, `score-gap.py` and `recheck-audit.py`. The retained result rows are `SCORECARD.md:1823-1825`. Appending a SKILL registry can change a density proxy without establishing craft depth; the new registry disclaims semantic authority and documents mutation limitations (`SKILL.md:1175-1186`). No density increase is credited here.
- **No new capability is admitted.** The unchanged scorecard says no capability row enters and distinguishes counters from capabilities (`SCORECARD.md:1834`). The added four instrument registry rows are diagnostics/selftests/battery, not a capability ledger. The ZDI entry is F02 enrichment, not independently new frontier ground.
- **No SHONEN self-promotion.** SHONEN is unchanged; all four latest evidence boxes remain `[~]` (`SHONEN.md:318-349`). The integrated lesson explicitly reserves independent closure and promotion outside the lane (`corpus/lessons/round-47.md:45-47,65`). Reusing the unlanded W1 SHONEN draft as if it were current integrated evidence would be incorrect; integration does not do so.
- **No manufactured saturation success.** The unchanged scorecard retains the 9/10, N=3 saturation declaration and identifies verifiability 4 as the lowest non-retired axis (`SCORECARD.md:1835-1838`). This revision neither crosses that line nor establishes a new saturation outcome. Coverage's operator half remains 0/18; no written 8→9 criterion exists (`SCORECARD.md:1788-1789`).

## Residual risk and verification gaps

- Final judged-head gated count, score-gap output, frontier rechecks, coverage denominator and density measurement are **unrun by this seat**. The 22-count receipt is prework evidence, not a fabricated final-head measurement. A main-owned final receipt should retain scores 4/8/9, explicitly distinguish the two score-5 limbs, and keep C1 incomplete/C2 unmet. `LOG.md:2040` already reserves final measurements/report; their absence here is not represented as a passed check.
- The integrated scorecard and SHONEN have no round-47 result append. Their unchanged historical state is not evidence of a new round-47 pass. No observed final 25-chain independent audit supports promotion.
- The milestone's 32 post-integration attacks is an orchestration-wide requirement, not a claim that this seat executed 32 attacks. This seat supplies bounded static counterexamples/invariant checks only.
- LSP device unavailable: reading `xd://lsp` returned `No such tool`. Consequently references/definition/diagnostics could not be obtained. Literal searches are navigation only, not semantic-reference proof. No cold empty result was treated as absence.
- Executed only read-only committed diff/show inspection and file/search tools. No canonical runtime, alternate runtime, domain action, counter, selftest, mutant battery, build, test or service restart was invoked. Runtime identity/rerouting and resume preflight are unaffected by the scoped documentation changes and were not exercised.
- No installs/updates, pacman transaction, git/jj mutation or production edits. No scratch created; none requires deletion. Only this scoped report was written.

Self-evaluation: accuracy 4/5 (final runtime readings deliberately unobserved); completeness 4/5 (bounded promotion review, not orchestration-wide attack census); clarity 4/5 (known target failures separated from new defects); actionability 4/5 (exact promotion conjunction and final-receipt limits identified); conciseness 4/5 (evidence qualifications add length). Overall 4.0/5. Highest-impact improvement belongs to main-owned final measurements, not an unauthorized reviewer runtime. User-agreement check: the requested held-score and self-promotion boundaries are preserved without rerolling either claim.

Report: .ufo/waves/round-47/w2/R47W2Promotion.md
