# ScoutPipeline — round63 predata reconnaissance

Axes: bounded upstream-error discrimination; existing zero-count compatibility; final-stage compatibility; provenance scope. Read-only source walk, not candidate validation or a coverage claim.

## Findings

**High confidence: positive upstream exit >1 is narrower than the four named examples.** A finite direct probe, `cat /fast/scratch/hyaku/kasegi-r63/ScoutPipeline/missing-r63`, exited **1**, stderr `cat: /fast/scratch/hyaku/kasegi-r63/ScoutPipeline/missing-r63: No such file or directory\n`, stdout empty. Thus the proposed >1 rule necessarily leaves `cat missing | wc -l` green when want=0. Treat that case as a disclosed residual/control, not a killed positive->1 case. Making it stale would require changing the intended predicate; do not silently broaden. Raw command/output/exit are saved under the seat output subdirectory. No other fresh execution probes or gates were run.

**Observed executor:** `corpus/instruments/figure-audit.py:74-120` (`run_derive`) launches every stage, consumes final stdout, waits every upstream process, then checks **only** `processes[-1].returncode` at :99-102. Upstream stderr is placed in temporary files, never read for verdicts, and closed. Consequently an upstream process can fail while the final `wc` produces nonempty `0`; `audit` at :279-291 calls that value ok when want=0. This is source reasoning, not a fresh execution receipt for grep/git/python.

Literal caller trace: `main` -> `audit` -> `parse_derive` -> `run_derive` -> `subprocess.Popen`. Parser :217-249 stores each pipeline separately and splits `&&`; current final failure returns before the next group, while successful groups concatenate stdout. Semantic tooling unavailable: `read xd://lsp` returned `No such tool`; the trace is literal source inspection, **not LSP semantic proof**.

## Real ledger inventory and compatibility

Re-opened the **committed** ledger using:

`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show fdccc6da803965234c1eff5a0fee38b97e6621c1:corpus/instruments/figure-audit-ledger.json`

Its 35 rows contain 31 grep derives: 17 final `grep -c` stages and 14 nonfinal grep stages. The nonfinal set is completely enumerated below:

- `entries-r54`, `entries-r55`, `entries-r56`: git show -> grep F-row selection -> cut -> tr -> wc; wants 38,39,40 (:87-92,151-156,233-238).
- **Actual intentional no-match uses:** `figure-audit-mentions-base-log` and `figure-audit-mentions-base-knowledge-expected` (:119-132). Both guard the object with `git cat-file -e ... &&`, then `git show ... | grep 'figure-audit' | wc -l`, want **0**. The row descriptions explicitly explain grep exit1. Original receipt `.ufo/waves/round-54/controls/c1-donothing-r54.txt:16-22` records each historical `grep -c` result as 0/exit1. These two rows, not generic hypothetical no-match examples, motivate preserving upstream exit1.
- `census-fresh-literal-r55`, `census-internal-r55-receipt`, `census-gone-r55-receipt`, `census-fixedpoint-internal-r55`, `census-fixedpoint-gone-r55`, `fail-entry-records`, `census-fresh-literal-r56`, `census-internal-r56-receipt`, `census-gone-r56-receipt`: grep -oE -> head/tail -> cut over historical receipts (:175-214,257-275). None expects zero/no-match.

The 17 final grep count rows are `frontier-rows`, `registry-rows`, `knowledge-expected-entries`, `knowledge-files`; the same four families with suffixes `-r54`, `-r55`, `-r56` (the expected-entry family is `knowledge-expected-rNN`); and `figure-audit-mentions-base-scorecard`. All expect positive counts. The remaining four nongrep derives are capture line/byte counts (S085), redirected S086 line count, and S086 sha256sum -> cut.

There are **no cat or Python derives in the production ledger**. Git upstreams are real: 20 git-show pipelines, four git-ls-tree pipelines, and the two cat-file guard stages within the already-counted zero rows. Source inspection identifies no legitimate ledger row that intentionally needs an upstream exit >1. **Inference:** the bounded >1 change should preserve intended ledger values, especially the two no-match rows; this is not a runtime claim that all current stage statuses are <=1. The prior committed receipt `.ufo/waves/round-62/controls/final-verification-r62.txt:80-119` records ledger35/35, but does not expose individual upstream statuses.

## Minimum compatibility controls for L1's finite collector

These are recommendations/expected verdicts, **not executed here**:

1. Replay both named historical no-match derives verbatim with want0 -> audit0, derived0; protects existing ledger behavior and `&&` guards.
2. An ordinary successful `cat present | wc -l`, plus `cat present | grep absent | wc -l` -> audit0 with expected 1 and 0 respectively.
3. Final-stage no-match `grep -c absent present` with want0 -> **audit1** (unchanged final exit1 handling). A final-stage positive >1 error -> audit1. A final-stage exit0 with empty stdout -> audit1.
4. Existing `and-shortcircuit-fails` and `and-stdout-concatenated` selftest shapes (:401-402) retain audit1 and audit0 respectively. An upstream >1 in an earlier pipeline group must not be erased by a later `&&` group.
5. Named error classes: `grep '[' present | wc -l`, `git show nonexistent-ref | wc -l`, and `python3 corpus/instruments/fail.py | wc -l` (fixture exits7) should change from masked0 to audit1 under positive->1. Record actual upstream statuses in the separate execution seat receipts. `cat missing | wc -l` remains masked0 under that exact rule because observed cat exit1.

No signal-status, sandbox, allowed-flag, side-effect or universal all-errors claim follows. Keep negative statuses out of this positive-status claim. Current docstring :40-41 and SKILL registry :1224 explicitly describe last-stage behavior; any later amendment must distinguish changed upstream >1 handling from unchanged final status/exit1 counting.

## S096 fit and source anchors

`/home/vgpnk/Projects/shokunin/CORPUS.md:90-108,112-125` permits kind own-work with a repo path/command, tier A **for its scope**, including “the lane's own re-runnable gate output”; lessons are valid used-by consumers. Existing S077 (`corpus/SOURCES.md:83`) is own-work/A with a lesson consumer and explicitly bounded normative scope. PROVINCE :24-32 owns claim gates; :43-52 leaves research-method ownership with chousa and refuses live targets. Thus **S096 own-work/A is appropriate only for this lane's committed figure-ledger/audit evidence**, not shell-tool semantics generally, independent verification, bounty efficacy or new knowledge ground.

Recommended source binding: `fdccc6da803965234c1eff5a0fee38b97e6621c1:corpus/instruments/figure-audit-ledger.json:119-132` plus the committed r62 final receipt :80-119, and executor :95-102. Located <=25-word quotes re-opened this round:

- Executor :99: `status = processes[-1].returncode`
- Ledger :124 and :132: `"want": "0"`
- r62 receipt :116: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`

L1 should personally reopen the committed source it registers; the row anchor must name revision + exact lines, and the round63 lesson Gate should cite S096, access date and a located quote grounding its narrow teaches cell. Registry currently ends S095 (:104); no S096 row was created by this seat. No external URL was accessed or needed.

## Governing limits and handoff

Read lane SKILL registry/execution corrections, PROVINCE, QUALITY R17/R50/R53/R58/R72/R82, and r62 spotcheck :52-63,98-105. R17 requires distinguishable exact-once compiling limb mutants; R50 requires at least three pre-freeze mutants per limb; R53 also requires defective-tree probes. R58 holds verifiability4 nominal unless the axis census metric itself moves. R72 bounds grammar/security claims to measured classes; R82 requires fail-closed harness errors and declared tools/current interpreter. This report is planning evidence, not satisfaction of those execution gates.

No production changes, Git/JJ mutations, installs, delegates, source registrations, heavy tests or live-target activity. No scratch directory was created, so no scratch cleanup remains. Only scoped report and own output evidence were written.

Self-evaluation: accuracy4 (stage-status compatibility inferred, not freshly measured); completeness4 (finite recommended controls await execution seats); clarity4 (inventory is grouped rather than reproducing all JSON); actionability4 (cat mismatch requires explicit claim disposition); conciseness4 (detail retained to make anchors auditable); mean4.0. Highest-impact improvement is to bind the final claim to the execution seat's actual status receipts. Would the user agree? Likely, provided the cat exit1 residual remains explicit.
