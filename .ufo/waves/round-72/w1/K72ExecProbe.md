# K72ExecProbe — round 72 attempt 1

## Setup and command provenance

Axes: row coverage, exact admission/refusal evidence, bounded filesystem effects.

`S=/fast/scratch/hyaku/kasegi-r72/K72ExecProbe`; `L=$S/lane`.
Parent approved read-only `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive a34ce4c` instead of clone/checkout because the leaf role forbids mutating git. The tar was extracted to L; no `.git` was installed. Both instrument files were copied from the supplied working tree with `shutil.copyfile` (not edited).

Initial extraction with Python tarfile's `filter='data'` stopped with:
```text
tarfile.AbsoluteLinkError: '.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge' is a link to an absolute path
```
A subsequent setup encountered `FileExistsError` on the partial lane. After deleting that partial scratch lane, extraction excluded archive symlinks/hardlinks, avoiding absolute links into external trees. Successful setup output:
```text
ARCHIVE skipped_links=58
PIN figure-audit.py b146c81a29437aef2d4e91576782a2829570ac12f13888cad099d6081d1fefdc match=True
PIN derive-head-census.py 255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52 match=True
BASE-SHA256 182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603
```
The base hash came from `git -C <source> show a34ce4c:corpus/instruments/figure-audit.py`. **Base rc below is historical evidence from SentinelC1 §3's C/rc columns, not a base replay in this seat.** That C gate has the base hash above. SentinelC1's B column is the older round-70 gate, not the round-72 base.

Every table row was run through the candidate (including the already-refused controls, beyond the required admitted rows). For each row n, the harness wrote `$S/ledger-n.json`:
```json
{"figures":[{"id":"p","record":"g:1","recorded":"35","derive":"<expanded table derive>","want":"35"}]}
```
Invocation, with cwd L and empty stdin except row 25:
```text
TMPDIR=$S/tmp HYAKU_SCRATCH=$S/tmp PYTHONDONTWRITEBYTECODE=1 python3 $L/corpus/instruments/figure-audit.py --ledger $S/ledger-n.json --root $L
```
Actual driver used `subprocess.run(..., cwd=L, input=..., text=True, stdout=PIPE, stderr=PIPE, timeout=180)`. It did not use shell evaluation for derives.

Table notation expands literally: `P` = `python3 corpus/instruments/`, `O` = `$S/out`, `U` = `file://$S/out/secret.txt`, `E` = `corpus/instruments/fixtures/claim-package/exemplar`; every `$S`/`$L` was expanded to the absolute path above before ledger serialization. `R` is the **complete observed stderr line** `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=p`. `—` means no refusal line, empty stderr. rc 1 without R is admitted-but-stale, not refused.

## Per-row replay

| row | derive (macros expanded as above) | base rc | candidate rc | candidate refusal line | as-expected/DIFFERENT |
|---|---|---:|---:|---|---|
| 1 | `Pcapture-source.py -- O/a1.txt` | 1 | 1 | — | as-expected |
| 2 | `Pcapture-source.py --ur U` | 2 | 2 | R | as-expected |
| 3 | `Pcapture-source.py -u U` | 1 | 1 | — | as-expected |
| 4 | `Pcapture-source.py –url U` (U+2013) | 1 | 1 | — | as-expected |
| 5 | `Pcapture-source.py --id=x --url=U --out=O/a5.txt` | 2 | 2 | R | as-expected |
| 6 | `python3 -m http.server 8791` | 2 | 2 | R | as-expected |
| 7 | `python3 -m json.tool corpus/SOURCES.md` | 2 | 2 | R | as-expected |
| 8 | `Pok.py` (outside-target alias) | 2 | 2 | R | as-expected |
| 9 | `Pok.py --url U --out O/d2.txt` (outside-target alias) | 2 | 2 | R | as-expected |
| 10 | `Pcensusf.py` → `capture-source.py` | 2 | 1 | — | DIFFERENT |
| 11 | `Pfigure-audit.py --selftest` | 2 | 2 | R | as-expected |
| 12 | `Pfigure-audit.py -- --selftest` | 1 | 1 | — | as-expected; see isolated diagnostic |
| 13 | `env PYTHONPATH=/x Pgate-quote-audit.py --root .` | 2 | 2 | R | as-expected |
| 14 | `sort -T $S/td1 -S 1K < big.txt` | 1 | 1 | — | as-expected |
| 15 | `sort -T /tmp -S 1M < big.txt` | 1 | 1 | — | as-expected |
| 16 | `sort --compress-program=sh < big.txt` | 2 | 2 | R | as-expected |
| 17 | `sort --co=sh < big.txt` | 2 | 2 | R | as-expected |
| 18 | `sort --temporary-directory=$S/td2 -S 1K < big.txt` | 1 | 1 | — | as-expected |
| 19 | `git -c core.pager=sh show HEAD:corpus/SOURCES.md` | 2 | 2 | R | as-expected |
| 20 | `Pcapture-binding-check.py --root .` | 1 | 1 | — | DIFFERENT: not refused |
| 21 | `Pclaim-package-check.py E --json` | 1 | 1 | — | DIFFERENT: not refused |
| 22 | `Pr47-f30-gate.py --root . --work $S/w2` | 1 | 2 | R | as-expected |
| 23 | `Pr47-counters-selftest.py --base . --work $S/w3 --counter c1` | 1 | 2 | R | as-expected |
| 24 | `cat O/secret.txt` | 1 | 1 | — | as-expected |
| 25 | `cat` (gate stdin supplied synthetic token below) | 1 | 1 | — | as-expected |
| 26 | `Pclaim-package-check.py E -- --selftest` | 1 | 1 | — | as-expected |
| 27 | `Pclaim-package-check.py -- --selftest` | 1 | 1 | — | as-expected |
| 28 | `Pok.py --json O/alias.json` → `gate-quote-audit.py` | 1 | 2 | R | as-expected |
| 29 | `Pok.py --url U` (same `gate-quote-audit.py` alias as row 28) | 1 | 1 | — | DIFFERENT: not refused |
| 30 | `Pgate-quote-audit.py --json O/direct.json` | 2 | 2 | R | as-expected |
| 31 | `python3 -B corpus/instruments/capture-binding-check.py --root .` | 2 | 2 | R | as-expected |
| 32 | `Pfigure-audit.py -- --ledger $S/evil.json --root .` | 1 | 1 | — | as-expected |
| 33 | `Pfreeze-check.py --claims $S/claims-evil.json --tool-root $L --base $S/empty-base` | 1 | 1 | — | as-expected; shell marker executed |

All SentinelC1 ellipses/placeholders were concretized with the same displayed head and flags. Rows 8/9 used `ok.py` pointing to `$S/outside-evil.py` (whose body only prints `outside-probe`); row 10 used `censusf.py` pointing to `capture-source.py`. Before row 28, `ok.py` was replaced with a relative symlink to `gate-quote-audit.py`. Row 29 follows the table's literal “same alias”; its ambiguity is separately measured below. Positional directory placeholders in rows 21/26 use E, row 33 uses the empty scratch base. Row 32's evil ledger derives `Pcapture-source.py --out O/nested.txt` with the same one-figure shape.

The sort input `big.txt` was deliberately only `z\nb\na\n` (six bytes): this measures admission, not round-71's write amplification. Keeping row 15's literal `/tmp` spelling without a spilling input avoids writes there; the trace below confirms the measured run. No network URL was fetched; file URLs name the synthetic scratch fixture.

## Retained output lines and discriminating findings

Every admitted run printed `FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1`; every refused run had empty stdout and stderr R.

Rows 1, 3, 4, 10, 26, 27, 29, 32 printed:
```text
FIG p recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale
```
Row 20 retained lines (the full result also contained per-round MANIFEST rows):
```text
FIG p recorded=35 derived=MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=85 bound=85 unbound=0 want=35 stale
```
Row 21's complete FIG line:
```text
FIG p recorded=35 derived={"exit": 0, "fail": 0, "package": "corpus/instruments/fixtures/claim-package/exemplar", "pass": 8, "rules": [{"detail": "files=6,missing=0,bad=0", "id": "R-FILES", "verdict": "pass"}, {"detail": "artifacts=4,positive=3,digest-bad=0,escape=0", "id": "R-MANIFEST", "verdict": "pass"}, {"detail": "artifacts=4,receipts=4,missing=0,digest-mismatch=0", "id": "R-REDACT", "verdict": "pass"}, {"detail": "chain=3,grant-miss=0,signal-bad=0,head=bound", "id": "R-CUSTODIAN", "verdict": "pass"}, {"detail": "agents=2,commands=9,pin=ok,effects=none,secrets=ok", "id": "R-PROVENANCE", "verdict": "pass"}, {"detail": "manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named", "id": "R-STATUS", "verdict": "pass"}, {"detail": "scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0", "id": "R-REPORT", "verdict": "pass"}, {"detail": "files-scanned=ok,symlinks=0,oversize=0,hits=0", "id": "R-NOSECRET", "verdict": "pass"}], "rules_count": 8, "verdict": "WELL-FORMED"} want=35 stale
```
Rows 20/21 contradict the supplied expectation of refusal; these observed runs execute the heads successfully and remain stale only because want=35. Row 10 is an additional changed admission: the unknown invoked alias now reaches its realpath target, whose missing required arguments exit 2.

Rows 14/15/18 printed:
```text
FIG p recorded=35 derived=a
b
z want=35 stale
```
Rows 24/25 printed (token is authored synthetic fixture data, not host session material):
```text
FIG p recorded=35 derived=SECRET-STDIN-TOKEN-9f3a want=35 stale
```

### Row 12 fixture isolation

The first replay, with row 10's extra `censusf.py` still installed in instruments, printed:
```text
FIG p recorded=35 derived=UNAVAILABLE reason=derive-exit-1 stale
```
After removing that extra alias from scratch and running the **same ledger/command**, the selected observed lines were:
```text
ROW12 ISOLATED rc=1
stdout_sha256=ba5babef8e3688c017e3fb173b47a893dd4d9db7a7132dfca6ee6f115d999859
selftest case=python-census-covers-instruments exit=0 want=0 verdict=pass
selftest cases=110 failures=0 want=35 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
stderr=''
```
The separator still permits the nested gate's 110-case selftest; the outer rc remains 1 because its complete stdout is not 35. No standalone selftest was substituted for this derive.

### Row 29 alias ambiguity

Keeping the exact row-29 argv but replacing `ok.py`'s target with `capture-source.py` (as SentinelC1 residual §5.4 describes) produced candidate rc 2, empty stdout, and:
```text
FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=p
```
Thus the capture-source alias interpretation meets the expected refusal; the section-3 table's “same alias” interpretation (`gate-quote-audit.py`) does not. No base rc is claimed for this extra diagnostic.

### Row 33 routed shell execution

Fixture claims JSON:
```json
{"schema":"kasegi-round-claims-v2","claims":[{"id":"p","counter_cmd":"printf pwned-from-claims > /fast/scratch/hyaku/kasegi-r72/K72ExecProbe/mark/freeze.mark; printf 'before=0\\n'; : {tree}","expect_before":"before=0","expect_after":"after=1"}]}
```
Observed candidate stdout and marker read:
```text
FIG p recorded=35 derived=claim p base_read=before=0 verdict=ok
freeze-check claims=1 base_ok=1 exit=0 want=35 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
MARKER pwned-from-claims
OUT-FILES ["secret.txt"]
```
This reproduces the routed row-33 capability without `--work`: claims data executed and wrote only the designated scratch marker. `OUT-FILES` also shows row 1's `a1.txt` and row 28's `alias.json` were absent after the replay.

### Row 15 outside-write guard

Executed the same gate/ledger under `strace -f -qq -e trace=execve,openat,unlink,unlinkat -o $S/sort15.trace` with the same cwd/environment. rc=1, same sorted FIG output, empty stderr. All observed write-capable/open-create/unlink trace lines:
```text
TRACE_WRITE_LINES=3
1851139 openat(AT_FDCWD, "/fast/scratch/hyaku/kasegi-r72/K72ExecProbe/tmp/b5m5yd5u", O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600) = 4
1851139 unlink("/fast/scratch/hyaku/kasegi-r72/K72ExecProbe/tmp/b5m5yd5u") = 0
1851139 openat(AT_FDCWD, "/fast/scratch/hyaku/kasegi-r72/K72ExecProbe/tmp", O_RDWR|O_EXCL|O_NOFOLLOW|O_CLOEXEC|O_TMPFILE, 0600) = 4
```
No `/tmp` write appeared in this measured trace. No tool installs/updates were performed; `command -v strace` returned `/usr/bin/strace`.

## Scope and retained evidence

33 candidate rows measured, plus the capture-source alias diagnostic and the two fixture/trace diagnostics. Four table DIFFERENTs: 10, 20, 21, 29. Rows 22/23/28 refuse; row 29 refuses under the alternate capture-source interpretation. Rows 14/15/18 and 33 remain admitted as requested. Evidence retained here is the exact selected output above; full initial harness output is tool artifact `artifact://157567` (long rows 20/21 were read in full). Scratch probes and fixtures are disposable, not report prerequisites. No lane implementation changes, no commits, no external-source changes, no broad build/lint/test gate execution.

Cleanup executed `rm -rf -- "$S"; test ! -e "$S"` with the EXIT trap retained; observed:
```text
SCRATCH-REMOVED=/fast/scratch/hyaku/kasegi-r72/K72ExecProbe
```
