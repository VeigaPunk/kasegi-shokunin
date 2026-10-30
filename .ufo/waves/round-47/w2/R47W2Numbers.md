# R47W2Numbers — committed-byte numeric ledger

Axes: **depth:verifiability**, **coverage**. Static final integrated review only; no admission, promotion, integration, or runtime verdict.

## Evidence and method

Base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; integrated `65e19bdb142c90a08103eb4b2af60c71218a920e`; freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`.

Executed read-only `git show REV:PATH` and `git ls-tree -r --name-only REV -- corpus/knowledge`; counted their returned committed bytes in memory. No checkout filesystem supplied the numbers. Receipt: `.ufo/waves/round-47/w2/R47W2Numbers.receipt.json` (definitions, input SHA-256 digests, counts, policy-sweep paths, role cross-check). No scratch directory or export was needed or created; no wave history exported.

Definitions retained from frozen `.ufo/waves/round-47/claims.json:20-26,44-47` and `.ufo/waves/round-47/w1/R47SrPlain.draft/r47-plain-measure.sh:111-131`: frontier `^\| F[0-9]+ \|`; sources `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|`; immediate `corpus/knowledge/*.md` files. Literal matching-line counts remain distinct from literal occurrence counts. Entry length is LF-byte count (`wc -l` definition), not display wrapping.

## Base → integrated

| Quantity | Base | Integrated | Delta |
|---|---:|---:|---:|
| Frontier rows | 29 | 29 | 0 |
| SOURCES registry rows | 74 | 76 | +2 |
| Knowledge files | 66 | 67 | +1 |
| F29 entry LF lines | 145 | 145 | 0 |
| F29 entry lines containing `S074.txt:` | 54 | 0 | −54 |
| F29 entry occurrences of `S074.txt:` | 59 | 0 | −59 |
| F29 entry lines containing `S076.txt:` | 0 | 54 | +54 |
| F29 entry occurrences of `S076.txt:` | 0 | 67 | +67 |
| SOURCES lines containing `to append` | 2 | 0 | −2 |
| SOURCES lines containing triple backticks | 4 | 0 | −4 |
| Entry lines containing `all 42 lines are body prose` | 1 | 0 | −1 |
| Entry lines containing `three cases` (contextual only) | 2 | 1 | −1 |
| SOURCES lines containing `supersedes S074` | 0 | 2 | +2 |
| SOURCES lines containing `docs.github.com/en/rest/security-advisories` | 0 | 1 | +1 |
| Files matching case-insensitive `zero day initiative|zerodayinitiative` over knowledge, SOURCES, README | 0 | 2 | +2 |

The F29 entry is `corpus/knowledge/github-repository-security-advisories.md:1-145`. The integrated citation count is **67**, not 59 conserved occurrences: migration plus explanatory edits add references. Equal matching-line counts do not establish one-for-one span migration, quote accuracy, or body-only locators. The entry expressly discusses chrome at `:11`, so its chrome citations cannot automatically be treated as faulty guidance citations. Source-span review remains separate.

### Contradictions that totals must not hide

1. **C2 target 30 frontier rows is unmet: actual 29.** The +2 source rows are S075 enrichment and S076 successor (`corpus/SOURCES.md:81-82,175`), not two new topics. The +1 knowledge file is ZDI policy; `corpus/README.md:699-702` explicitly places it within F02 and admits no F30. This agrees with `corpus/lessons/round-47.md:59-65`; no target reroll is proposed.
2. **Frozen policy-name plain expectation ≥3 files is not reached: actual 2.** Exact hits are `corpus/knowledge/zdi-disclosure-policy.md` and `corpus/SOURCES.md`. README uses the abbreviation “ZDI” (`corpus/README.md:699,702`), which the frozen expression does not match. Do not silently widen the expression to include ZDI or replace its numeric result with a semantic count.
3. **Frozen `supersedes S074` plain target 1 differs from actual 2.** Both matches are legitimate distinct surfaces: registry teaches at `corpus/SOURCES.md:82`, registry-change explanation at `:175`. This is not two successor rows. Do not collapse matching lines into a boolean or delete explanatory evidence merely to hit one.
4. **C1 remains not fully met despite scaffold and old-citation zeros.** `corpus/lessons/round-47.md:59,67-69` preserves S074 as mined historical because rejection breaks B3. `corpus/SOURCES.md:176-177` records the used-by change and historical anchor correction. Numeric cleanup cannot imply the frozen mined→rejected transition happened.

## Wave-1 roles

Committed `.ufo/waves/round-47/w1/swarm-registry.json:7-711` contains **64 members**. Independently counted role fields in committed `.ufo/waves/round-47/wave1-spec.json:12-333` agree exactly:

| Role | Members |
|---|---:|
| connector | 2 |
| critic | 8 |
| executor | 8 |
| mutation-tester | 6 |
| revenger | 1 |
| reviewer | 12 |
| scout | 11 |
| scribe | 12 |
| sentinel | 3 |
| simplifier | 1 |
| **Total** | **64** |

This measures registered/specification membership, not completed reports, distinct successful attacks, or independent closure. The lesson explicitly denies that lane-dispatched seats constitute non-author closure (`corpus/lessons/round-47.md:45-47`). Base predates this wave: its role total is not a zero-member completed wave; it is not applicable.

## One bounded proposed move

Use this **two-layer ledger** in the final review: publish exact frozen-expression numeric deltas alongside, never in place of, C1/C2 semantic dispositions. Preserve both the 0→2 supersession-line result and 0→2 policy-name-file result without repairing either expression or production text to manufacture a target count.

Second-order effects: current guidance may migrate to a reproducible successor while historical capture binding stays mined; an enrichment can expand source/knowledge substrate without expanding frontier coverage; explanatory provenance can increase token counts without adding admissions. This move improves verifiability without inflating coverage or harming historical evidence. It changes only review evidence, not contract, runtime, captures, instruments, or registry decisions.

Risk: consumers could misread row growth or 64 seats as coverage/closure, or require citation-occurrence conservation and reject valid explanatory references. The separate units and explicit unmet-target statements above prevent those substitutions; they do not prove semantic correctness.

## Verification boundary

Executed: committed-object reads and static data arithmetic only, including independent registry/spec role aggregation. Unrun: all repository counters, capture-binding/recheck instruments, census, live captures, selftests, mutant batteries, domain-target actions, and any other runtime. No gate is claimed green here. Verification for the numeric proposal is reproducible by the cited frozen expressions against `git show` bytes, comparing receipt hashes first. Semantic review must still inspect source spans and B3 preservation separately. No tools installed or updated; no git/jj mutations, service operations, or production edits.

Report: .ufo/waves/round-47/w2/R47W2Numbers.md
