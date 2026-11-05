# SentinelCounter — round 75, attempt 1, wave w1

Scope: exec-surface and host-safety audit of the round's only code change (C1, `corpus/instruments/recheck-cwd-census.py`). Read-only over the lane; no lane file written. Leaf seat; no subagents.

## Inputs and a caveat on the amendment

- `claims.json` read in full (C1 target, A1–A4, kill rule, `exec_surface` clause).
- The round-75 `ExecC1Amend.patch` has NOT appeared under `.ufo/waves/round-75/w1/` (checked `ls`, exit 0). The only `ExecC1Amend.patch` on disk is `.ufo/waves/round-74/w1/ExecC1Amend.patch`, a round-74 amendment already landed as commit `dca80cf` (verified with `git log --oneline -1 -- corpus/instruments/recheck-cwd-census.py`, exit 0). It is not the round-75 change and was not used.
- Per the spec fallback, I derived the C1 amendment in scratch from the `claims.json` target text (clauses i–iv) and measured that derivation. The derivation is a stand-in for the integrated patch. L1 must re-run the counts below against the file actually landed.
- Base file: `git show 748dfb666280adfb1e249fcf6a265c5d9951eefb:corpus/instruments/recheck-cwd-census.py | sha256sum` = `5ef12c7ff09937524df00a76ca3498afa1b23a52983f6e06bd4e3fc6575e2574`; byte-identical to the lane working file (`cmp`, exit 0).

## (1) Exec-surface counts (base vs amended derivation)

Full table with grep exit codes: `.ufo/waves/round-75/w1/SentinelCounter-exec-counts.txt`.

| pattern | base | amended |
|---|---|---|
| `subprocess\.` | 3 (import, `subprocess.run`, `subprocess.TimeoutExpired`) | 3 |
| `subprocess\.run` | 1 | 1 |
| `bash -c` | 1 (line 52, inside `run_foreign`) | 1 (line 59, inside `run_foreign`) |
| `os\.system` / `popen` / `shell=True` | 0 / 0 / 0 (grep exit 1 = no match) | 0 / 0 / 0 |
| `run_foreign(` (def + call) | 2 | 2 (call site line 92, the only caller) |
| `timeout=` | 1 (`TIMEOUT`, value 120, unchanged) | 1 |

Command: `grep -c -- '<pattern>' <file>`; counts recorded with per-pattern `grep_exit` in the evidence file. The derivation's diff (`.ufo/waves/round-75/w1/SentinelCounter-derived-C1.diff`, 7 hunks, 57 changed lines) touches no line matching `TIMEOUT|subprocess|bash|shell|run_foreign|Popen|os\.system` (`grep -nE '^[-+].*(...)' amended.diff`, exit 1 = no matches). No new subprocess construction, no `shell=True`, no timeout change.

**exec-surface unchanged: yes** (on the derivation; re-measure on the landed file).

## (2) The restoration_only bucket executes nothing

Amended `census()` (scratch derivation, lines 80–92), quoted:

```
value = first_recheck(path)            # header scan: line.startswith("recheck:")
if value is None:
    if first_value(path, "restoration-recheck:") is not None:   # header scan only
        counts["restoration_only"] += 1
        print("RESTORATION-ONLY %s" % name)
        continue                        # returns before run_foreign
    counts["norecheck"] += 1
    ...
code = run_foreign(value, env_tmp)      # reached only for a recheck: value
```

`first_value` only reads lines and returns the stripped remainder; it has no call into `run_foreign` or `subprocess`. The restoration value is never bound to `value` in the restoration branch, so `run_foreign` cannot receive it. The `restoration-recheck:` key does not match `startswith("recheck:")`, so the two headers are disjoint.

## (3) Host bounds and credential material

- Mutation grep over `.ufo/waves/round-75/` (all files incl. `w1/swarm-registry.json`) and the scratch amendment: `grep -rniE 'sysctl|pacman -|/proc/sys|systemctl|op://|ghp_…|sk-…|AKIA…|xox[baprs]-|BEGIN … PRIVATE KEY|api[_-]?key|password'`. Exit 0. Every hit is in the spec text (`w1-dispatch.json`, `w1-spec.json`) and reads as a prohibition ("Never mutate host sysctls", "PACMAN IS PAUSED", "grep … for 'op://', token-shaped strings"). No hit is a command or a credential. Zero token-shaped strings.
- Amended source grep `sysctl|pacman|op://|token|secret|password|sudo|chmod|/etc/|systemctl|curl|wget|http` (exit 1 = no matches).
- No sysctl, pacman, sudo, or install was run by this seat. No tool installed (none needed; no entry for `~/.local/bin` or any PATH dir).
- Writes by this seat: scratch `/fast/scratch/hyaku/kasegi-r75/SentinelCounter/` (removed, see (4)) and four files in the wave dir listed below. No lane file written. `git status --short corpus/instruments/` printed nothing (exit 0 from the `head` pipeline) and the lane HEAD still carries the base census sha.

**host mutation: none**

## (4) Scratch discipline

- Scratch was created at `/fast/scratch/hyaku/kasegi-r75/SentinelCounter/` and passed explicitly (`TMPDIR=<scratch>/tmp`).
- Removal: `rm -rf -- /fast/scratch/hyaku/kasegi-r75/SentinelCounter`; `test -e <that path>` → exit 1 (absent); parent `/fast/scratch/hyaku/kasegi-r75/` still present (shared root, owned by the orchestrator). Receipt: `.ufo/waves/round-75/w1/SentinelCounter-scratch-removal.txt`.
- The scratch selftest on the derivation (`TMPDIR=<scratch>/tmp python3 amended.py --selftest`, exit 0) printed `selftest cases=6 failures=0`; base `--selftest` printed `selftest cases=5 failures=0`, exit 0. These were on the scratch copy only, not the lane file; A1 must still run on the lane file at integration.

**scratch clean: yes**

## Observations for L1 (not verdicts)

1. The amended census prints `RESTORATION-ONLY <name>` unconditionally, not gated by `--verbose`. On the real tree it prints nothing, because every knowledge file has a `recheck:` header (`grep -l '^recheck:' corpus/knowledge/*.md | wc -l` = 90 of `ls corpus/knowledge/*.md | wc -l` = 90). So A4's "only stdout delta is the inserted field" holds on the real tree. If the landed patch keeps the unconditional print, state that or gate it on verbose.
2. Two real knowledge files carry a `restoration-recheck:` header alongside `recheck:` (`grep -l '^restoration-recheck:' corpus/knowledge/*.md` → `claim-gates.md`, `claim-package-contract.md`; count 2, exit 0). They count under `entries`/`exit*_foreign` through their `recheck:` line, so `restoration_only=0` at A2 depends on those two files keeping a `recheck:` line. This is consistent with the claim text; flagging it because a future edit could move them into the new bucket.
3. The `grep -c` exit column in the counts file is the grep exit (fixed after a first pass that recorded the `tr` exit by mistake; the file in the wave dir is the corrected one).

## Evidence files (wave dir)

- `SentinelCounter-exec-counts.txt` — per-file, per-pattern counts with grep exit codes
- `SentinelCounter-derived-C1.diff` — unified diff base → derived amendment (`diff -u`, exit 1 = differences)
- `SentinelCounter-scratch-selftest.txt` — scratch selftest output (amended: `selftest cases=6 failures=0`, exit 0)
- `SentinelCounter-scratch-removal.txt` — scratch removal receipt

## Verdicts

SENTINEL exec-surface unchanged: yes (derivation; re-measure on the landed patch)
SENTINEL host mutation: none
SENTINEL scratch clean: yes
