# ExecCollector — round 64 predata collector

Axes: depth:verifiability only; prefreeze instrument construction, no candidate scoring, no freeze claim. No production edits, git/jj mutations, installs, delegation, builds or lane gates. No tool was installed or updated (RULES.md read; nothing needed beyond host python3 3.14.8, /usr/bin/python3). No LSP interface is mounted in this seat's inventory; navigation used read/grep, not an empty LSP response.

## Deliverables

All under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-64/w1/ExecCollector/`:

- `c1-probes-r64.py` SHA256 `fe9ba177cfdf3722a2946b5f29dc815c6df8db572221cc3489efd5044e2f196b` — CLI `--instrument ABS --work ABS --mode base|candidate` plus `--selfcheck`. Stdlib only; needs PATH python3 cat grep wc cut head tail ls sort sha256sum; no shell, no Git. Exit 0 exact / 1 mismatch / 2 fail-closed (`HARNESS-ERROR ...`). Work must be absolute, a disposable subdirectory >=2 levels under `/fast/scratch/hyaku/kasegi-r64`; missing instrument/dependency or unusable work fails closed; an instrument inside work is rejected before fixtures are written and byte-checked again after; existing files are never cleared; only the fresh private run directory is removed. The instrument is invoked exactly once per run with one 18-figure ledger; its whole stdout (every FIG record plus the `FIGURE-AUDIT figures/ok/stale/exit` trailer), process exit and empty stderr are compared exactly, record by record.
- `base-receipt.txt`, `candidate-receipt.txt`, `selfcheck-receipt.txt`: each the untouched merged stdout+stderr of exactly one collector invocation, with run-utc, argv JSON, PROBE/NATIVE/EXPECT establishment lines, the raw instrument stdout and PASS/FAIL records.
- `base-command.json`, `candidate-command.json`, `selfcheck-command.json`: exact invoking argv, observed exits, hashes, lane revision `d74be00a82c8c2962a0b78442c5daea3af0adaae`.

## Independent native establishment

Each probe's per-stage exit codes and stdout are measured by the collector's own staged subprocess runner (never the instrument), and `want` values are asserted against that native stdout whenever the mode rule expects green; drift fails closed exit 2. Measured this host (piped to `wc -l`, final stage rc0):

| upstream head | native rc | stdout |
|---|---|---|
| `cat nosuch-r64.txt` | 1 | 0 |
| `cat one.txt nosuch-r64.txt` (partial) | 1 | 1 |
| `cut -d, -f1` | 1 | 0 |
| `head -n 1` | 1 | 0 |
| `tail -n 1` | 1 | 0 |
| `ls` | 2 | 0 |
| `sort` | 2 | 0 |
| `sha256sum` | 1 | 0 |
| `grep zzz-absent one.txt` | 1 (no-match) | 0 |
| `grep '[' one.txt` (invalid regex) | 2 | 0 |
| SIGTERM python counter | -15 | 0 |

## Probe set and exact expectations

18 probes = the eight new-probe shapes plus ten retained controls. Mode rules: base = current production rule (nonzero final wins `derive-exit-N`, then first upstream rc>1 `derive-upstream-exit-N`, upstream exit1 and negatives ignored); candidate = final precedence and negatives unchanged, plus first upstream positive rc rejected as `derive-upstream-exit-N` except rc1 from a stage whose command basename is exactly `grep`.

| probe | base expect | candidate expect |
|---|---|---|
| cat-missing / cat-partial-missing / cut-missing / head-missing / tail-missing / sha256sum-missing | ok (want 0; partial want 1) | stale `derive-upstream-exit-1` |
| ls-missing / sort-missing | stale `derive-upstream-exit-2` (retained >1 regression, not a flip) | stale `derive-upstream-exit-2` |
| grep-no-match (rc1 upstream) | ok | ok (grep exception) |
| cat-success / sort-success | ok | ok |
| and-concatenated (`1\n1`) | ok | ok |
| and-stops-on-failure | stale `derive-exit-1` | stale `derive-exit-1` |
| grep-invalid-upstream | stale `derive-upstream-exit-2` | stale `derive-upstream-exit-2` |
| final-grep-no-match | stale `derive-exit-1` | stale `derive-exit-1` |
| final-precedes-upstream (final7 over upstream2) | stale `derive-exit-7` | stale `derive-exit-7` |
| upstream-negative-signal (-15) | ok | ok |
| final-negative-signal (-15) | stale `derive-exit--15` | stale `derive-exit--15` |

## Observed results

- BASE construction control (production `corpus/instruments/figure-audit.py` SHA256 `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`, the r63-integrated bytes): exit0, `HARNESS probes=18 failures=0 mode=base`, instrument exit1 observed as expected (7 stale controls), trailer `FIGURE-AUDIT figures=18 ok=11 stale=7 exit=1` matched exactly. No base expectation was falsified; the six exit1 heads are asserted green in base exactly as measured.
- CANDIDATE mode against the same production bytes (no r64 candidate file exists yet; none required): exit1, `HARNESS probes=18 failures=7 mode=candidate` — precisely the six would-be flips (each observed `derived=0/1 ok` where `derive-upstream-exit-1 stale` is required) plus the ok/stale trailer delta (`ok=11 stale=7` vs required `ok=5 stale=13`). ls/sort and all retained controls already agree with the candidate rule. This is the pre-candidate red baseline; a real candidate must drive this to `failures=0` return0.
- SELFCHECK: exit0, `HARNESS selfcheck cases=9 failures=0`. Cases: missing instrument → exit2 `HARNESS-ERROR FileNotFoundError`; unusable work (regular file) → exit2 `HARNESS-ERROR FileExistsError`, sentinel byte-preserved; instrument under work → exit2 `instrument-under-work`, instrument byte-preserved; always-green counterfeit (fabricated all-ok output, candidate mode) → exit1 rejected; empty output → exit1 rejected; nonzero exit (7) with byte-perfect clean summary → exit1 rejected on the exit-code record alone (`failures=1`); pristine control → exit0 `failures=0 mode=base`; plus sentinel/instrument preservation assertions.

## Verification commands (main agent / L1)

```
/usr/bin/python3 .ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py --instrument corpus/instruments/figure-audit.py --work /fast/scratch/hyaku/kasegi-r64/<seat>/base --mode base
/usr/bin/python3 .ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py --instrument <candidate> --work /fast/scratch/hyaku/kasegi-r64/<seat>/cand --mode candidate   # must print HARNESS probes=18 failures=0 mode=candidate, exit0
/usr/bin/python3 .ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py --instrument <candidate> --work /fast/scratch/hyaku/kasegi-r64/<seat>/sc --selfcheck
```

verify-r64.py compatibility: its collector task passes `--work <its-work>/collector` (guard satisfied, dir created if absent), cwd is its extracted tree (unused; the instrument is addressed by absolute path with a private ledger and root), and expects collector exit0 under `--mode candidate` with a real candidate — reachable only after the six flips land.

## Bounds, risks, handoff

Scratch `/fast/scratch/hyaku/kasegi-r64/ExecCollector` was used for the three runs above and removed after receipts were saved. Not a sandbox and no general error policy claim: the collector trusts PATH binaries, cannot detect a counterfeit that fabricates exact measured output AND exits correctly (it would need this host's native numbers), and grade's record splitter assumes FIG/FIGURE-AUDIT line prefixes. The and-stops probe's ledger `want` is nominal ("1") because a natively failing && group prints nothing; the drift assert is deliberately scoped to green-expected probes so a must-fail probe is never falsified by its own want. Empty-Git/GIT_* hygiene is retained from r63 although no probe uses Git. No negative-final/derive-exit--15 formatting is claimed portable beyond this host's repr (`derive-exit-%d % -15`). Per KasegiR64/ReviewPredicate-3 relay: the intended-eight was reinterpreted before freeze — ls/sort are encoded as retained >1 regressions (base stale, candidate stale), the six exit1 heads are the flips; `HARNESS probes=18 failures=F mode=<mode>` is the bound summary shape and the selftest-style case count is probes=18 (+ trailer/exit/stderr records in failures) with selfcheck cases=9.

Self-evaluation: accuracy4 (single-invocation raw receipts, measured per-stage codes, exact per-record verdicts); completeness4 (eight shapes, ten controls, selfcheck, base control, red baseline); clarity4 (expectation rules and residual risks stated); actionability4 (exact rerun commands and required candidate summary supplied; freeze stays L1's); conciseness4 (raw evidence linked, not duplicated). Average4.0. Highest-value next action: run this collector against ExecPipeline's r64 candidate before freeze; MutationCollector may attack these exact bytes (`fe9ba177…`).

Report: .ufo/waves/round-64/w1/ExecCollector.md
