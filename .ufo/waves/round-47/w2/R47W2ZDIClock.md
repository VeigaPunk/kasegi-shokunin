# R47W2ZDIClock — integrated clock-policy review

Axes: **depth:verifiability**, **coverage**. Recommendation only; no admission, integration, or judgment.

Reviewed revision `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; frozen claim identity `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Scope: the 120-day unknown-start inference, permissive 15-business-day fallback, conditional limited advisory, and extension discretion.

## Findings by severity

**No actionable defect found in the integrated clock guidance.** The new entry distinguishes a branch-selection event from a stated clock origin, preserves the fallback's permission and exhausted-contact condition, and retains the limited-advisory conditions and sole-discretion rare extensions. This is a static semantic conclusion, not a counter pass or an execution result.

**Frozen claim failures remain, not rerolled:** C1 is not fully met because rejecting S074 would break B3; C2 is unmet because ZDI remains F02 enrichment with no F30 row. These dispositions are explicit at `corpus/lessons/round-47.md:57-69` and `corpus/README.md:699-702`. Correct clock prose does not establish independent coverage or erase either failure. No mechanical green would change that conclusion.

## Evidence and 32 distinct static attacks

Abbreviations: **E** = `corpus/knowledge/zdi-disclosure-policy.md`; **S** = committed `corpus/source-snapshots/round-47/S075.txt`; **F02** = `corpus/knowledge/coordinated-disclosure-timelines.md`. Every row below is a manually reviewed counterexample hypothesis against the post-integration text, **not an executed mutant/test**. “Blocked” means the text explicitly rules out that interpretation; no runtime enforcement is claimed.

| # | Counterexample hypothesis | Static disposition and evidence |
|---|---|---|
| 1 | Acquisition starts the 120 days. | Blocked: E:9,36 reject acquisition as an inferred origin; S:24 names no acquisition event. |
| 2 | Initial contact necessarily starts the 120 days. | Blocked: E:9 explicitly refuses first contact; S:23's explicit initial-contact origin belongs to the separate fallback. |
| 3 | Acknowledgement necessarily starts the 120 days. | Blocked: E:9 explicitly refuses acknowledgement as an inferred origin. |
| 4 | Receipt of a timely response is an explicitly stated 120-day origin. | Blocked: E:9 distinguishes selecting the branch from identifying the interval's start; S:24 supplies the condition but no explicit start-date clause. |
| 5 | No start event means the source states no interval. | Blocked: E:17 retains “four months (120 days)” while preserving unknown origin. |
| 6 | Unknown origin means a guessed date can be reported as observed. | Blocked: E:36 rejects a computed date solely from this page when the required origin is unstated; F02:9,16 retain unknown dates. |
| 7 | The entry rejects independently evidenced origins too. | Blocked: E:36 expressly allows the start event to be separately evidenced. |
| 8 | Every acquired finding receives the ordinary 120-day branch. | Blocked: E:9 conditions it on timely response; E:36 rejects the universal acquired-finding formulation. |
| 9 | Four calendar months can silently replace the source's parenthetical 120 days. | Blocked: E:17 requires preserving both stated units rather than selecting a derived calendar convention. |
| 10 | The 120-day allowance is the vendor's own disclosure policy. | Blocked: E:9 attributes the rule to TrendAI ZDI and distinguishes vendor-owned policy. |
| 11 | The allowance is a universal researcher deadline. | Blocked: E:9; F02:8. |
| 12 | The fallback mandates publication at fifteen business days. | Blocked: E:16 says possible; E:24 explicitly says permissive, not an automatic promise; S:23 says may. |
| 13 | Fifteen calendar days is interchangeable with fifteen business days. | Blocked: E:16,24 retain business-day units; E:36 requires preserving units. |
| 14 | The fallback begins at the second notification. | Blocked: E:16 quotes initial contact, matching S:23. |
| 15 | The fallback begins at intermediary involvement. | Blocked: E:16 retains initial contact; E:15 reserves the second-notification reference for intermediary escalation. |
| 16 | Fifteen business days alone authorizes the fallback even if reasonable contact means remain. | Blocked: E:16 requires exhausted reasonable contact means; S:23 makes exhaustion conditional. |
| 17 | Initial silence permits skipping the second-contact threshold in the documented sequence. | Blocked as a description of the policy: E:14 records the five-business-day acknowledgement threshold before the second attempt; S:23 states that sequence. |
| 18 | Intermediary escalation's additional five days run from the first contact. | Blocked: E:15 preserves the second notification as reference, matching S:23. |
| 19 | The two five-day thresholds establish a precise 120-day origin. | Blocked: E:9 and E:36 keep that origin unknown despite selecting the response branch. |
| 20 | Every applicable 120-day deadline guarantees limited-advisory publication. | Blocked: E:18,24 preserve the nonresponse or inadequate-explanation condition from S:24. |
| 21 | Publication requires both nonresponse and an inadequate explanation. | Blocked: E:24 preserves the source's disjunction, “or,” rather than requiring both. |
| 22 | Continued responsiveness alone necessarily defeats publication regardless of explanation. | Blocked: E:24 retains inability to provide a reasonable explanation as the alternative condition. |
| 23 | An unfixed issue alone necessarily triggers publication even with a reasonable explanation. | Blocked: E:18,24 preserve the explanation condition instead of equating unfixed with unconditional publication. |
| 24 | The promised advisory is full exploit disclosure. | Blocked: E:18 retains limited advisory including mitigation; S:24 does not promise a full exploit advisory. |
| 25 | The fallback public advisory and the limited deadline advisory have identical triggers. | Blocked: E:16 versus E:18,24 keep exhausted-contact permission separate from the ordinary deadline consequence. |
| 26 | Customer protection filters establish a public-advisory date. | Blocked: E:13 separates possible customer protection from public disclosure, matching S:22. |
| 27 | A vendor can unilaterally claim an extension. | Blocked: E:19,24 identify ZDI's sole discretion and deny vendor entitlement; S:24 is explicit. |
| 28 | Every reasonable explanation automatically grants an extension. | Blocked: E:19 denies entitlement and E:24 retains sole discretion; S:24 does not equate explanation with an awarded extension. |
| 29 | Extensions are routine. | Blocked: E:19 quotes rare circumstances; S:24 restricts them to rare circumstances. |
| 30 | The extension has a source-prescribed fixed duration. | Unsupported by source and not asserted by entry: S:24 supplies discretion and rarity, no extension length; E:19,24 invent none. |
| 31 | Granting an extension establishes a formerly unknown clock origin. | Blocked: E:9,17,36 preserve the unknown origin independently of E:19's extension authority. |
| 32 | Vendor refusal to address an acquired finding proves publication exactly 120 days after acquisition. | Blocked: E:24 retains nonsuppression without asserting that date; E:36 explicitly rejects that over-generalization; S:26 gives the disposition, not a date. |

The key inference in rows 1–7 is deliberately narrow: the page does not **explicitly name** a start event for the ordinary interval. It does not establish that ZDI has no internal start convention, that no contextual reading is possible, or that independently evidenced correspondence could never supply an origin. E:9,36 make precisely that distinction.

## Actual diff, definitions, and consumer checks

Executed only read-only inspection commands: `git diff --stat <base> <revision>`, `git diff <base> <revision> -- corpus/knowledge/zdi-disclosure-policy.md corpus/knowledge/coordinated-disclosure-timelines.md`, `git show <revision>:corpus/source-snapshots/round-47/S075.txt`, and the scoped committed diff for `corpus/README.md`, `corpus/SOURCES.md`, and `corpus/lessons/round-47.md`. The entry is new in this diff; F02's underlying rule is unchanged. Complete long source sentences S:24–26 were read from the untruncated committed-command artifact, including the final sole-discretion/rare-circumstances sentence.

Consumer checks used literal search in SKILL.md, corpus README, SOURCES, and QUALITY after semantic tooling proved unavailable. Current README:699 describes conditional clocks and an unknown origin, not an admitted frontier; SOURCES:81 locates the conditional ordinary window, extensions, contact sequence, and faulty-patch branches; SOURCES:175 identifies F02 enrichment. E:28 links back to F02:6–17, whose unknown-trigger and condition-separation requirements were read directly. The frozen counter fixtures contain older proposed F30 phrasing; the lesson:61 explicitly retains counters as frozen diagnostic evidence, not current semantic authority. Those historical predicates were not used to override the integrated entry.

`read xd://lsp` returned **No such tool: xd://lsp**. Thus status, references, definition, and diagnostics could not be requested from a mounted server; literal searches are not semantic-reference proof. No empty cold-index result was treated as absence.

## Residual risk and verification gaps

- All 32 attacks above are **static review scenarios**. Runtime, selftests, gate replay, full mutation battery, live reopens, or domain-target actions were **unrun**. No saturation or mutation-kill-rate claim is made.
- No business-day holiday calendar, timezone, exact date arithmetic convention, extension duration, or negotiated start is supplied by this source. The entry correctly avoids manufacturing them; a real dated package would require independent evidence.
- This bounded policy addition changes no runtime, same-identity rerouting, or resume path. No `resume_continuity_v1` execution/preflight guarantee is asserted by this review.
- Earlier W1 quote-location and claim-shape reviews were read as historical evidence (`R47RevEntryQuotes.md:7–9,55–60`; `R47RevEntryQ.md:13–17,24–28`), not promoted into integrated execution evidence. Their “vendor clock” ambiguity is resolved by E:9's distinction between a ZDI-set vendor allowance and the vendor's own policy.
- No tools installed/updated, package transactions, service operations, production edits, git/jj mutations, or scratch files/directories. Only this seat report was written; no scratch cleanup was necessary.

Self-evaluation: accuracy 4/5 (committed source supports findings; no live freshness evidence); completeness 4/5 (32 scoped static hypotheses, no executable enforcement evidence by role); clarity 4/5 (evidence abbreviations require the key); actionability 4/5 (no repair requested, gaps separated from defects); conciseness 4/5 (full attack inventory retained for verifiability). Mean 4.0/5. Highest-impact additional evidence would be independently sourced clock-start correspondence for any actual dated claim, not another mechanical gate. The user should regard this as bounded static review only.

Report: .ufo/waves/round-47/w2/R47W2ZDIClock.md
