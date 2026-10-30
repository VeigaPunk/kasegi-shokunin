# R47W2AdmissionLanguage — integrated honest-stop review

Axes: **depth:verifiability** (claims versus evidence and authority); **coverage** (F02 enrichment versus independent F30 ground).

Reviewed integrated commit `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, with freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`. Scope: current-round LOG, lesson and corpus README language. Recommendation only, not admission or a canonical verdict.

## Findings by severity

**No actionable honest-stop language defect found in the scoped integrated blocks.** This is not a successful-claim finding: **C1's frozen target is not fully met and C2 is unmet.** Mechanical greens cannot reverse either conclusion.

- C1: `LOG.md:2037` explicitly says the retained mined S074 fails the frozen status transition and forbids representing a counter pass as full verification. `corpus/lessons/round-47.md:59,69` preserves that mismatch rather than rerolling the claim. The underlying witness is `.ufo/waves/round-47/w1/R47RevD7.md:9-17`: rejected S074 causes B3 `rejected-row-anchor`; its documented control changes from `records=3 bound=3 unbound=0 EXIT=0` to `records=3 bound=2 unbound=1 EXIT=1`. Those are peer-reported executions, not runs by this reviewer.
- C2: `LOG.md:2038`, `corpus/README.md:702`, and `corpus/lessons/round-47.md:60,65` consistently retain ZDI as F02 enrichment and reject the F30 count. The semantic reason is the existing owner/trigger/interval discipline, not an insufficient mechanical total: `.ufo/waves/round-47/w1/R47CritNovelty.md:7-23`. The frozen contract still demands 30 rows (`.ufo/waves/round-47/claims.json:37,44`); 29 is not silently relabeled success.

## Thirty-two static language challenges

These are distinct post-integration documentary challenges, **not executed mutations, tests, or proof of runtime saturation**. L = `corpus/lessons/round-47.md`; R = `corpus/README.md`; G = `LOG.md`.

| # | Attempted false inference | Integrated evidence blocking it |
|---|---|---|
| 1 | Eleven limbs alone establish semantic admission | L:3 explicitly denies it |
| 2 | C1 mechanical green overrides S074 status mismatch | G:2037; L:59 |
| 3 | Keeping S074 mined completes the frozen rejection | L:59,69 says target remains unmet |
| 4 | B3 may be relaxed to obtain green | L:59,69 retains mined historical binding instead |
| 5 | S076 retroactively reproduces S074's producing method | G:2038; round-46 correction:157 limits reproducibility |
| 6 | Historical S074 must be deleted for the repair | L:21,65 explicitly retains it |
| 7 | S074 remains the current-guidance source | R:700,702 supersedes it with S076 |
| 8 | Historical F29 row is an unqualified current provenance claim | R:702 explicitly marks it historical |
| 9 | New source numbering proves new frontier ground | L:33,60 rejects that inference |
| 10 | F02 enrichment achieves C2's F30 target | G:2038; L:60 |
| 11 | A new F30 row was admitted | R:702 explicitly denies it |
| 12 | The frontier grew to 30 | G:2038 explicitly retains 29 |
| 13 | Useful non-suppression facts substitute for frozen C2 | L:60 explicitly declines substitution |
| 14 | The old ZDI flip automatically licenses an independent frontier | L:33 separates procedure from coverage judgment |
| 15 | The prior F02 recommendation can be omitted | L:33,60 preserves its opposition |
| 16 | A lead reserves an already consumed source id | L:35 explicitly denies durable reservation |
| 17 | REST-API link presence means the page was opened | L:39,65 labels it unopened |
| 18 | The REST-API page is an admitted source | L:39 says not a source row |
| 19 | One GHSA is database-wide documentation | L:37 narrows S068 to one advisory |
| 20 | The ordinary 120-day interval has a known trigger | L:26 and R:699 retain unknown start |
| 21 | Faulty-patch 30 days is the ordinary deadline | L:28 expressly limits its tier |
| 22 | Extensions are automatic entitlements | L:27 denies that reading |
| 23 | Imminent fix permits immediate publication without a fix | L:31 says wait |
| 24 | Green 43-case selftest establishes full mutation coverage | L:13; G:2039 distinguishes them |
| 25 | Pre-freeze battery passed despite survivors | L:13 says exit 1 is not a pass |
| 26 | Uncaught mutants are equivalent | L:13,55 denies equivalence |
| 27 | Four further uncaught mutants erase the original 34 | L:55 explicitly preserves the original gaps |
| 28 | A broken receipt parser proves no divergent witnesses | L:55 identifies parser limitation and saved stdout |
| 29 | A moving working-tree reading replaces the frozen baseline | L:51 explicitly distinguishes them |
| 30 | Unbound staged captures are a green round-end gate | L:43 explicitly denies it |
| 31 | Lane source admission is independent closure/promotion | L:47,65 reserves independent closure |
| 32 | Repairs retroactively reverse round-46 rejected-harmed | R:702; round-46 correction:159 explicitly preserve it |

## Residual risk and verification gaps

- This finding is limited to truthful language, not independent certification of every substantive repair or all corpus facts. `G:2040` correctly leaves integrated measurements/report prospective. A later report must preserve the two failed frozen targets even if all mechanical gates are green.
- No saturation, full mutation coverage, score promotion, or independent final admission is established here. Existing `29/29 admitted` language at `R:693` is explicitly round-46 history; the current block adds no frontier count and does not settle C2 by arithmetic.
- `G:2036` wave settlement, round-wide tooling statements, and live capture claims were read as author statements; this seat did not independently census every wave seat, audit all installations, reopen external sources, or rerun captures.
- Runtime identity, same-identity rerouting, and `resume_continuity_v1` preflight mutation behavior are unchanged/not exercised by these scoped prose blocks. No runtime or resume-path certification is inferred.
- `read xd://lsp` returned `No such tool: xd://lsp`. Semantic references, definitions and diagnostics were unavailable. Used committed diff/show plus literal text inspection; these are not semantic caller proofs.

## Execution and custody

Executed only read-only `git diff <base> <integrated> -- LOG.md corpus/README.md corpus/lessons` and `git show <integrated>:corpus/lessons/round-47.md` for committed-content evidence, plus tool reads/searches. The committed diff supplied the scoped LOG/README additions; numbered file reads supplied their locators. Existing W1 receipts were inspected, not rerun. No counter, selftest, mutant battery, domain action, alternate runtime, judgment, build or service restart. No git/jj mutation, production edit, installation/update, or scratch creation; no scratch remains. Host rules and Godspeed skill read; pacman untouched. Only this report was written.

Self-evaluation: accuracy 4/5 (static review, attributed historical runs); completeness 4/5 (all three assigned surfaces covered, no independent execution); clarity 4/5 (32 challenges are explicitly documentary, not mutation receipts); actionability 4/5 (later final report must retain C1/C2 failure, but is not yet in scope); conciseness 4/5 (table retained to expose each challenge). Overall 4.0/5. Highest-value improvement is independent final-report comparison when that report exists. Expected user agreement: bounded final integrated-language review, not admission.

Report: .ufo/waves/round-47/w2/R47W2AdmissionLanguage.md
