# ReviewPredicate-3 — round-64 static prefreeze review (depth:verifiability)

Scope: static review of the intended command-aware upstream rule, the r63 missing-receipt closure, `.ufo/waves/round-64/verify-r64.py`, and the finite probe/test plan. Read-only except the own receipt. No production, fleet, sibling or domain source edited. No commit, no mutating git. No tool installed. No final claim verdict: the claim is not frozen and nothing here scores it.

Raw evidence (own dir): `.ufo/waves/round-64/w1/ReviewPredicate/static-probe-receipt-r64.txt` (run-utc=2026-11-04T18:37:59Z; native exit codes plus base-vs-candidate derive probes; only the first output line per invocation is kept there).

Axes named: (1) closure completeness, (2) driver forgery resistance, (3) falsification plan strength. Moves kept only where they improve one axis without harming another.

## Findings, by severity

### F1 — HIGH: `verify-r64.py` is weaker than the r63 driver it replaces, and admits an always-clean collector
- `verify-r64.py:74` sets `good = returncode == 0 and (expected is None or ...)`; the collector row at `:65` passes `expected=None`. A collector that prints nothing, or a fixed `HARNESS probes=8 failures=0 mode=candidate`, and exits 0 is PASS.
- The r63 driver (`.ufo/waves/round-63/controls/verify-r63.py`, committed at d74be00) required `HARNESS probes=8 failures=0 mode=candidate` for the collector, `TREE probes=8 failures=0 mode=candidate` for trees, and `mutbat killed=5/5 ...` / `MUTBAT mutants=7 killed=7 ...` for both batteries, plus `FIGURE-AUDIT figures=4 ok=4 ...` for the domain trial.
- r64 drops every one of: tree probes, old mutbat, new mutbat, domain trial, and the collector expected line. The r64 final measurement therefore runs no R50 mutant battery and no R53 tree-level probe. Under QUALITY R50 (≥3 mutants per limb, before freeze) and R53 (tree-level false-green probes, each red at freeze bytes), a freeze measured by this driver is non-conforming as written.
- `selftest` expectation (`:66`) is built from the caller's `--selftest-cases`, not a pinned constant; a summary-only line `selftest cases=N failures=0` satisfies it. QUALITY R24 requires one `selftest case=<name> verdict=...` line per case; the driver checks none.
- Required fix before the trial: restore the r63-style expected lines, require exact-once matching, pin the selftest count in the driver (candidate value, not a caller argument), and add the r64 mutbat and tree-probe scripts to `PATHS` with their expected lines.

### F2 — HIGH: stale premise in the r64 base claim — `ls` and `sort` are NOT base-green
- Spec and r64 prompts say base is green (`want0`) for all eight new probes except partial. Measured on d74be00 bytes (`base.py`, sha 15bcb6c4…): `ls missing | wc -l` → `derive-upstream-exit-2` stale; `sort missing | wc -l` → `derive-upstream-exit-2` stale. Reason: base code tests `p.returncode > 1` at figure-audit.py:107 and both exit 2 natively (rc=2 measured).
- Consequence: the candidate delta is six repairs, not eight: `cat missing`, `cat present+missing` (partial), `cut`, `head`, `tail`, `sha256sum` (all native exit 1, base green, candidate stale). `ls` and `sort` are retained stale in both base and candidate; their candidate expectation is `derive-upstream-exit-2`, same as base.
- Predicted candidate-mode collector run on base bytes: failures=6 over these probes (the collector must confirm from raw output). Predicted base-mode run on candidate bytes: failures=6.
- This is the same class as r63 M63-4 (wrong initial premise about exit codes). Recommend recording it as a new mistake row before the collector freezes, with native exit codes cited from the receipt: cat 1, cut 1, head 1, tail 1, sha256sum 1, ls 2, sort 2, grep-missing-file 2, grep-no-match 1.

### F3 — HIGH: no paired base-bytes control in the driver; constant-output forgery undetected
- The driver runs counters only against committed candidate bytes. A forged producer that prints the expected candidate line passes. The discriminating control is missing from the final measurement.
- Required paired invocation: the same collector, same work tree, run twice — (a) on the frozen candidate bytes in `--mode candidate` expecting `failures=0`, and (b) on d74be00 base bytes in `--mode candidate` expecting `failures=6` (per F2) and exit 1. A constant-output fake cannot satisfy both lines; a fake that reads its instrument's sha is defeated by the R50/R53 mutants being red.
- Also run each counter on ≥3 mutant instruments (one per limb, see test plan); every mutant must be red.

### F4 — MEDIUM: driver does not pin inputs or the construction override
- `INPUT … sha256=` lines are printed, never compared. The frozen claim must pin: `corpus/instruments/figure-audit.py` = candidate sha; `figure-audit-ledger.json` = `28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b` (unchanged since r63, verified at d74be00); `S086.txt` = `fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f`; `gate-final-r55.txt` = `31ec08a998abf3b396a41a3515d9e2a9631b5d15cc6339c8b38e438016abb8c5`; `df3-fixedpoint-r55tip.txt` = `a054cbfec69819b1096269fa3365675ecd7ca07dc7f63ed7393d7eb4562acb2b`; `c2-counter-final-r53.txt` = `be69ece74fcd5498dd23e14c9ec1aa862a579bbb46f2df22c1692409f42bf3ab`; `gate-final-r56.txt` = `e0771d54473251537fff131a569f230d315c42061784c809232f88a2fd2863d9` (all six measured via `git show d74be00:<path> | sha256sum`).
- `--candidate` is accepted in the same code path as the final run; `construction-override=True` is printed but nothing refuses it. Add a `--final` mode that rejects `--candidate` and requires `construction-override=False` and no `CANDIDATE` line in the receipt.
- The driver's own sha is not recorded. `verify-r64.py` is currently untracked (absent from d74be00); record its sha256 and require it to equal `git show <R>:.ufo/waves/round-64/verify-r64.py`.

### F5 — MEDIUM: "missing Git ref" probe and selftest case test a non-repository, not a missing ref
- Selftest case `upstream-git-missing-ref-stale` (figure-audit.py:415) and the r63 collector probe `git-missing-ref` run `git show refs/…` in a fixture directory that is not a Git repository (r63 transcript cwd=`…/git-missing-ref`, no `.git`). The exit 128 comes from "not a git repository"; the label "missing ref" is not what was exercised. The same probe passes whether the ref is missing or the repo is absent.
- Fix: build the fixture as a real repo (`git init` under the fixture dir; assert `git rev-parse --show-toplevel` equals the fixture dir before any git op, per the host guard). Pair it with a present-ref control (green) and a missing-ref case (128 from inside the repo). Otherwise rename the probe to `git-not-a-repo`.

### F6 — MEDIUM: test-plan gaps for the new rule (cases the candidate selftest lacks)
- `&&` with upstream positive error in the FIRST group, final group green: `cat missing.txt | wc -l && cat g.txt` → must be stale `derive-upstream-exit-1`. Measured: base returns no upstream reason (`derived=0` then second line), candidate returns `derive-upstream-exit-1`.
- `&&` with upstream positive error in the SECOND group: `cat g.txt && cat missing.txt | wc -l` → must be stale. Measured: base `derived=35\n…` with no upstream reason; candidate `derive-upstream-exit-1`. Not in the ExecPipeline case list.
- Middle-stage positive error, final stage success: `cat present.txt missing.txt | cat | wc -l` style (R53 middle-stage class). Not in the candidate list (only first-stage).
- Named-file and named-program disguise: `cat grep.txt | wc -l` with `grep.txt` missing → must be stale (kills any mutant that tests `"grep" in argv` rather than `argv[0]`). And `python3 corpus/instruments/grep.py | wc -l` with an exit-1 fixture → must be stale.
- Final precedence with an upstream error present: `cat missing.txt | grep absent` → `derive-exit-1` (base and candidate agree; keep as a case). `cat missing.txt | python3 corpus/instruments/fail.py` → `derive-exit-7` (candidate case exists; keep).

### F7 — MEDIUM: equivalent mutant under the admitted grammar must be classified, not killed
- `os.path.basename(head) != "grep"` (ExecPipeline diff, `upstream_stale`) versus `head.startswith("grep")`: READ_ONLY_HEADS admits only the literal `grep`, so both are equivalent on every decodable argv. Classify as an equivalent control (R17 invalid/equivalent class), not as a kill. Same for `"grep" in head` versus `==`.
- Non-equivalent basename mutant to kill: `os.path.basename(argv[-1]) != "grep"` or any argv-scanning check; killed by the named-file case above.

### F8 — LOW: receipts, closure hygiene and residual
- Short revs in the ledger (`32782bd` on frontier-rows, registry-rows, knowledge-expected-entries, knowledge-files, capture-lines-s085, capture-bytes-s085, and the figure-audit-mentions rows use full 32782bd6…): abbreviations can become ambiguous as the lane grows. Record full hashes in the r64 closure receipt (no ledger edit in this round).
- Git-object derives read through the `.git` gitdir pointer, so lane `config`, `replace` refs and `info/grafts` apply. Verified this round: `refs/replace` empty, no `info/grafts`, `core.bare=false`. Set `GIT_NO_REPLACE_OBJECTS=1` in the driver env and record it.
- Collector runtime binaries: r63 manifest listed cat, git, grep, python3, wc. r64 adds cut, head, tail, ls, sort, sha256sum. The collector must emit resolved path and sha256 of each (PATH-dependence otherwise).
- Real ledger does not discriminate: 35/35 on both base and candidate (no real derive has a non-grep positive upstream error). Its green is a regression guard only; say so in the claim.

## r63 missing-receipt closure — exact

Root cause (verified): r63 `verify-r63.py` PATHS omitted four worktree receipts. `final-verification-r63.txt` printed `real-ledger ... figures=35 ok=26 stale=9` with the nine stale derives all `derive-upstream-exit-2` (census-*-r55, census-*-r56, census-fixedpoint-*-r55, fail-entry-records). `verify-r63-supplemental.py` added exactly those four and printed 35/35 (`supplemental-verification-r63.txt`), labelled NONCLAIM.

Derive-by-derive enumeration of the 35 ledger entries (`figure-audit-ledger.json`):
- 24 entries use `git show|ls-tree|cat-file <rev>:…` (rev-addressed; need commit objects, not worktree files). Revs: `32782bd` (short), `32782bd6b564f80454af853b38868603a4140e79`, `5108584aab38a1919992c46d0224f6ec1cb59363`, `133c575394099abf28ddf1b0125c53aefde3e0fa`, `8a5d7538b0caa50300b1eee88442a230d9a433f2`. All five verified present with `git cat-file -e` (exit 0).
- 11 entries read worktree paths with cwd=root:
  - `corpus/source-snapshots/round-54/S086.txt` — capture-lines-s086 (`wc -l <`), capture-sha256-s086
  - `.ufo/waves/round-55/controls/gate-final-r55.txt` — census-fresh-literal-r55, census-internal-r55-receipt, census-gone-r55-receipt
  - `.ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt` — census-fixedpoint-internal-r55, census-fixedpoint-gone-r55
  - `.ufo/waves/round-53/controls/c2-counter-final-r53.txt` — fail-entry-records
  - `.ufo/waves/round-56/controls/gate-final-r56.txt` — census-fresh-literal-r56, census-internal-r56-receipt, census-gone-r56-receipt
- Default ledger path `corpus/instruments/figure-audit-ledger.json` and the instrument itself are read by the CLI.

Closure of the LEDGER in `verify-r64.py` PATHS: complete. The 8 PATHS entries cover all 5 worktree files above plus the instrument, ledger and collector. No derive reads an unlisted file. The four receipts exist at d74be00 (verified). So the ledger closure gap that caused M63-7 is closed in the r64 driver; I found no remaining ledger gap.

Closure of the DRIVER (what a claim needs), not yet complete:
1. Collector `.ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py` — directory does not exist yet (`w1/ExecCollector` absent); driver fails closed with exit 2 until it is authored AND committed at the measured revision.
2. Candidate `corpus/instruments/figure-audit.py` must be committed at the measured revision with the frozen sha; the d74be00 base is `15bcb6c4…`, the ExecPipeline candidate in progress is `ca1015b2…` (uncommitted, unfrozen).
3. Mutant battery script (R50) and tree-probe script (R53): none exist for r64; add both to PATHS with their committed paths and expected lines (F1).
4. Driver itself committed (F4).
5. Collector resolved-binary manifest (F8).
6. Domain-trial inputs (`domain-review-ledger-r63.json`) are only needed if the r64 claim cites the S094 trial; out of scope for the figure-audit predicate — drop from closure unless the claim says otherwise.

Hence: the IRC-announced selection (eight files, including the four receipts) is correct for the ledger; the driver is not yet a sufficient closure for the claim.

## Test plan (finite)

Probe table (candidate-mode expectation vs base-mode expectation, native exit in parentheses):
| # | derive | base (d74be00) | candidate |
|---|---|---|---|
| P1 | `cat missing.txt \| wc -l` (1) | green want0 | stale derive-upstream-exit-1 |
| P2 | `cat present.txt missing.txt \| wc -l` (1) | green want1 | stale derive-upstream-exit-1 |
| P3 | `cut -c1 missing.txt \| wc -l` (1) | green want0 | stale derive-upstream-exit-1 |
| P4 | `head -n 1 missing.txt \| wc -l` (1) | green want0 | stale derive-upstream-exit-1 |
| P5 | `tail -n 1 missing.txt \| wc -l` (1) | green want0 | stale derive-upstream-exit-1 |
| P6 | `ls missing.txt \| wc -l` (2) | stale exit-2 (retained) | stale derive-upstream-exit-2 (unchanged) |
| P7 | `sort missing.txt \| wc -l` (2) | stale exit-2 (retained) | stale derive-upstream-exit-2 (unchanged) |
| P8 | `sha256sum missing.txt \| wc -l` (1) | green want0 | stale derive-upstream-exit-1 |

Positive/regression controls (must stay green on candidate; base result in parentheses):
- `grep absent g.txt \| wc -l` → 0 (green/green)
- `grep -c absent g.txt \| wc -l` → 1 (green/green; grep no-match)
- `cat g.txt \| wc -l` → 1; `cat g.txt && cat g.txt` → `35\n35` (green/green)
- `python3 corpus/instruments/kill.py \| wc -l` (signal -15) → ignored (green/green)
- `grep '[' g.txt \| wc -l` → stale derive-upstream-exit-2 (both)
- `git show refs/…missing \| wc -l` inside a REAL repo → stale derive-upstream-exit-128 (both)
- `cat g.txt \| grep absent` → stale derive-exit-1 (both; final-stage)
- `cat missing.txt \| grep absent` → stale derive-exit-1 (both; final precedence over upstream)
- `cat missing.txt \| python3 corpus/instruments/fail.py` → stale derive-exit-7 (final precedence)

Tree probes (R53, each red at freeze bytes): T1 P1; T2 P2; T3 `cat present.txt \| cat missing.txt \| wc -l` (middle stage); T4 `cat grep.txt \| wc -l` with grep.txt missing (named-file disguise); T5 `python3 corpus/instruments/grep.py \| wc -l` exit-1 fixture; T6 `cat missing.txt \| wc -l && cat g.txt` (first && group); T7 `cat g.txt && cat missing.txt \| wc -l` (second group). Controls green on freeze bytes: `grep absent g.txt \| cat \| wc -l` → 0; `cat g.txt \| cat \| wc -l` → 1.

Mutants (R50, ≥3 per limb, exact-once, each must compile and be killed or classified):
- Limb A (non-grep exit1 stale): A1 delete `status == 1 and …` (grep no-match now stale → killed by grep controls); A2 `return False` for all exit1 (killed by P1–P5, P8); A3 revert to `status > 1` (killed by P1–P5, P8); A4 `startswith("grep")` → equivalent, classify, not killed (F7).
- Limb B (negative statuses ignored): B1 `status > 1` → `status != 0` (killed by kill.py control); B2 add `if status < 0: return True` (killed by kill.py control); B3 `abs(status) > 1` (killed by kill.py control).
- Limb C (final precedence): C1 move upstream loop before `status != 0` check (killed by `cat missing \| python exit7` case); C2 drop `status != 0` return (killed by `cat g \| grep absent`); C3 check final stage only when no upstream error (killed by C1-case).
- Limb D (&& propagation): D1 check upstream only for last group (killed by T6); D2 check upstream only for first group (killed by T7); D3 break on first group but not stale-stop (killed by T7 stdout).

Forgery matrix (must read red):
- Always-clean collector (`print HARNESS probes=8 failures=0 mode=candidate`, exit 0): red under paired base-bytes control (expects failures=6 mode=candidate).
- Always-clean instrument printing `selftest cases=54 failures=0`, `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, exit 0: red under the collector's exact per-probe stdout comparison and under the 54 `selftest case=` line count.
- Summary-only selftest (no per-case lines): red under R24 check.
- Collector absent from revision: driver exit 2 (VERIFY-ERROR), no partial PASS.
- `--work` outside `/fast/scratch/hyaku/kasegi-r64/<seat>/`: exit 2.
- `--candidate` supplied to the final measurement: refused (after F4 fix).
- Tampered input (e.g., ledger with one receipt deleted): real-ledger exit 1 with the named stale derives, not a pass.

Driver closure command set for the trial (run once, after the seats land; not run by me): committed-revision driver run with `--revision <R>`, `--work /fast/scratch/hyaku/kasegi-r64/<owner>/…`, `--selftest-cases 54` pinned in the driver, plus the paired base-bytes run described in F3.

## Verdict on the seat's question
- Closure of the four r63 receipts into the LEDGER input list: complete and correct in `verify-r64.py`.
- The r64 driver as written is NOT freeze-grade: it removes the collector check, drops the R50 and R53 batteries, leaves selftest count caller-supplied, and has no base-bytes negative control.
- The intended rule is sound on the paths I traced (negative statuses, final precedence, grep no-match, `&&`); its probe premise is wrong for `ls` and `sort` (F2), and its selftest is missing the `&&` and middle-stage cases (F6).
- No candidate scoring and no claim verdict here; the claim stays NOT FROZEN.

Tools: none installed. Commands run: read-only `git cat-file`, `git show`, `git rev-parse`, `git replace -l`, `sha256sum`, native shell probes and one-invocation derive probes in `/fast/scratch/hyaku/kasegi-r64/ReviewPredicate/` (removed on exit after receipt copy). Nothing committed. No production file written.
