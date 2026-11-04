# ReviewPredicate — round63 predata predicate review

Axes: depth:verifiability, nominal score4 held per R58. Static review of the proposed finite claim and current `run_derive`, exact before/after predicate, kill rule, counter consistency, controls, S096 citation check, candidate review. Reviewer seat: no edits, no certification, no promotion judgment. LSP: no lsp device is mounted in this seat's inventory; evidence is committed-source reading plus one-run scratch receipts, not semantic-reference proof.

Base: `fdccc6da803965234c1eff5a0fee38b97e6621c1` == observed HEAD; tree clean except untracked round-63 wave files and the untracked `corpus/lessons/round-63.md` draft. Instrument identity: my base copy sha256 `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080` == committed blob (`ReviewPredicate/base/instrument-sha256.txt`, `instrument-git-blob-sha256.txt`). Candidate reviewed: `W/ExecPipeline/figure-audit.py` sha256 `e557d2f0ceea9866b40b7b99dd53864a00330ae7481f32e7eeefca2fbf2431e8`. Scratch `/fast/scratch/hyaku/kasegi-r63/ReviewPredicate` deleted after receipts were saved.

## 1. Base defect, independently reproduced (my receipts, `ReviewPredicate/base/`)

Direct upstream statuses pinned (`direct-*.exit/stderr`): `cat missing.txt`=1, `grep '['`=2 (`Invalid regular expression`), `git show nonexistent-ref-r63`=128 (`not a git repository` in a non-repo scratch root — no fixture commit needed), `python3 corpus/instruments/fail.py`=7.

| derive (want=0 unless noted) | base audit exit | base summary |
|---|---|---|
| `cat missing.txt \| wc -l` | 0 | figures=1 ok=1 stale=0 — masked green (upstream rc1; retained-residual class) |
| `grep '[' f1.txt \| wc -l` | 0 | figures=1 ok=1 stale=0 — masked green (upstream rc2) |
| `git show nonexistent-ref-r63 \| wc -l` | 0 | figures=1 ok=1 stale=0 — masked green (rc128) |
| `python3 corpus/instruments/fail.py \| wc -l` | 0 | figures=1 ok=1 stale=0 — masked green (rc7) |
| `cat g.txt \| python3 corpus/instruments/fail.py \| wc -l` | 0 | masked green (mid-stage rc7) |
| `grep 'zzzNoMatchR63' f1.txt \| wc -l` | 0 | legitimate green (upstream rc1 no-match) |
| `cat missing.txt` (final) | 1 | `derive-exit-1` stale — existing final-stage behavior |
| `grep '[' f1.txt` (final) | 1 | `derive-exit-2` stale |
| `cat g.txt` want35 | 0 | ok — happy path |
| missing ledger | 2 | fail-closed |
| committed ledger replay | 0 | figures=35 ok=35 stale=0 |
| selftest | 0 | cases=35 failures=0 |

Cause confirmed at `corpus/instruments/figure-audit.py:100-106` (baseline): only `processes[-1].returncode` is read; upstream `p.wait()` results are discarded. The three >1 probes are false greens exactly when `want` is the value the final stage prints from empty input ("0"). The real ledger's `figure-audit-mentions-base-log` (`git cat-file -e … && git show … | grep 'figure-audit' | wc -l`, want0) is an in-ledger upstream-exit1 figure that must stay green.

Probe-validity receipt: my first-draft invalid-regex probe used `grep 'a('` — a VALID literal BRE (upstream exits 1), so it silently probed the exit1 class (`base/p2-grep-regex2.*`). Corrected to `grep '['` (exit2, `base/p2b-grep-invalid2.*`). Any collector/receipt for this claim must pin the direct upstream exit code, or a wrong-class probe reads as coverage.

## 2. Exact predicate, before → after

Before (`run_derive`, baseline `:74-120`): per `&&` group, stages run concurrently; final-stage rc!=0 → stale `derive-exit-N` (returns immediately, later groups do not run); final rc==0 → upstream rcs ignored; all-group stdout concatenated; empty stdout → `derive-empty` stale; audit: ok/stale counters, exit=1 iff stale>0, exit=2 harness/refusal.

After (candidate diff, whole diff inspected): identical, plus one branch after the final-status check, inside the per-group loop:

- when the group's final rc==0, scan upstream stages in execution order; first positive rc>1 → stale `reason=derive-upstream-exit-N`, return immediately (subsequent `&&` groups do not run — a deliberate widening of the gate's stop condition, documented in the candidate docstring as "&& stops on either failure"; it is not bash pipeline-status equivalence);
- upstream rc==1 and negative (signal) rcs: unchanged, ignored;
- final-stage reason precedence unchanged (`derive-exit-N` checked first; selftest case `final-error-precedes-upstream-error` binds `derive-exit-7` over a present upstream rc2);
- no parse/allow-list/flag/timeout/side-effect change (diff touches only docstring, `EXPECTED_CASES`, `run_derive` guard, `run_case` reason assertion, 8 new selftest cases, confined `fail.py` fixture);
- `EXPECTED_CASES` 35→43 declared with the R17 pin comment retained; each new error case binds both audit exit and the printed reason substring.

## 3. Counter-consistency requirements (verified on candidate)

Per figure exactly one verdict; `ok+stale==figures`; summary `FIGURE-AUDIT figures=N ok=X stale=Y exit=E` with E=1 iff Y>0, E=0 iff all ok, 2 only on harness/refusal paths; upstream-stale counts in `stale` and prints `derived=UNAVAILABLE reason=derive-upstream-exit-N` (no derived value printed); reason strings deterministic (`%d` of the first offending stage). `git grep` over tracked files finds no other consumer that parses the summary line (receipts in LOG/SCORECARD/lessons quote it textually); the selftest's own case exits and the mutant battery are the executable consumers, and both pass on the candidate.

## 4. Kill rule (finite; every clause exercised unless named)

FAIL the claim if any of:

1. Red-before absent: base tuples differ from §1 (three >1 greens, mid-stage green, retained exit1 greens, final-stage stales, happy green, exit2 missing-ledger, selftest 35/0).
2. Do-nothing passes: unmodified base bytes run in candidate mode against the adopted expectations must FAIL (`r62` c1-do-nothing discipline).
3. Candidate tuples differ on my named set: `p2b`=exit1 figures1 ok0 stale1 `derive-upstream-exit-2`; `p3`=`…-128`; `p4`=`…-7`; mid-stage=`…-7`; `&&`-upstream shape stale with the group after it not run; `p1` cat-exit1 and grep-no-match retained exit0 ok1; final-stage `derive-exit-1`/`derive-exit-2` and final-before-upstream precedence unchanged; happy path unchanged; missing-ledger exit2.
4. Negative-rc retention breaks: `python3 corpus/instruments/spam.py | head -n 1` (upstream killed by SIGPIPE) stays ok on candidate (`candidate/base-p7-sigpipe.*`, `cand-p7-sigpipe.*` — both ok, verified).
5. Regression: committed 35-figure ledger replay is not byte-identical `figures=35 ok=35 stale=0 exit=0` (includes the in-ledger upstream-exit1 figure); domain-review ledger not 4/4; selftest not `cases=43 failures=0` with `EXPECTED_CASES=43`; SIGPIPE probe flips.
6. Harness fail-closed: collector returns nonzero on missing instrument / unusable work / instrument-under-work (MutationCollector receipts cover these five fault classes; no false-green found).
7. Mutants: battery anchors have 0 sites at base without the battery failing (base receipt must FAIL `anchor-sites`, exit2 — verified); any new-limb limb carries <3 exact-once compile-ok mutants; any survivor relabelled; equivalence controls killed or invalid controls counted as killed.
8. R53 second class incomplete at freeze: MutationCollector tree probes 2–6 (invalid-regex, git-ref, exit7, mid-stage, &&-concatenated-want shapes; the masking `&&` variant needs the concatenated want, e.g. want `0\n0`) not bound to the final integrated bytes with candidate receipts.
9. Stale premise: claim/lesson/docstring retains "Pipeline status is the last command's status, not pipefail" as a description of current behavior.
10. Scope drift: any wording claiming all-error detection, pipefail, sandboxing, signal handling, exit1 repair (incl. a "four-of-four repaired" formulation), or coverage/score movement.

## 5. S096 own-work citation check

Committed `corpus/SOURCES.md` has no S096 (S095 last row, :104). The proposal `W/SourceLedger/source-row.txt` is honest predata: source cell names lane-local committed bytes (`fdccc6d…:corpus/instruments/figure-audit-ledger.json`), anchor pins L38-L68 (the four pinned capture records — verified present by my ledger enumeration) and L118-L132 (the two `git cat-file -e`-guarded zero-count records — verified), `teaches` states exactly the bounded rule (grep2/git128/python7 stale; grep no-match exit1 countable; final-stage unchanged; cat-exit1 residual), and the admission condition requires L1 to bind the actual final C1 command + unedited single-invocation receipt before landing, with no invented hash/quote. It cannot itself prove the behavior — correct.

Supports the claim without fake expansion credit iff: (a) cited by `corpus/lessons/round-63.md` at landing; (b) no coverage/frontier/knowledge movement is claimed — frontier stays F43/43, knowledge stays 81, no new knowledge entry; (c) registry 95→96 recorded as the R8 census fact in the Registry-changes bullet, nothing more; (d) depth:verifiability stays nominal 4 held under the R58 label per r58–r62 precedent, coverage 8 untouched. Novelty to resolve at landing: `kind=own-work` is a new registry kind value (existing vocabulary: docs/spec/dataset/paper/community); the landing bullet must either state the new kind explicitly or map it to the convention. S094's separate documentation-only review is independently pinned: I verified the located quotes verbatim at `corpus/source-snapshots/round-61/S094.txt:18` ("before it appeared in an official release, so SQLite users were not impacted.") and :118 ("a target-specific fuzzer would be at least as effective"), and the four-figure domain-review ledger replays 4/4 green at base (and on the candidate).

## 6. Three-mutants-per-limb obligation (M63-1): SATISFIED on the new limb, with scope

`W/ExecMutants/pipeline-mutbat-r63.py`: anchors `guard-threshold`/`guard-refusal` have 0 sites at base → battery FAILs there (`base-anchors-receipt.txt`, exit2). On the candidate: 7 mutants, each exact-once and compile-ok, all killed by named selftest cases — threshold limb m-threshold-0 (kills via retained-exit1 case), m-threshold-2, m-threshold-ge0 (kills via exit0 case); refusal-site limb m-refusal-dead/-skip/-rc-launder; reason limb m-reason-value-constant; two equivalence controls held; one invalid control held (`candidate-battery-receipt.txt`: MUTBAT 7/7, verdict PASS). My independent re-run on my own candidate copy reproduces it exactly (`candidate/mutbat-rerun.*`). ≥3-per-limb is met for the new limb. This is not mutation saturation — it covers these anchors only.

## 7. Candidate review verdict (recommendation, not certification)

Static: the diff is the minimal bounded form; predicate §2 satisfied exactly; no second convention introduced. Independent execution on my copies (receipts `ReviewPredicate/candidate/`): all §4 clauses 1–7 pass — 12 per-instrument probe receipts ×2, selftests 35/0 and 43/0, collector 8/8 PASS in both modes on my paths, ledger 35/35, domain ledger 4/4, SIGPIPE retained, battery re-run PASS. Remaining pre-freeze integration owed (not defects in the candidate): clause 8 tree-probe candidate receipts; claim text drafting per clauses 9–10 and §5 conditions; F3 below.

Findings:

- **F2 (claim-text, must):** claim/lesson must state the four named probes as three >1 repairs plus the retained cat-exit1 control (L1's M63-4 correction); never "four repaired".
- **F3 (docstring, should):** the Exit-codes parenthetical at candidate line ~38 still reads only "a nonzero final pipeline status or empty stdout is stale" — now incomplete; harmonize to include the first upstream positive >1 branch (the later paragraph is correct; the parenthetical lags).
- **F4 (receipt hygiene, should):** every probe receipt for this claim pins the direct upstream exit code (§1 pitfall).
- **F5 (landing, note):** S096 `kind=own-work` convention decision at landing (§5).
- **F6 (claim wording, note):** name the `&&` stop-condition widening explicitly so it is not read as bash-equivalence.

## 8. Residuals (unchanged, outside the claim)

Upstream exit1 everywhere (incl. missing cat input), negative signal statuses beyond the one SIGPIPE probe, allowed counters/unscreened flags, PATH/Git configuration, races, descendant effects, timeout interplay, side effects — unchanged by the candidate and outside the predicate. Host-bound replays (ledger, domain) are not hermetic-export verification (M63-3). No LSP was available; no tool installs; no production edits; no git mutations; no lane-wide gate storm (finite one-run receipts only).

Report: .ufo/waves/round-63/w1/ReviewPredicate.md

## Erratum (appended 2026-11-04, post-review correction; nothing above rewritten)

- **F5 WITHDRAWN.** `corpus/SOURCES.md:83` (S077, "Canonical Shokunin protocol checklist contract — .ufo/waves/round-48/controls/protocol-source.txt") is an existing `own-work` / tier-A registry row. The `kind=own-work` cell follows held precedent, not new registry vocabulary; the S096 row needs no special landing bullet for its kind. My §5/F5 statement that own-work was a new kind value was wrong — S077 fell inside an elided read window when I checked.
- **F3 CLOSED.** Corrected candidate `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997` (W/ExecPipeline/figure-audit.py) fixes the Exit-codes parenthetical to "(fail-closed: nonzero final status, upstream positive status >1, or empty stdout is stale)". Diff against baseline shows the guard hunk byte-identical to the reviewed candidate and no other functional change; `py_compile` ok; recheck on my scratch copy: `cat missing.txt | wc -l` exit0 ok (retained) and `grep '[' g.txt | wc -l` exit1 `derive-upstream-exit-2` stale (`candidate/recheck-p1.stdout`, `recheck-p2b.stdout`). Behavior unchanged, as claimed.
- **R53 binding path updated.** The tree-probe counter now lives at `.ufo/waves/round-63/controls/tree-probes-r63.py` for prefreeze final-byte binding; the kill-rule clause 8 reference reads that path instead of the MutationCollector proposal copies.

Report: .ufo/waves/round-63/w1/ReviewPredicate.md
