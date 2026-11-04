# kasegi r64 w1 — CriticPipeline (critic, prefreeze falsification)

Scope: attack the intended figure-audit upstream rule in scratch only. Intended rule (from spec):
upstream `rc > 0` is stale except basename `grep` with `rc == 1`; negative (signal) upstream
statuses stay ignored; final-stage nonzero keeps precedence; `&&` short-circuits.
No production edit, no commit, no candidate scoring against the frozen claim, no network, no installs.
Host: GNU grep 3.12-modified, GNU coreutils 9.12, Python 3.14.8 (all pre-existing; nothing installed).
Scratch: /fast/scratch/hyaku/kasegi-r64/CriticPipeline (removed on exit after receipts copied).
Receipts: .ufo/waves/round-64/w1/CriticPipeline/ (run UTC printed in each receipt).

## 1. Base controls (run before attacking)

- Base production copy at d74be00 (`figure-audit-base-copy-d74be00.py`) `--selftest`: `selftest cases=43 failures=0` (receipt `selftest-base.txt`).
- Base audit against the lane ledger, root = lane: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` (receipt `base-ledger-run.txt`).
- Native head exit codes (receipt `probe-heads-run.txt`):

| probe | native rc | base verdict (`| wc -l`) |
|---|---|---|
| `cat missing.txt` | 1 | ok 0 |
| `cat d_exist missing.txt` (partial stdout "a") | 1 | ok 1 |
| `cut -d' ' -f1 missing.txt` | 1 | ok 0 |
| `head missing.txt` | 1 | ok 0 |
| `tail missing.txt` | 1 | ok 0 |
| `ls missing.txt` | 2 | stale (exit-2) already |
| `sort missing.txt` | 2 | stale (exit-2) already |
| `sha256sum missing.txt` | 1 | ok 0 |
| `grep absent g.txt` (no match) | 1 | ok 0 |
| `grep 35 missing.txt` / `grep '[' g.txt` / `grep -s 35 missing.txt` / `grep 35 adir` / `grep -q absent missing.txt` | 2 | stale (exit-2) |
| `grep -a x bin.dat` | 0 | — |
| `wc -l missing.txt` | 1 | — |

## 2. Attack matrix (base vs intended rule, receipt `harness-run.txt`)

Intended rule implemented in the harness as a mirror of `run_derive`; only the upstream decision differs.

| case | base | intended | note |
|---|---|---|---|
| cat missing `\| wc -l` | ok 0 | stale upstream-1 | intended |
| cat partial `\| wc -l` | ok 1 | stale upstream-1 | intended (want1 base) |
| cut / head / tail / sha256sum missing `\| wc -l` | ok 0 | stale upstream-1 | intended |
| ls / sort missing `\| wc -l` | stale upstream-2 | stale upstream-2 | non-discriminating (see §4) |
| grep absent g `\| wc -l` | ok 0 | ok 0 | must stay |
| grep `'a\d'` g `\| wc -l` (rc1 + stderr warning) | ok 0 | ok 0 | see F6 |
| grep absent missing `\| wc -l` | stale upstream-2 | stale upstream-2 | must stay |
| cat missing `\| grep absent g` | stale derive-exit-1 | stale derive-exit-1 | final precedence preserved |
| grep absent g `\| cat missing` | stale derive-exit-1 | stale derive-exit-1 | final precedence preserved |
| cat missing `\| python3 fail7.py` | stale derive-exit-7 | stale derive-exit-7 | final precedence preserved |
| `python3 exit1count.py \| wc -l` (prints 3, rc1) | ok 1 | stale upstream-1 | new fail-closed (F3) |
| `python3 nonzero-after-output.py \| wc -l` | ok 1 | stale upstream-1 | new fail-closed (F3) |
| `python3 sigkill-partial.py \| wc -l` (prints 1,2,3, SIGKILL) | ok 3 | ok 3 | pre-existing false green (F4) |
| `sha256sum -c sums.txt \| grep -c OK` (one FAILED, rc1) | ok 1 | stale upstream-1 | new fail-closed (F3) |
| `sort -c unsorted.txt \| wc -l` (disorder, rc1) | ok 0 | stale upstream-1 | new fail-closed (F3) |
| `python3 bigprint.py \| head -1` (writes into closed pipe, rc1) | ok line 0 | stale upstream-1 | new fail-closed (F3) |
| `cat big.txt \| head -1` (SIGPIPE, rc -13) | ok | ok | negative preserved (killmatrix) |

Verdict monotonicity: base accepts every upstream `rc <= 1`; intended accepts `rc <= 0` plus `grep rc == 1`; negatives are handled identically. Therefore the intended accept set is a subset of the base accept set: **the rule cannot introduce a new false green**, provided final-stage checks and negative handling are unchanged. All new differences are fail-closed (false stale).

Production ledger sweep (harness, root = lane): 0 verdict differences across 35 entries (`harness-run.txt` is the harness; the sweep ran inline and printed `verdict-diffs 0 of 35`).

[INFERENCE] Selftest: by inspecting the 43 cases, only `upstream-cat-missing-exit1-retained` (expects ok 0 with `cat missing | wc -l`) changes under the intended rule; the other 42 do not involve a non-grep upstream rc1. Not executed against a candidate (candidate build belongs to ExecPipeline).

## 3. Kill matrix (receipt `killmatrix-run.txt`)

26 probes, each with an intended expected verdict. Mutants are plausible mis-implementations of the rule.

| mutant | killed by (count) | killing probes |
|---|---|---|
| intended | 0 | — |
| exemption keyed to NEXT stage argv (off-by-one) | 4 | grep-nomatch, grep-nomatch-warning, grep-nomatch-chain, sha256-check-fail |
| exemption if ANY stage is grep | 3 | mid-cat-missing-grep, grep-then-cat-missing, sha256-check-fail |
| exemption by substring `grep` in argv | 1 | filename-contains-grep (`cat grep-missing.txt`) |
| all negatives stale (incl. SIGPIPE) | 3 | sigpipe-head, sigpipe-grep-head, negative-signal-counter |
| SIGPIPE-only negatives (option, §5) | 1 | negative-signal-counter only |
| base rc1 ignored | 14 | cat/cut/head/tail/sha256 missing, partial, mid, chains, filename, sort/sha256 -c, python exit1 |
| upstream checked before final | 2 | final-python7-precedence, final-grep1-precedence |

Each mutant-specific kill is a concrete regression requirement (§6).

## 4. Probe-design defects found (fix before freeze)

- `ls missing` and `sort missing` are rc 2 in base: base is **stale**, not green, so they are not "base green want0" and cannot discriminate the new rule. Keep them only as pins for the existing `>1` path.
- `grep -c absent g.txt | wc -l` prints `1` (the `0` line counts as one line), not `0`. Use `grep absent g.txt | wc -l` (= 0) for the "no-match zero" control.
- My first harness `cat-big-head-sigpipe` used `bigprint.py` (a 60-byte script), so it did not exercise SIGPIPE. The kill-matrix `sigpipe-head` probe uses a 6.6 MB `big.txt` (receipt does not ship the file; regenerate with `400000 x "row %d value"`). Use a fixture > pipe buffer (≥ 64 KiB; 6.6 MB used) so the upstream really gets rc -13.
- Partial probe: `cat d_exist missing | wc -l` base prints `1` — the "want1" partial is correct for base, and the intended rule must return stale for it.

## 5. Findings: new harm vs pre-existing

**New harm (all fail-closed, none false green):**
- F3. A legitimate non-grep rc1 that base silently counted now goes stale: `sha256sum -c` with a FAILED line, `sort -c` disorder, a counter that deliberately exits 1 after printing, an uncaught exception after printing (intended), and a python counter piped into `head -N` (BrokenPipe → rc1). Requirement: pin each as stale in the selftest and document in the docstring. Refusing `-c`/`-C`/`--check` at parse time is an alternative but changes the refusal set and is not required by the spec.

**Pre-existing, preserved by spec, NOT fixed by the intended rule:**
- F4. Negative-signal upstream (SIGKILL/OOM) counts partial output as green (`python3 sigkill-partial.py | wc -l` → `ok 3`, base and intended). The spec says "preserve negative signal handling", so this stays. L1 must either disclose it as residual or decide otherwise. Concrete option tested: ignore only SIGPIPE (rc -13) and stale every other negative; it keeps both SIGPIPE probes green and kills only `negative-signal-counter` (receipt `killmatrix-run.txt`, mutant `opt-sigpipe-only-negatives`). This is a spec change, so it is L1's call.
- F5. PATH-shadowed `grep` (a fake `grep` that exits 1 with no output) yields `ok 0` in both base and intended (`path-shadow-run.txt`). The rule narrows the exemption to basename `grep`, but a shadowed `grep` remains exempt. The docstring already says PATH binaries are not sandboxed; no rule-level fix is in scope.
- F6. `grep 'a\d' g.txt` exits 1 with stderr `grep: warning: stray \ before d` and is counted as a no-match by base and intended (stderr is never inspected). Sound on current evidence: on grep 3.12 every real error I tested exits 2 (missing file, directory, invalid regex, `-E '('`, `-P '('`, `-q` with missing file, `-s` with missing file, `-r` on a missing dir). If L1 wants "exit1 only with no stderr", K-warning flips to stale; I recommend pinning the current verdict and documenting that stderr is ignored.

## 6. Finite kill-rule requirements for the candidate and its selftest

R1 `cat missing.txt | wc -l` → stale `derive-upstream-exit-1` (kills base-rc1-ignored).
R2 `cat d_exist.txt missing.txt | wc -l` → stale `derive-upstream-exit-1` (base want1).
R3 `cut -d' ' -f1 missing.txt | wc -l`, `head missing.txt | wc -l`, `tail missing.txt | wc -l`, `sha256sum missing.txt | wc -l` → stale `derive-upstream-exit-1`.
R4 `ls missing.txt | wc -l`, `sort missing.txt | wc -l` → stale `derive-upstream-exit-2` (pin only).
R5 `grep absent g.txt | wc -l` → ok `0`; `grep 'a\d' g.txt | wc -l` → ok `0`.
R6 `grep absent missing.txt | wc -l` → stale `derive-upstream-exit-2`.
R7 `cat missing.txt | grep absent g.txt | wc -l` → stale `derive-upstream-exit-1` (kills any-grep-in-pipe).
R8 `grep absent g.txt | cat missing.txt | wc -l` → stale `derive-upstream-exit-1` (kills next-stage-argv).
R9 `cat grep-missing.txt | wc -l` → stale `derive-upstream-exit-1` (kills substring; fixture file must not exist).
R10 `cat missing.txt | python3 corpus/instruments/fail7.py` → stale `derive-exit-7` (precedence).
R11 `cat missing.txt | grep absent g.txt` → stale `derive-exit-1` (precedence).
R12 `cat big.txt | head -1` → ok first line; `grep row big.txt | head -1` → ok first line (SIGPIPE negative ignored).
R13 `grep absent g.txt | wc -l && cat missing.txt | wc -l` → stale `derive-upstream-exit-1`; first pipeline alone ok.
R14 `sha256sum -c sums.txt | grep -c OK` (one FAILED) → stale `derive-upstream-exit-1`; `sort -c unsorted.txt | wc -l` → stale; `python3 exit1count.py | wc -l` → stale; `python3 bigprint.py | head -1` → stale. These are new fail-closed pins (F3).
R15 `python3 sigkill-partial.py | wc -l` → ok `3` (preserved negative; F4) unless L1 adopts the SIGPIPE-only option.
R16 Selftest: flip `upstream-cat-missing-exit1-retained` to stale `derive-upstream-exit-1`; add R1–R14 pins; update `EXPECTED_CASES` accordingly. Docstring: replace "upstream exit1 ... remain ignored" with the grep-only exemption and list the new fail-closed consequences (F3).

## 7. Smallest safe correction (for ExecPipeline, not applied here)

Upstream decision per stage, using that stage's own argv: `rc > 0 and not (basename(argv[0]) == "grep" and rc == 1)` → `derive-upstream-exit-<rc>`; `rc < 0` ignored; keep final-stage check first; keep `&&` and per-pipeline return; keep `grep` no-match zero. Keep the decision keyed to `processes[i]` and its argv (the `mut-misidx-next-argv` mutant shows an off-by-one is caught by R8/grep-nomatch).

## 8. Tool authorization

No installs or updates. Used only existing `/usr/bin/{grep,cat,cut,head,tail,ls,sort,sha256sum,wc,git,bash}` and `/usr/bin/python3`. Nothing written to PATH directories; the fake `grep` shadow lived only in scratch `fakebin/` and was used only for F5.

Report: .ufo/waves/round-64/w1/CriticPipeline.md
