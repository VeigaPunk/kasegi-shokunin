# S097 — draft registry row (NOT landed; L1 decides admission)

Scope: own-work, tier A. Opened 2026-11-04 from committed bytes at base `d74be00a82c8c2962a0b78442c5daea3af0adaae`.
Target file `corpus/instruments/figure-audit.py` has sha256 `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`, identical to the r63 candidate digest (`git show fdccc6d…` carries a different digest `a0ddbd40…`; the candidate landed after fdccc6d). Receipt: `native-exit-absolute-paths-r64.txt` (run-utc 2026-11-04T18:38:06Z) and `base-probe-recon-r64.txt` (run-utc 2026-11-04T18:37:31Z).

Row (one line, registry column order: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by):

```
| S097 | Kasegi own-work command-aware upstream-exit predicate — corpus/instruments/figure-audit.py at d74be00 | own-work | A | This lane's local figure runner: which positive upstream exit statuses an evidence derive may ignore, with grep exit1 as the only no-match status; not POSIX-complete, not a sandbox, not external policy | corpus/instruments/figure-audit.py L42-L43 ("Upstream exit1 and negative signal statuses remain" / "ignored, preserving grep\|wc zero-count derives"); L107 ("if p.returncode > 1:"); selftest controls L412 and L419; sha256 15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997; opened 2026-11-04; receipts .ufo/waves/round-64/w1/SourceLedger/base-probe-recon-r64.txt | Treat grep exit1 as no-match only; name every other positive upstream status only after measuring that command's native value on the host; keep negative signal statuses as explicit residuals. | proposed-not-landed | 2026-11-04 | on-release | corpus/lessons/round-64.md |
```

Companion row (spec, L1 decision whether to register as S098; not counted here):

```
| S098 | IEEE Std 1003.1-2017 (POSIX Issue 7) grep, cat utility pages — https://pubs.opengroup.org/onlinepubs/9699919799/utilities/grep.html ; …/utilities/cat.html | spec | A | Only the grep and cat EXIT STATUS sections; not other utilities, not GNU option behaviour | fetched 2026-11-04 via reader; section EXIT STATUS in each page; grep: "No lines were selected." and "An error occurred."; cat: "All input files were output successfully." and "An error occurred." | grep exit 1 is a defined no-match; cat's nonzero exit is defined only as ">0", so cat exit1 is a host fact, not a spec value | proposed-not-landed | 2026-11-04 | on-release | corpus/lessons/round-64.md |
```

Observed native values (receipts above, GNU coreutils 9.12 / GNU grep 3.12 at /usr/bin, resolved by the instrument's own subprocess PATH lookup):

| command on missing input | native exit | base (d74be00) derive verdict | candidate expectation (inference, not measured) |
|---|---|---|---|
| `cat missing.txt \| wc -l` | 1 | green 0 | stale, derive-upstream-exit-1 |
| `cat g.txt missing.txt \| wc -l` (partial) | 1 | green 1 | stale, derive-upstream-exit-1 |
| `cut -c1 missing.txt \| wc -l` | 1 | green 0 | stale, derive-upstream-exit-1 |
| `head missing.txt \| wc -l` | 1 | green 0 | stale, derive-upstream-exit-1 |
| `tail missing.txt \| wc -l` | 1 | green 0 | stale, derive-upstream-exit-1 |
| `sha256sum missing.txt \| wc -l` | 1 | green 0 | stale, derive-upstream-exit-1 |
| `ls missing.txt \| wc -l` | 2 | stale, derive-upstream-exit-2 | stale, derive-upstream-exit-2 (unchanged) |
| `sort missing.txt \| wc -l` | 2 | stale, derive-upstream-exit-2 | stale, derive-upstream-exit-2 (unchanged) |
| `grep absent g.txt \| wc -l` (no match) | 1 | green 0 | green 0 (preserved) |
| `grep absent missing.txt \| wc -l` | 2 | stale, derive-upstream-exit-2 | stale, derive-upstream-exit-2 (unchanged) |

Correction to the wave prompt: the assignment's expectation "base greens want0" is wrong for `ls` and `sort` missing; they are already base-stale (exit2). They are controls, not repairs.
