# SentinelC1 — round-78 C1 TMPDIR / scratch-handling review (read-only)

## Candidate state at review
- `.ufo/waves/round-78/w1/successor/recheck-cwd-census.py`: **absent**. `successor/` holds only an empty `mutants/` dir. No candidate sha256 exists to record (N/A).
- Review therefore runs on the two available bytes: the frozen base `0687cca8:corpus/instruments/recheck-cwd-census.py` (sha256 `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`) and the round-77 reference `.ufo/waves/round-77/c1-amended-reference.py` (sha256 `18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33`, the stated proxy for the successor's selftest and TMPDIR design). Line numbers below are base unless marked r77.
- All attacks ran from scratch only (`/fast/scratch/hyaku/kasegi-r78/SentinelC1`), with a fake sensitive dir `sensitive/secret.txt` (0600 in 0700). Nothing host-level was touched. No sysctl, sudo, pacman, or chmod was run. No tool was installed. Python 3.14.8.

## Findings

**F1 — blocker (review scope): candidate not on disk.** Frozen claims P1–P7 and the candidate's TMPDIR refusal cannot be checked. Every verdict below is provisional and must be re-run on the landing bytes (the grep and audit commands in F11 apply unchanged).

**F2 — low (R-77-A, robustness not escape): nonexistent or non-directory TMPDIR raises a traceback, rc=1.** `base.py:65` (`mkdtemp(dir=env_tmp)` inside `run_foreign`), reached via `census` (`base.py:84`, `:103`) and `main` (`base.py:273`). r77 is identical in shape (`r77.py:66`).
```
$ env TMPDIR="$S/nonexist" python3 -B proxy/base.py --root $S/fx/t1 --lane $S/fx/t1 | tail -1
FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r78/SentinelC1/nonexist/recheck-cwd-jasovd_r'   rc=1
$ env TMPDIR="$S/afile" ... | tail -1
NotADirectoryError: [Errno 20] Not a directory: '.../SentinelC1/afile/recheck-cwd-5ratwp7l'
```
Fix required in the candidate: refuse in `main()` before any mkdtemp, including the `--selftest` path (`base.py:132` also calls mkdtemp), with exit 2 and a line starting `recheck-cwd: TMPDIR`.

**F3 — low (writes outside TMPDIR): empty TMPDIR silently falls back to `/tmp`.** `base.py:84` and `:132` use `os.environ.get("TMPDIR") or None`, so `""` becomes `dir=None` and tempfile uses its default list.
```
$ TMPDIR= python3 -c 'import tempfile;print(tempfile.gettempdir())'
/tmp
```
The counter then writes scratch under `/tmp`, which the lane rule forbids. Only the operator's environment can set this, so exposure is small. Candidate must treat `""` as refused (exit 2, `recheck-cwd: TMPDIR`), not as unset.

**F4 — low: relative TMPDIR resolves against cwd.** Measured: with `cwd=$S/rel-run` and `TMPDIR=relt`, scratch dirs were created at `rel-run/relt/recheck-cwd-*` (mode 700) and removed. `TMPDIR=.` with `cwd=fixture root` created `recheck-cwd-*` inside the census root for the duration of each recheck (T5b; listing during run shows it; removed after). A missing relative TMPDIR gives the same traceback as F2. Candidate should require an absolute path (`os.path.isabs`) and refuse otherwise.
```
TMPDIR=. (cwd=fx/t5b): root_listing_during_run: ['corpus','parent.txt','recheck-cwd-cm8lm20k','seen.txt']; after: ['corpus','parent.txt','seen.txt']
```

**F5 — note: symlink TMPDIR is followed, scratch lands in the link target.** `TMPDIR=$S/tmpdir-link -> $S/sensitive`: the mkdtemp dir `recheck-cwd-*` (mode 700) was created inside `sensitive/` and removed. Digest of `sensitive/` (names, modes, sizes) was identical before and after, and `secret.txt` stayed 0600. There is no chmod and no escape beyond the directory the operator's env names. An `isdir`-plus-`W_OK` check passes symlinks; that is acceptable and should not be "fixed" with chmod.

**F6 — note: newline in TMPDIR works.** `TMPDIR=$S/"nl\ndir"`: scratch created at `nl\ndir/recheck-cwd-*`, removed, rc as for a normal run. TMPDIR is never echoed into the output, so there is no output injection. A `\n` in a path is not a sandbox issue.

**F7 — pass: rmtree does not traverse symlinks.** `base.py:77` `shutil.rmtree(scratch, ignore_errors=True)`. A recheck value planted `dirlink -> sensitive/` and `filelink -> sensitive/secret.txt` inside its scratch. After census the links were unlinked, `sensitive/` digest was identical, and `tmp7` was empty. Same result on r77. Python 3.14's fd-based rmtree does not follow the links.

**F8 — low (repo-text driven, residue only): a recheck value can swap its own scratch for a symlink.** The value ran `mv "$P0" "$P0.moved"; ln -s sensitive "$P0"`. `rmtree` on the symlink is refused (`Cannot call rmtree on a symbolic link`) and swallowed by `ignore_errors=True`. `sensitive/` was unchanged, but `TMPDIR` retained `recheck-cwd-*` (the symlink) and `recheck-cwd-*.moved` (a real dir). Failure mode is residue, not deletion. Candidate need not change this; it is covered by F9.

**F9 — medium (pre-existing; candidate must not widen it): repo-authored text runs under bash -c with the full environment.** `base.py:70` `subprocess.run(["bash","-c",value], cwd=scratch, env=env, ...)`, `base.py:68` `env = dict(os.environ)`. Measured with `SENTINEL_SECRET=abc123` in the census environment and a value that runs `env`, writes outside scratch, and reads the fake sensitive file:
```
T9-exec-base => (0, 'RECHECK-CWD-RESULT conformant', 'outside_written:', True, 'env_leak_secret:', True, 'leak_read:', 'TOP-SECRET', 'sens_same:', True)
```
The `cd <LANE> && ` check (`base.py:90`, string prefix) is not a sandbox: a value `cd $S/fx/t9b && touch $S/exposure/after-prefix ; true` passes `noprefix=0`, runs, and creates the file. The operator ruling on running repo-text recheck values (round-73 Q, routed) is still pending; this exposure is unchanged by the candidate's TMPDIR work provided the `bash -c` call line and `env` copy stay as they are. **Candidate changes this exposure? Not verifiable (absent); the r77 proxy lines 71–72 and `env = dict(os.environ)` are identical to base, so the proxy adds none.** A candidate that adds `env` scrubbing or a different shell would change exposure and must be re-reviewed.

**F10 — low (availability): TIMEOUT does not bound pipe drain.** `base.py:70–75` applies `timeout=120` only to the bash process. A background child holding stdout keeps `capture_output` blocked after bash exits. Measured:
```
T10-grandchild-hang => (0, 'RECHECK-CWD-RESULT conformant', 'elapsed_s:', 12.0)   # value: (sleep 12 &) ; true
```
A longer background job would hang the census past TIMEOUT. Routed: candidate should run bash in its own session and kill the process group, or redirect output to a file in scratch.

**F11 — pass: no shell-out to sysctl, sudo, chmod, or host mutation.** Audit hook (`sys.addaudithook`) over census and selftest, base and r77:
```
T11-audit-base => AUDIT [('subprocess.Popen', 'bash')]
T11-audit-r77-selftest => AUDIT [('subprocess.Popen', 'bash')]  selftest cases=12 failures=0
```
Static grep of base and r77: no `sysctl|sudo|chmod|chown|os.system|shell=True|os.chmod` (only `subprocess.run(["bash","-c",…])`). Candidate-check command for landing bytes: `grep -nE 'sysctl|sudo|chmod|chown|os\.system|shell=True' <candidate>` must print nothing, and the audit hook above must list only `subprocess.Popen 'bash'`.

**F12 — note: TMPDIR cannot leak from one recheck into the next.** `run_foreign` sets `TMPDIR` on a copy (`base.py:68–69`); `os.environ` is never assigned. A recheck cannot change the census's own TMPDIR.

## Verdict
**Provisional: no-new-exposure** on the r77 proxy design (F2–F8, F10–F12). The verdict on the candidate is **not issued**: the candidate file is absent (F1). Re-run this review on the landing bytes with: (1) the TMPDIR matrix in F2–F4 (nonexistent, file, empty, relative, `.`, symlink, newline) expecting exit 2 and `recheck-cwd: TMPDIR` with no traceback for the refused cases; (2) the F7 and F8 rmtree checks; (3) the F11 grep and audit; (4) a diff confirming the `bash -c` line and `env = dict(os.environ)` are unchanged (F9).

Routed defects for the candidate: F2, F3 (empty string refused), F4 (absolute path required), F10 (pipe drain bounded). Exposure F9 is pre-existing and blocked on the pending operator ruling; it is not new.

## Scratch
`/fast/scratch/hyaku/kasegi-r78/SentinelC1` removed before yield. Nothing was written outside it except this file.
