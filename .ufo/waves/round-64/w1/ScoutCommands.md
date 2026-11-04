# ScoutCommands — r64 recon: native exit1 semantics, controls, exact predicate, r63 closure

run-utc=2026-11-04T18:34–18:41Z (per-receipt `run-utc` lines). Scratch `/fast/scratch/hyaku/kasegi-r64/ScoutCommands/` (removed on exit; receipts + drivers copied to `receipts/` and this directory). No production bytes touched; the candidate instrument exists only as a scratch copy. No installs (repo tools only: coreutils 9.12, git 2.56.0, Python 3.14.8; `/bin/sh -> /usr/bin/bash`, dash absent — `receipts/tools.txt`).

## 1. Native exit codes of the eight proposed heads + grep (Popen returncodes = the instrument's view)

Receipts: `receipts/recon-popen-mirror.txt`, `receipts/<name>.txt` (one invocation each, rc printed).

| stage (argv) | rc | stdout | stderr |
|---|---|---|---|
| `cat missing` | **1** | — | cat: missing: No such file or directory |
| `cat g.txt missing` (partial) | **1** | `35` (partial!) | cat: missing: … |
| `cut -d : -f1 missing` | **1** | — | cut: missing: … |
| `head missing` | **1** | — | head: cannot open … |
| `tail missing` | **1** | — | tail: cannot open … |
| `sha256sum missing` | **1** | — | sha256sum: missing: … |
| `ls missing` | **2** | — | ls: cannot access … |
| `sort missing` | **2** | — | sort: cannot read: missing: … |
| `grep absent g.txt` (no-match) | **1** | — | **empty** |
| `grep absent missing` | 2 | — | grep: missing: … |
| `grep '[' g.txt` | 2 | — | Invalid regular expression |
| `tr a b missing` (extra operand) | **1** | — | tr: extra operand … |
| `wc missing` | **1** | — | wc: missing: … |
| `git show refs/heads/<absent>` | 128 | — | fatal: … |
| `git cat-file -e <absent>` | **1** | — | (silent) |
| `python3 -c 'sys.exit(1)'` / `(2)` | 1 / 2 | — | — |
| `yes` piped into `head -1` | **−13** (SIGPIPE) | — | — |
| python self-SIGTERM | **−15** | — | — |

Split of the eight proposed probes (`cat missing`, `cat partial`, `cut`, `head`, `tail`, `ls`, `sort`, `sha256sum`, each piped to `wc -l`): **six exit 1** (cat, cat-partial, cut, head, tail, sha256sum → masked by base), **two exit 2** (ls, sort → already rejected by base's `>1` rule). So ls/sort are not candidate-only catches; their regression value is preserving the >1 reason verbatim.

Shell-view cross-checks (`receipts/pipe-*.txt`): `cat g.txt missing | wc -l` → stdout `1`, rc 0 (silent under-count masked); `set -o pipefail; sha256sum missing | wc -l` → rc 1; `set -o pipefail; grep absent g.txt | wc -l` → **rc 1** (pipefail alone would flip the sanctioned no-match-zero green red — the exemption must be per-stage, not a pipefail adoption); `set -o pipefail; ls missing | cat missing2 | wc -l` → rc 1 (rightmost-nonzero precedence); bash `PIPESTATUS` for `yes | head -1` = `141 0`.

## 2. Base-vs-candidate instrument matrix (falsification battery)

Candidate = one line in `run_derive`'s upstream scan (`receipts/candidate-diff.txt`):
`if p.returncode > 0 and not (os.path.basename(p.args[0]) == "grep" and p.returncode == 1):`
(final-status check untouched, so final-stage precedence and negative finals are unchanged). Full raw log: `receipts/battery-r64.txt`.

| derive (want) | base | candidate |
|---|---|---|
| `cat missing \| wc -l` (0) | ok derived 0 | stale `derive-upstream-exit-1` |
| `cat g.txt missing \| wc -l` (1) | ok derived 1 | stale `derive-upstream-exit-1` |
| `cut -d: -f1 missing \| wc -l` (0) | ok 0 | stale exit-1 |
| `head missing \| wc -l` (0) | ok 0 | stale exit-1 |
| `tail missing \| wc -l` (0) | ok 0 | stale exit-1 |
| `sha256sum missing \| wc -l` (0) | ok 0 | stale exit-1 |
| `ls missing \| wc -l` (0) | stale `derive-upstream-exit-2` | same |
| `sort missing \| wc -l` (0) | stale `derive-upstream-exit-2` | same |
| `tr a b missing \| wc -l` (0) | ok 0 | stale exit-1 |
| `grep absent g.txt \| wc -l` (0) | ok 0 | ok 0 (exemption limb) |
| `grep '[' g.txt \| wc -l` (0) | stale `derive-upstream-exit-2` | same |
| `cat g.txt \| grep absent` (0) | stale `derive-exit-1` | same (final precedence) |
| `cat present.txt \| cat missing \| wc -l` (0) | ok 0 | stale exit-1 (mid-stage) |
| `python3 corpus/instruments/exit1.py \| wc -l` (0) | ok 0 | stale exit-1 |
| `python3 corpus/instruments/sigterm.py \| wc -l` (0) | ok 0 | ok 0 (negative retained) |
| `python3 corpus/instruments/sigterm.py` (0) | stale `derive-exit--15` | same (negative final) |
| `git show refs/heads/<absent> \| wc -l` (0) | stale `derive-upstream-exit-128` | same |
| `cat g.txt \| wc -l` (1) / `cat g.txt && cat g.txt` (35⏎35) | ok | ok |
| `cat missing && cat g.txt` (35) | stale `derive-exit-1` | same |

## 3. Real ledger replay (35 figures, read-only, cwd = lane)

Base and candidate both print `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`; FIG-line diff between the runs = **0 lines** (`receipts/real-ledger-base.txt`, `receipts/real-ledger-cand.txt`; the two files' sha differ only in the run-utc header line). The derive grammar in `corpus/instruments/figure-audit-ledger.json` is `git show|cat-file|ls-tree` + `grep -c|-oE|-F` + `wc|cut|tr|head|tail` + `wc -l < file` + `sha256sum | cut`; no `sort -c`, no python counters. **The two want=0 derives (`figure-audit-mentions-base-log`, `figure-audit-mentions-base-knowledge-expected`: `git cat-file -e … && git show … | grep 'figure-audit' | wc -l`) stay green only because upstream grep exit1 is exempt** — a candidate without the grep exemption turns the real ledger red. The rule is exactly calibrated, not over-broad.

## 4. Recommended exact finite predicate

In `run_derive`, keep the final check first (`status != 0` → `derive-exit-%d`, negatives included — preserves final-stage precedence and negative finals), then replace the upstream scan condition with:

```python
if p.returncode > 0 and not (os.path.basename(p.args[0]) == "grep" and p.returncode == 1):
```

- `> 0` not `!= 0`: upstream negative signal statuses stay ignored (`yes|head` −13, sigterm −15 upstream: observed ok in both modes).
- basename test on the already-validated argv: the grammar refuses absolute/aliased heads, so `basename(p.args[0])` is the allow-list name itself.
- First offending upstream stage wins (scan order); final check precedes it (observed `derive-exit-7` before `upstream-exit-2` in the base selftest case `final-error-precedes-upstream-error`).
- Selftest: candidate bytes fail exactly one pinned case today — `upstream-cat-missing-exit1-retained` (exit1 want0) — so that case must be repointed to want exit1 with reason `derive-upstream-exit-1` and the docstring's "upstream exit1 … remain ignored" limb updated; keep `EXPECTED_CASES` consistent with the final case count (43 now; +1 if a partial/negative-retained case is added — recount, don't guess).

## 5. Finite regression cases for the collector/selftest (per-mode expectations in §2 table)

New eight: cat-missing (base ok want 0 / cand stale exit-1), cat-partial (base ok derived **1**, want 1 / cand stale exit-1), cut-missing, head-missing, tail-missing, sha256sum-missing (base ok 0 / cand stale exit-1), ls-missing and sort-missing (both modes stale `derive-upstream-exit-2` — assert the reason stays 2, never collapses to 1). Controls that must not move: grep-no-match ok both; grep-invalid exit-2 both; final grep no-match `derive-exit-1` both; sigterm upstream ok both + sigterm final `derive-exit--15` both; git missing ref 128 both; success pipeline, `&&` concat, `&&` fail as in base.

## 6. Legitimate non-grep exit1 cases and compatibility risks

- **`git cat-file -e <absent>` rc1** is a legitimate object-absent diagnostic; under the derive grammar it can only be the final stage of its own `&&` pipeline (single stage → final) → `derive-exit-1` fail-closed. Never needs the exemption; the current ledger's two mention derives use exactly this form.
- **`sort -c` disorder rc1** (`receipts/sort-c-disordered-real.txt`) is a legitimate non-grep exit1 the rule does NOT exempt; no current derive uses `sort -c`. Document as known boundary; do not widen the rule for it.
- **python counter `SystemExit(1)`** upstream becomes a catch (positive rc1). No current ledger derive runs python; new-catch class, not a regression.
- `tr` extra-operand rc1 and `wc missing` rc1 become catches too (same limb, beyond the eight probes).
- grep rc1 is the only silent success-path rc1 in the set (stderr empty; all other rc1s carry diagnostics on stderr) — a useful independent corroborator if the collector wants one.
- pipefail/`&&` are not the mechanism and would regress: pipefail flips grep-no-match-zero to rc1; `&&` short-circuits on it (`cat g.txt && grep absent g.txt` rc1, observed). Keep the per-stage Popen scan.
- No sandbox/universal claim: PATH-shadowed plain names remain pre-existing exposure outside this limb.

## 7. r63 supplemental driver dependency closure (`receipts/r63-supplemental-closure.txt`)

`verify-r63-supplemental.py` at `204a627b32671b6e5e1ee682acbe31714c6d46eb`: all 12 PATHS present at the rev; pinned objects `32782bd…`, `5108584…`, `133c575…`, `8a5d7538…`, `fdccc6da…` all present; `corpus/source-snapshots/round-61/S094.txt` present at that rev — the domain-trial ledger reads it via `git show fdccc6da…:…` through the root `.git` gitdir pointer, i.e. its closure is git objects, not PATHS. Ledger workspace derives materialize exactly: S086.txt, gate-final-r55, df3-fixedpoint-r55tip, c2-counter-final-r53, gate-final-r56 (all in PATHS). `c1-probes-r63.py` / `pipeline-mutbat-r63.py` / `tree-probes-r63.py` write only under their `--work` run dirs (self-built fixtures, gitdir skeletons); required tools python3/cat/grep/wc/git are self-checked via `which`. Runtime proof: `controls/supplemental-verification-r63.txt` — 7/7 measurements PASS, `VERIFY measurements=7 failures=0` at that rev. r64 analog (`verify-r64.py`): same receipt set plus `.ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py`, so that collector must stay fixture-self-contained (r63 pattern) for PATHS closure to hold.

Confidence: §1–§3, §5, §7 observed on receipts; §4–§6 predicate text is the exact line tested in the scratch candidate. Gaps: none blocking; `sort -c`/python-rc1 boundaries are documented, deliberately not exempted.

Report: .ufo/waves/round-64/w1/ScoutCommands.md
