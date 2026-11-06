# SentinelC1 — attack surface of the C1 candidate (round 79, attempt 1, w1)

Seat: security/robustness review, read-only. No lane byte, corpus byte, instrument or frozen byte
was modified; nothing was installed. Everything below was executed on exact scratch copies under
`S=/fast/scratch/hyaku/kasegi-r79/SentinelC1` (deleted before yield).

## 0. Objects under test (sha256 verified at probe time)

| object | sha256 | note |
|---|---|---|
| `.ufo/waves/round-79/c1/recheck-cwd-census.py` | `eda49d32…091f2f` | candidate (frozen) |
| `.ufo/waves/round-79/c1/mutbat.py` | `735d2336…3ea9` | counter (frozen) |
| `.ufo/waves/round-79/c1/mutant-table.json` | `0cb50dc8…31e2` | 19 rows (frozen) |

Scratch copies were `cp -p` of these files; every sha matched, so results transfer to the frozen
bytes. Static surface (P7 limb): exactly one `subprocess.run(` and one `"bash", "-c"`; the only
`/tmp` occurrence in either file is the docstring sentence "no path is hard-coded under /tmp".

## 1. Findings (severity, exploit path, evidence, impact, remediation)

### F-1 — BLOCKER (verification integrity): the frozen counter scores the frozen candidate `killed=18`, not 19

Not a memory-safety bug; it is the failure mode this sentinel exists for — a claim whose
acceptance measurement does not reproduce on its own frozen artifacts.

- Surface: `mutbat.verdict()` — `EXC_RE = ^selftest case=\S+ FAIL .*exception` runs before the
  class gate, and `counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")`.
- Path: row `K-T1` (`class: "assertion"`) deletes `tmpdir_refused()`; the selftest's own
  `except` handler reports `stdout="exception=FileNotFoundError(2, …)"`, so the FAIL detail contains
  the word `exception` → `EXCEPTION-KILL` → `counted=no` → `dirty=1`.
- Evidence (byte-identical scratch copy of the target, frozen table, two consecutive runs):
  ```
  MUTANT K-T1 verdict=EXCEPTION-KILL rc=1 fails=1 counted=no
  MUTBAT target_sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0
  rc=1
  ```
  The mutant **is** genuinely killed (`selftest case=tmpdir-refusal FAIL ret=-99 stdout="exception=FileNotFoundError(2, 'No such file or directory')"`, rc1); only the tally refuses it. The row's own `expect` text already predicts this mode ("exception caught as ret=-99").
- Impact: claim P3 requires the literal `killed=19 survived=0 dirty=0`; the frozen counter cannot print it. Landing the candidate turns the gate red, and the kill rule makes that `C1 NOT VERIFIED`.
- Smallest remediation (outside this seat's authority — table, counter and claim bytes are all frozen): reclassify `K-T1.class` to `"exception"`, or scope `EXC_RE` to a detail the counter itself emits rather than text the target prints. Corroborated independently by `ExecC1Battery.md` §3; my run adds only an independent reproduction.

### F-2 — MEDIUM (process cleanup): a timed-out recheck's descendants survive, and the census still says `conformant`

- Surface: `run_foreign()` — `subprocess.run(["bash","-c",value], …, timeout=120)` with no
  `start_new_session=True` / `os.killpg`. `subprocess.run`'s timeout kills only the direct `bash`
  child on POSIX.
- Path: a `recheck:` value that backgrounds work — `cd <root> && (sleep 6; touch <root>/late-marker)`.
  The census times the entry out (`exit_other=1`), deletes the scratch, prints `conformant`, exits 0;
  the orphan subshell keeps the lane-root cwd rights and writes afterwards.
- Evidence (probe copy with `TIMEOUT = 120` → `2`; frozen bytes untouched):
  ```
  RECHECK-CWD entries=1 … exit_other=1 …
  RECHECK-CWD-RESULT conformant          rc=0
  marker_at_return: absent
  marker_after_8s:  present  (late-marker, written by the orphan after the verdict)
  ```
- Impact: `TIMEOUT` bounds the counter, not the command. A hanging recheck can keep mutating the
  lane root while the gate has already recorded the tree as conformant; the mutation is unattributed.
- Remediation: run each value in its own process group (`start_new_session=True`) and `killpg` on
  `TimeoutExpired` before the scratch is removed.

### F-3 — MEDIUM-LOW (resource): `capture_output` is unbounded; one entry can OOM the counter

- Surface: `run_foreign()` keeps the whole stdout+stderr of every recheck in memory
  (`capture_output=True`), 92+ entries, `TIMEOUT=120`.
- Evidence: single entry writing 200,000,000 bytes →
  `Elapsed 0:00.35`, `Maximum resident set size 599868 kbytes` (~3x output), verdict `conformant`.
- Impact: a runaway entry (`yes`) can exhaust memory inside 120 s and take the gate process down
  (exit with a MemoryError traceback, not a per-entry verdict). Lane content is trusted, so this is
  a robustness/DoS limit, not an escalation.
- Remediation: redirect child stdout/stderr to a scratch file with a size cap, or drain with a
  bounded read loop; classify the overflow as `exit_other` with a named line.

### F-4 — LOW-MEDIUM (refusal completeness): the guard checks only `isdir`, so two other odd TMPDIR values still traceback

- Surface: `tmpdir_refused()` = `os.environ.get("TMPDIR") is not None and not os.path.isdir(tmp)`.
- Path A (unwritable dir): `TMPDIR=<dir chmod 0555>` passes the guard, then
  `tempfile.mkdtemp(prefix="recheck-cwd-selftest-", …)` raises.
  ```
  PermissionError: [Errno 13] Permission denied: '…/rotmp/recheck-cwd-selftest-vjdhxkw7'
    (census.py:242 in selftest)
  ```
  rc=1, no `recheck-cwd: TMPDIR` line, 0 leftovers.
- Path B (TOCTOU): the guard runs once at `main()` entry, then `census()` runs for minutes. With the
  directory removed between the guard and the first `mkdtemp` (rmdir injected in a probe harness):
  `uncaught= FileNotFoundError [Errno 2] … /recheck-cwd-ssmx5jll`. On the CLI that is a traceback.
- Impact: the class of defect P4 was written to remove (base: rc1 traceback) still exists for values
  the guard cannot see: not-writable, vanished-mid-run, ENOSPC. Fails closed in both cases.
- Remediation: probe writability (`os.access(tmp, os.W_OK)` plus a real `mkdtemp` in `main()` before
  the run) and wrap `run_foreign`'s `mkdtemp` in the same named refusal path.

Other odd values behave (`P-B*`): nonexistent, nonexistent-relative, regular file, dangling symlink →
rc2, stdout empty, one named stderr line, no traceback; empty string → rc2 (stricter than `tempfile`,
which would have used `/tmp`; note the message renders as `TMPDIR  is not a directory`, double space);
existing relative dir → rc0 and cleaned; symlink to dir → rc0; path with spaces → see F-5.

### F-5 — LOW (injection): the TMPDIR value reaches `bash` unquoted in the selftest fixtures

- Surface: fixtures interpolate paths into executed commands:
  `"recheck: cd %s && true\n" % lane1`, `touch %s/first-ran`. No `shlex.quote`.
- Path: a directory **name** carrying shell syntax is accepted by the `isdir` guard and then executed.
- Evidence: `TMPDIR="$S/p/x;touch \$SENTINEL_MARK;#"`, `SENTINEL_MARK=$S/p/MARK` →
  `MARK_created_by_TMPDIR_name=yes` (`-rw-r--r-- … MARK`), selftest rc=1.
  The same unquoted interpolation is why `TMPDIR="dir with spaces"` yields
  `selftest cases=15 failures=7`: `cd /…/dir with spaces` is two arguments.
- Impact: an environment value becomes a command line. The value is operator-controlled, and the
  failure direction is closed (rc1, never a false `failures=0`), so severity stays low — but the
  primitive is real and the same code shape will be reused by future instruments.
- Remediation: `shlex.quote()` every interpolated path in fixture command strings (and compare the
  prefix against a quoted lane string); this also restores the spaces case.

### F-6 — LOW (log injection): raw values forge log lines, never the verdict

- `TMPDIR=$'/nonexistent-xyz\nTraceback (most recent call last):\nFAKE'` → stderr becomes
  ```
  recheck-cwd: TMPDIR /nonexistent-xyz$
  Traceback (most recent call last):$
  FAKE is not a directory$
  ```
  A consumer that greps combined output for `Traceback` (exactly `mutbat.verdict()`'s rule) can be
  moved by the value it passed in.
- A knowledge **filename** containing newlines forges a complete per-entry line inside the census
  output: `ENTRY a` / `ENTRY fake.md noprefix=0 foreign_exit=0` / `b.md noprefix=1 foreign_exit=2`.
- Bound (verified negative result): the authoritative `RECHECK-CWD …` summary and
  `RECHECK-CWD-RESULT` are computed from the counts dict, and the selftest's `ok/FAIL` lines cannot be
  forged by an entry's output — `run_foreign` captures both pipes, so nothing a recheck prints reaches
  the census's stdout.
- Remediation: `print` with `%r`/JSON escaping for TMPDIR and for entry names; have reviewers read the
  summary only.

### F-7 — LOW / INFORMATIONAL (exec boundary): every `recheck:` value runs as the operator with the full environment, and the glob follows symlinks

- `env = dict(os.environ)` is passed through; a fixture entry wrote the caller's variable to disk:
  `leaked=[TOKEN-abc123]`. `cwd` is the TMPDIR scratch, but the value itself may `cd` anywhere.
- `glob.glob(kdir/*.md)` follows symlinks: `corpus/knowledge/evil.md -> …/outside.md` outside
  `--root` was read **and executed** (`symlink-ran` created), census still `conformant`.
- Impact: the trust boundary is "whoever can write `corpus/knowledge/` runs commands as the gate
  operator and can read its environment". That is the documented purpose of a Q10 census, so this is a
  boundary statement, not a regression — but it must be written down next to the instrument.
- Remediation: document the boundary in the instrument docstring (and the README row); optionally pass
  an allowlisted environment (`PATH`, `HOME`, `TMPDIR`) and skip non-regular entries (`os.path.islink`).

## 2. Properties that held (fail-closed evidence, not assumptions)

| property | probe | result |
|---|---|---|
| F0: unreadable `__file__` fails closed | import module, `chmod 000`, call `selftest()` | `gate-wiring FAIL findings=["F0:unreadable:PermissionError(13, …)"]`, `gate-checkids FAIL side_logs=[[True],[False],[True]]`, `cases=15 failures=2`, rc1 — no silent pass |
| F0 via stdin (`python3 - --selftest < census.py`) | no real `__file__` | `F0:unreadable:FileNotFoundError('<stdin>')`, failures=2, rc1 |
| F0 cannot be reached by running the file directly | `chmod 000` then execute | interpreter refuses (`can't open file … Permission denied`, rc2); no code runs |
| P4 form | `TMPDIR=/nonexistent-kasegi-r79 … --selftest` | rc2, stdout empty, one `recheck-cwd: TMPDIR …` stderr line, no traceback |
| scratch cleanup on exception | inject `RuntimeError` from `census()` mid-selftest | `propagated= injected failure mid-selftest`, `leftovers= 0` |
| scratch cleanup on success | baseline run | `cases=15 failures=0`, rc0, `0` leftovers in TMPDIR |
| no `/tmp` literal | grep both files | only the docstring sentence |
| counter writes confined | static read + run from an isolated cwd | writes only under `--work` (`dir=work`); no cwd pollution |
| counter baseline limb is load-bearing | `--work "…/work with spaces"` | `baseline=bad … rc=1` (a spaces path cannot turn into 19 false kills) |
| error paths are named | `--root /no/such/root`; `--root` with no value | named rc1 and usage rc2, no traceback |

## 3. Routed defects for the L1 (no rule change made here)

1. **F-1** — frozen `mutant-table.json` row `K-T1.class` is `assertion` while its only kill mode is a
   caught exception; P3 is unreachable as frozen (`killed=18 dirty=1 rc1`). Independent reproduction of
   `ExecC1Battery.md` §3. A finding, not a verdict edit.
2. **F-2** — no process-group kill on timeout: timed-out descendants outlive the verdict.
3. **F-3** — unbounded output capture (≈3x RSS).
4. **F-4** — refusal covers `not isdir` only: unwritable and vanished TMPDIR still traceback.
5. **F-5** — unquoted path interpolation into shell in fixture commands (TMPDIR-name command execution).
6. **F-6** — raw TMPDIR and entry filename interpolation into log lines (verdict not forgeable).
7. **F-7** — exec boundary: full environment inheritance and symlink-following glob, undocumented.

Scope note: this seat judged only the C1 candidate surface. C1's predicates were not scored here
beyond reproducing the counting command; P1/P2/P5/P6/P7 and the C2 axis were out of scope.
