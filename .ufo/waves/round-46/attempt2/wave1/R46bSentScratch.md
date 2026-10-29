VERDICT: BROKEN

# R46bSentScratch — scratch-discipline audit (round 46, attempt 2)

Seat: R46bSentScratch (sentinel, leaf; no delegation). Scope: scratch discipline of the round's
new instruments + attempt-2 drafts (hardcoded `/tmp` / `/fast` paths, `mkdtemp` without `dir=`,
`subprocess` without `timeout=`, anything that writes outside `--work`), plus the two committed
selftests' dead `PURE` defaults (routed defect class) with the exact one-line fix per file.

All paths below are under the lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/` unless stated otherwise.
Scratch for this seat: `/fast/scratch/hyaku/kasegi-r46/R46bSentScratch/` (removed on exit).

**Findings summary**

| # | Severity | Finding | Where |
|---|---|---|---|
| F1 | HIGH | Dead `PURE` default: both committed selftests name a path that does not exist; a bare invocation is an unhandled `FileNotFoundError` traceback | `corpus/instruments/r46-counters-selftest-c1.py:47,568`; `...-c2.py:47,275` |
| F2 | MEDIUM | The C2 selftest has no `--work` flag, ignores `TMPDIR`, and writes into a hardcoded shared directory named after an attempt-1 wave-2 seat — so the battery's C2 half never keeps its scratch under `--work` | `corpus/instruments/r46-counters-selftest-c2.py:282`; `corpus/instruments/r46-mutbat.py:102-105` |
| F3 | LOW | The only committed round-46 `subprocess` call without `timeout=`, plus the same class in a shell script; both take tree-supplied input. No hang demonstrated — severity is defence-in-depth, not a live DoS | `corpus/instruments/r46-c1-gate.py:232`; `corpus/instruments/r46-plain-measure.sh:25` |
| F4 | LOW | Attempt-2 reviewer drafts: hardcoded scratch path, two `subprocess.run` without `timeout=`, no exit cleanup | `.ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/attack-h1.py:12,27,31`; `R46bRevF29H2H3.draft/build-defects.py:5` |

Checked and **clean**: no `mkdtemp` without `dir=` anywhere in the round's `r46*` files; no
hardcoded `/tmp` in the committed round-46 instruments; the committed `r46-f29-gate.py` writes
neither into the tree it grades nor into the fleet root; the census helper it shells out to
writes stdout only. Evidence for each is in the "Clean results" section.

**L1 action summary.** F1's one-line fix per file is ready to land at integration (the committed
counters and the frozen claims are read-only for every seat; the selftests are this round's C1
surface). F3 carries a coupling the L1 must honour: any erratum that adds a timeout to
`r46-c1-gate.py:232` breaks the frozen battery's `M20` mutant unless the battery's old-substring
is updated in the same landing — see F3's "L1 coordination note".

---

## F1 (HIGH) — Both committed selftests default `--pure` to a path that does not exist: the "dead PURE default"

**Attacked:** the default value of `--pure` in the two committed round-46 selftests, and the
behaviour of a bare invocation (no `--pure`) that a grader or CI would perform.

**Evidence — the default is dead.** Both files name a path that is not on disk:

```
$ grep -n 'PURE = \|default=PURE' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py
corpus/instruments/r46-counters-selftest-c1.py:47:PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
corpus/instruments/r46-counters-selftest-c1.py:568:    ap.add_argument("--pure", default=PURE)
corpus/instruments/r46-counters-selftest-c2.py:47:PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
corpus/instruments/r46-counters-selftest-c2.py:275:    ap.add_argument("--pure", default=PURE)
```

The named directory does not exist; the live export for this round is `.../L1/pure2`:

```
$ ls -d /fast/scratch/hyaku/kasegi-r46/L1/pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
ls: cannot access '/fast/scratch/hyaku/kasegi-r46/L1/pure': No such file or directory
/fast/scratch/hyaku/kasegi-r46/L1/pure2
```

**Evidence — a bare invocation crashes (not a clean "give me --pure" error).** C1:

```
$ TMPDIR=$S python3 corpus/instruments/r46-counters-selftest-c1.py
Traceback (most recent call last):
  File ".../corpus/instruments/r46-counters-selftest-c1.py", line 675, in <module>
    sys.exit(main(sys.argv[1:]))
  File ".../corpus/instruments/r46-counters-selftest-c1.py", line 589, in main
    shutil.copytree(pure, base, symlinks=True)
  File "/usr/lib/python3.14/shutil.py", line 652, in copytree
    with os.scandir(src) as itr:
FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r46/L1/pure'
EXIT=1
```

C2:

```
$ TMPDIR=$S python3 corpus/instruments/r46-counters-selftest-c2.py
Traceback (most recent call last):
  File ".../corpus/instruments/r46-counters-selftest-c2.py", line 619, in <module>
    sys.exit(main())
  File ".../corpus/instruments/r46-counters-selftest-c2.py", line 308, in main
    sources_txt = open(os.path.join(a.pure, SOURCES), encoding="utf-8").read()
FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kasegi-r46/L1/pure/corpus/SOURCES.md'
EXIT=1
```

**Control (do-nothing discrimination).** The instrument itself is fine; only the default is
wrong. With an explicit `--pure` pointing at the live export, the same committed bytes run green:

```
$ python3 corpus/instruments/r46-counters-selftest-c1.py --pure $S/pure --work $S/w1 --jobs 8 | tail -1
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
EXIT=0
```

(`$S/pure` is a copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure2`, made with `cp -a`; the
L1 export itself was never edited.) The same holds for C2: a copy of the committed C2 selftest
whose `PURE` constant alone was repointed to `pure2` runs the null control and the controls
correctly (`null-pure-base-unmodified fixed=1/7 failing=['G1','G2','G3','G4','G5','G6']`,
`ctl-complete-tree fixed=7/7 failing=[]`).

**Comparison against the already-landed sibling instrument (round 45).** The r45 selftest has
the *same* class of hardcoded default but handles it as a clean, non-crashing error:

```
$ python3 corpus/instruments/r45-counters-selftest-c1.py
r45-counters-selftest-c1: /fast/scratch/hyaku/kasegi-r45/L1/pure is not a directory
EXIT=2
```
(`corpus/instruments/r45-counters-selftest-c1.py:785-787` — `if not os.path.isdir(d): print(...); return 2`.)
The r46 pair lacks that guard, so the same condition becomes a traceback.

**Exact one-line fix, per file.** One line each; the change is at the `argparse` call site so the
dead constant can no longer be reached as a default, and the tool then fails with argparse's own
usage error instead of a traceback:

`corpus/instruments/r46-counters-selftest-c1.py:568`
```diff
-    ap.add_argument("--pure", default=PURE)
+    ap.add_argument("--pure", required=True)
```

`corpus/instruments/r46-counters-selftest-c2.py:275`
```diff
-    ap.add_argument("--pure", default=PURE)
+    ap.add_argument("--pure", required=True)
```

**This fix makes the code match the contract the corpus already publishes.** The registry rows
for both selftests (`SKILL.md:1164-1165`, mirrored in `corpus/instruments/README.md:1001-1002`)
already document `--pure DIR` as a *required* argument — note the brackets: the optional flags are
`[--counter FILE]`, `[--work DIR]`, `[--do-nothing-control]`, while `--pure DIR` is not bracketed:

```
SKILL.md:1164 | r46-counters-selftest-c1.py | ... | run `corpus/instruments/r46-counters-selftest-c1.py` with --lane DIR --pure DIR [--counter FILE] [--work DIR]; ...
SKILL.md:1165 | r46-counters-selftest-c2.py | ... | run `corpus/instruments/r46-counters-selftest-c2.py` with --lane DIR --pure DIR [--counter FILE] [--do-nothing-control]; ...
```

The published contract says `--pure` is required; the implementation gave it a default pointing at
a path that does not exist. `required=True` is therefore a conformance fix, not a contract
change — no documented invocation changes behaviour, and every invocation the round itself uses
already passes `--pure` explicitly (`r46-mutbat.py:102-105` forwards it to both selftests; the
claim's `plain` lines and `.ufo/waves/round-46/attempt2/controls/final-measure.sh` both pass
`--pure "$PURE"`).

Verified on scratch copies of the two committed files (the committed files were not edited):

```
$ python3 $S/patched/r46-counters-selftest-c1.py
usage: r46-counters-selftest-c1.py [-h] [--lane LANE] --pure PURE
                                   [--counter COUNTER] [--work WORK]
                                   [--jobs JOBS] [--keep]
r46-counters-selftest-c1.py: error: the following arguments are required: --pure
EXIT=2
$ python3 $S/patched/r46-counters-selftest-c2.py
usage: r46-counters-selftest-c2.py [-h] [--lane LANE] --pure PURE
                                   [--counter COUNTER] [--do-nothing-control]
                                   [--keep] [-v]
r46-counters-selftest-c2.py: error: the following arguments are required: --pure
EXIT=2
```

Note for the L1: the counters `r46-c1-gate.py` / `r46-c2-gate.py` and the frozen claims are
READ-ONLY for every seat, and the two selftests are the round's C1 work surface (the claim's
`after` text says the selftests "keep `failures=0` baselines at the final revision with their
new dedicated cases"), so this is a proposed one-line amendment to land at L1 integration as a
logged erratum, not a seat edit.

**The alternative one-line fix, also verified green end-to-end.** If the L1 prefers to keep a
default, repointing line 47 in each file to the live export is the other one-line form:

```diff
-PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
+PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure2"
```

I ran a scratch copy of the committed C1 selftest with **only** that one line changed, with no
`--pure` argument at all, and it produced the full green baseline:

```
$ python3 $S/patched2_r46-counters-selftest-c1.py --work $S/w-patched2 --jobs 8 | tail -3
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
EXIT=0
```

I recommend `required=True` anyway: it satisfies the published registry contract ("--pure DIR"
unbracketed), it removes the committed instrument's dependence on an L1 scratch export
outright, and it cannot go stale again the next time the export is renamed or removed. The
`pure2` repoint does restore the *current* run, but it re-arms the same defect class the next
time `pure2` is rotated out — which is exactly what happened to `pure`.

**Impact on the C1 claim.** The claim's counter command always passes `--pure` explicitly
(`counter_cmd`: `python3 {tool}/corpus/instruments/r46-mutbat.py --root {tree} --pure {pure}
--work {work} --counter both --jobs 8`), and `r46-mutbat.py:100-104` forwards `--pure` to both
selftests, so the battery itself is not blocked. The defect bites the *bare* invocation, which
is what the freeze replay, `SKILL.md:1164-1165` / `corpus/instruments/README.md:1001-1002`
("run ... with --lane DIR --pure DIR") and any reviewer re-running the selftest standalone will
hit. It is the same routed defect class the round-45 lesson already recorded — `corpus/lessons/
round-45.md:17`, M45-7 `reference-drift`: "case 2 depended on a scratch path
(`/fast/scratch/hyaku/kasegi-r45/L1/pure`) ... registry cells claimed 'fixtures under --work or
TMPDIR'". The r46 pair repeats it.

---

## F2 (MEDIUM) — `r46-counters-selftest-c2.py` has no `--work` flag and ignores `TMPDIR`: it writes into a hardcoded, shared, stale-seat scratch directory

**Attacked:** where the C2 selftest puts its own scratch, and whether a caller can redirect it.

**Evidence.** The C2 selftest's entire option set has no `--work`:

```
$ grep -n 'add_argument' corpus/instruments/r46-counters-selftest-c2.py
274:    ap.add_argument("--lane", default=LANE)
275:    ap.add_argument("--pure", default=PURE)
276:    ap.add_argument("--counter", default=None)
277:    ap.add_argument("--do-nothing-control", action="store_true")
278:    ap.add_argument("--keep", action="store_true")
279:    ap.add_argument("-v", action="store_true")
```

and its scratch root is hardcoded to a *wave-2 attempt-1* seat name, with `TMPDIR` never
consulted for the selftest's own directory (`corpus/instruments/r46-counters-selftest-c2.py:282`):

```python
    seat_dir = os.path.join(os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku", "kasegi-r46", "R46W2ExecSelftestC2")
    os.makedirs(seat_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2st-", dir=seat_dir)
```

Proof that `TMPDIR` is ignored: with `TMPDIR` pointed at this seat's scratch, the run still
created its directories under the hardcoded path, and nothing appeared under the `TMPDIR`:

```
$ ls -d $S/c2st-*
ls: cannot access '/fast/scratch/hyaku/kasegi-r46/R46bSentScratch/c2st-*': No such file or directory
$ ls -d /fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/c2st-*
/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/c2st-gg4c9oho
/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/c2st-t6ko4bxc
/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/c2st-wh8z3e3c
```

Orphan `c2st-*` directories accumulate in that shared directory. The directory name belongs to
the *attempt-1 wave-2* seat, so this round's C2 runs collide with the previous attempt's
directory and with any concurrently running attempt-2 seat. The selftest's own cleanup only
fires on a normal exit; a killed or timed-out run leaves the directory behind.

**The directory is shared and actively written by other seats while this audit ran.** Later in
the same session the listing showed four orphans, two of them *new* while other seats' C2
selftests were running, and a `ps` sweep found 24 concurrent `r46-counters-selftest-c2.py`
processes, none of them pointed at a private scratch root:

```
$ ls -la --time-style=+%H:%M:%S /fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/
drwxr-xr-x  6 vgpnk vgpnk   90 18:47:40 .
drwxr-xr-x 33 vgpnk vgpnk 4096 18:50:52 ..
drwx------  5 vgpnk vgpnk   68 18:38:04 c2st-gg4c9oho
drwx------  5 vgpnk vgpnk   45 18:51:57 c2st-gh27holv
drwx------  5 vgpnk vgpnk   45 18:51:54 c2st-t6ko4bxc
drwx------  5 vgpnk vgpnk   45 18:36:40 c2st-wh8z3e3c

$ ps -eo pid,etimes,args | grep 'r46-counters-selftest-c2.py' | grep -v grep | wc -l
24
$ ps -eo pid,etimes,args | grep 'r46-counters-selftest-c2.py' | grep -v grep | head -2
 165992   1026 python3 drv.py --selftest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure --work /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work --jobs 7 --out /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/receipts/c2-mutant-table-committed.txt
 801624    719 /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2b/pure --counter /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2b/work/mut-lo2tjdkj/corpus/instruments/r46-c2-gate.py
```

Note the second line: a seat passes `--pure` and `--counter` but there is **no** `--work` flag
for it to pass — the scratch root of every one of those 24 processes is the same hardcoded
directory. I left that directory untouched on exit: it is shared with live concurrent runs, and
deleting inside it could destroy another seat's in-flight scratch (the very hazard this finding
is about).

**Contrast — the C1 selftest gets this right** (`corpus/instruments/r46-counters-selftest-c1.py:575`):

```python
    base_dir = a.work or os.environ.get("TMPDIR") or os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kasegi-r46", "R46W2ExecSelftestC1")
```
`--work` first, then `TMPDIR`, and the fallback name is the seat's own.

**Smallest remediation.** Give the C2 selftest the same `--work`/`TMPDIR` resolution the C1
selftest has, i.e. replace line 282 with the C1 line-575 expression (adding a `--work` argument
and preferring it), so a caller can redirect the scratch and the stale attempt-1 seat name
disappears. The C2 selftest's *children* are already contained (`base_env` sets `TMPDIR` to the
selftest's own `work/tmp`, line 294); only the selftest's own scratch root escapes.

**Why this reaches the C1 claim's own battery.** `r46-mutbat.py` forwards `--work` to the C1
selftest but **not** to the C2 selftest, because the C2 selftest has no such flag
(`corpus/instruments/r46-mutbat.py:102-105`):

```python
    if which == "c1":
        cmd += ["--pure", pure, "--work", work, "--jobs", str(jobs)]
    else:
        cmd += ["--pure", pure]
```

So every C2 mutant the battery grades writes its scratch into the shared, hardcoded
`/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/` directory — outside the battery's own
`--work`, outside the caller's `TMPDIR`, and in a directory named after a seat that belongs to
attempt-1 wave 2. The battery's `--work` promise ("mutant copies and selftest scratch live
here", `corpus/instruments/r46-mutbat.py:31`) is therefore not kept for the C2 half. Note that
the C2 half does not actually pass `--work` to the selftest today, so the C2 selftest's own
scratch is *never* under the battery's `--work` — the defect is not conditional on the flag
being added, it is unconditional.

Two concurrent battery runs (e.g. the base and tip replays in
`.ufo/waves/round-46/attempt2/controls/final-measure.sh`, which run the battery twice) and any
other seat running the C2 selftest at the same time all share that one directory. The C2
selftest's own cleanup removes only its own `c2st-*` subtree
(`shutil.rmtree(work, ignore_errors=True)` then `os.rmdir(seat_dir)` in the `finally` block,
`corpus/instruments/r46-counters-selftest-c2.py:605-610`), so a killed run leaves orphans — the
three `c2st-*` directories observed above are exactly that.

---

## F3 (LOW) — `corpus/instruments/r46-c1-gate.py:232` runs `bash -n -c <line>` with **no timeout**

**Attacked:** the one committed round-46 subprocess call without a `timeout=` argument.

**Evidence.** An AST sweep over every `r46*` Python file in `corpus/instruments/` and in the
round-46 draft trees, printing every `subprocess.run/Popen/call/check_output` that has no
`timeout=` keyword, reports exactly one call in a committed round-46 instrument:

```
NO-TIMEOUT corpus/instruments/r46-c1-gate.py:232 subprocess.run timeout=False
```

The line is (`corpus/instruments/r46-c1-gate.py:232`):

```python
        if subprocess.run(["bash", "-n", "-c", line], capture_output=True).returncode != 0:
```

`line` is a `recheck:` line read out of the **tree being graded**: `classify()` walks
`os.path.join(root, "corpus/knowledge")` (`:218`), reads each `*.md` (`:224`), and takes
`line = recheck_line(text)` (`:229`) — so the string handed to `bash` is tree-supplied. Every
other `subprocess.run` in that same file carries a timeout (`:243` `timeout=180`, `:271`
`timeout=120`, `:307` `timeout=120`, `:335` `timeout=120`); only the syntax-check call has none.

**Severity, stated honestly: LOW, because I could not demonstrate an actual hang.** `bash -n`
parses without executing, and I confirmed it does not execute — a tree-supplied
`echo PWNED > canary.txt` line left no canary:

```
$ bash -n -c 'echo PWNED > /fast/scratch/hyaku/kasegi-r46/R46bSentScratch/canary.txt'
bash -n exit=0
$ ls /fast/scratch/hyaku/kasegi-r46/R46bSentScratch/canary.txt
ls: cannot access '/fast/scratch/hyaku/kasegi-r46/R46bSentScratch/canary.txt': No such file or directory
```

Nor did the parser prove slow at realistic scale (each measured with a 30–60 s bound):

```
-- 20000 nested parens (40 KB):     real 0m0.004s   exit=2  (syntax error, fast)
-- 50000 nested parens (100 KB):     real 0m0.008s   exit=2
-- 100000 nested double quotes:      real 0m0.008s   exit=0
-- 20000 nested $( (40 KB):          real 0m0.108s   exit=139 (bash SEGV, not a hang)
-- 2 MB single token:                real 0m0.042s   exit=126 (argv too long)
-- 4 MB single line:                 real 0m0.089s   exit=126
```

So the defect is a **defence-in-depth / consistency gap** (the only unbounded child in the
file, fed by tree-supplied text), not a demonstrated denial-of-service. The remaining unbounded
risk is a `bash` that never returns on some input I did not find; the timeout is what bounds
that risk class rather than my having found the instance.

**Smallest remediation.** Add a timeout to that one call, e.g.
`subprocess.run(["bash", "-n", "-c", line], capture_output=True, timeout=30)`.

**Same class, one more committed round-46 instrument (not in the AST sweep because it is a shell
script).** `corpus/instruments/r46-plain-measure.sh:25` runs the tree-supplied recheck line
through `bash -n -c "$cmd"` with no bound, while the *next* line that actually executes it does
carry one:

```
corpus/instruments/r46-plain-measure.sh:25:  bash -n -c "$cmd" >/dev/null 2>&1 || continue
corpus/instruments/r46-plain-measure.sh:26:  ( cd "$T" && timeout 120 bash -c "$cmd" >/dev/null 2>&1 </dev/null )
```

`cmd` comes from the tree's `corpus/knowledge/*.md` `recheck:` lines (`:23-25`). The
smallest remediation is the same: bound the parse, e.g.
`timeout 30 bash -n -c "$cmd" >/dev/null 2>&1 || continue`.

**L1 coordination note — the battery is coupled to this exact line.** The frozen battery's
`M20-syntax-ignored` mutant matches the counter's line-232 text byte-for-byte
(`corpus/instruments/r46-mutbat.py:64-65`):

```python
    ("M20-syntax-ignored",   "if subprocess.run([\"bash\", \"-n\", \"-c\", line], capture_output=True).returncode != 0:",
                              "if False:"),
```

and `apply_mutant` asserts the substring occurs **exactly once**, else it aborts with
`"mutant=%s old-substring occurs %d times (expected 1) — battery vs counter drift"`
(`corpus/instruments/r46-mutbat.py:116`). I simulated the erratum on a scratch copy of the
counter and re-checked the table:

```
$ python3 - <<'EOF'   # load r46-mutbat.py, count M20's old-substring in the amended counter
MUTBAT DRIFT: M20-syntax-ignored old-substring occurs 0 times (expected 1)
EOF
```

So any L1 erratum that adds `timeout=30` to `r46-c1-gate.py:232` **must** land together with a
matching update of the battery's `M20` old-substring, or `r46-mutbat.py` aborts before grading
and the C1 after-value cannot be produced. The counter and the battery are READ-ONLY for seats,
so this is an L1 integration pairing, not a seat edit.

---

## F4 (LOW) — Attempt-2 reviewer drafts: hardcoded scratch path, no `timeout=` on subprocess calls, and no exit cleanup

**Attacked:** the attempt-2 draft scripts in `.ufo/waves/round-46/attempt2/wave1/`.

**Evidence.** The AST sweep over the attempt-2 draft trees reports:

```
NO-TIMEOUT ./R46bRevF29H1.draft/attack-h1.py:27 subprocess.run
NO-TIMEOUT ./R46bRevF29H1.draft/attack-h1.py:31 subprocess.run
HARDPATH ./R46bRevF29H1.draft/attack-h1.py:12: SCRATCH = "/fast/scratch/hyaku/kasegi-r46/R46bRevF29H1"
HARDPATH ./R46bRevF29H2H3.draft/build-defects.py:5: S = "/fast/scratch/hyaku/kasegi-r46/R46bRevF29H2H3"
```

`attack-h1.py:27` and `:31` are `subprocess.run([sys.executable, FIXTURE, ...], check=True)` and
`subprocess.run([sys.executable, GATE, "--root", d], capture_output=True, text=True)` — neither
carries `timeout=`, and neither script removes its scratch on exit
(`grep -n 'atexit\|trap\|rmtree(SCRATCH\|finally'` prints nothing for `attack-h1.py`; likewise
`build-defects.py`). Both hardcode the scratch root rather than deriving it from `HYAKU_SCRATCH`.

Note these two are *reviewer* drafts (not builder seats) and their residue was not present when I
looked (`ls -d /fast/scratch/hyaku/kasegi-r46/R46bRevF29H1` → `No such file or directory`; same
for `R46bRevF29H2H3`), so this is a robustness finding, not a claim-blocking one. The owning
seats may re-run these drafts, in which case the missing cleanup will leave residue.

**Smallest remediation.** Derive the scratch root from `HYAKU_SCRATCH` with a `mktemp -d`-style
unique directory, add `timeout=` to the two `subprocess.run` calls, and remove the scratch tree
on exit (`atexit`/`finally`).

---

## Clean results (checked, no finding)

These were attacked and came back clean; the evidence is recorded so the checks are not
silently skipped.

**`mkdtemp` without `dir=` — none.** Every `tempfile.mkdtemp` / `mkstemp` /
`NamedTemporaryFile` / `TemporaryDirectory` call in the round's `r46*` files passes `dir=`:

```
.ufo/waves/round-46/wave1/R46ExecLandingA.draft/r46-landing-gate.py:297 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave1/R46ExecLandingA.draft/r46-landing-gate.py:227 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave1/R46ExecLandingB.draft/r46-landing-gate.py:333 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave1/R46ExecLandingB.draft/r46-landing-gate.py:562 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave1/R46ExecSelftestC1.draft/r46-counters-selftest-c1.py:413 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave1/R46ExecSelftestC2.draft/r46-counters-selftest-c2.py:278 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave2/R46W2ExecSelftestC1.draft/r46-counters-selftest-c1.py:577 tempfile.mkdtemp dir=True
.ufo/waves/round-46/wave2/R46W2ExecSelftestC2.draft/r46-counters-selftest-c2.py:288 tempfile.mkdtemp dir=True
corpus/instruments/r46-c1-gate.py:304 tempfile.mkdtemp dir=True
corpus/instruments/r46-c1-gate.py:319 tempfile.mkdtemp dir=True
corpus/instruments/r46-counters-selftest-c1.py:577 tempfile.mkdtemp dir=True
corpus/instruments/r46-counters-selftest-c2.py:284 tempfile.mkdtemp dir=True
corpus/instruments/r46-landing-gate.py:334 tempfile.mkdtemp dir=True
corpus/instruments/r46-landing-gate.py:563 tempfile.mkdtemp dir=True
corpus/instruments/r46-mutbat.py:160 tempfile.mkdtemp dir=True
```
The battery's mutant copies are made with `dir=a.work`
(`corpus/instruments/r46-mutbat.py:160`), and each mutant directory is removed in a `finally`
(`:164-165`).

**Hardcoded `/tmp` in the committed round-46 instruments — none.**
`grep -n '/tmp' corpus/instruments/r46-*.py corpus/instruments/r46-*.sh` prints nothing.

**Hardcoded `/fast` in the committed round-46 instruments — two occurrences, both the F1 dead
default and one C1 fixture string.**
```
corpus/instruments/r46-counters-selftest-c1.py:47:PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
corpus/instruments/r46-counters-selftest-c1.py:230:    set_recheck(t, CP, "recheck: cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && python3 %s --entry corpus/knowledge/%s" % (GATE, CP))
corpus/instruments/r46-counters-selftest-c1.py:471:    ("L3-cd-target-not-the-lane", m_cd_bogus, {"L3"}, "mut", "contract recheck `cd /fast/scratch/hyaku/kasegi-r46/no-such-dir && python3 ...--entry ...`"),
corpus/instruments/r46-counters-selftest-c2.py:47:PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
corpus/instruments/r46-counters-selftest-c2.py:282:    seat_dir = os.path.join(os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku", "kasegi-r46", "R46W2ExecSelftestC2")
```
Lines 230 and 471 are *fixture text* (a deliberately non-existent `cd` target used as a mutant
input for the L3 limb) and are not scratch paths the tool writes to — no finding. Line 47 (both
files) and line 282 are the F1/F2 findings.

**The committed `r46-f29-gate.py` writes nothing into the tree it grades and nothing into the
fleet root.** It declares `--work` (`:349`) but never uses it and never creates scratch. Ran
against a scratch tree and diffed the fleet-root listing before/after:

```
$ python3 corpus/instruments/r46-f29-gate.py --root $S/pure
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
$ diff fleet_before.txt fleet_after.txt && echo "NO CHANGE in fleet root listing"
NO CHANGE in fleet root listing
$ find $S/pure -newermt '-2 minutes'
(empty = no writes into --root)
```
Its two subprocess calls (`source-recheck.py` at `:266`, the census at `:337`) both carry
`timeout=120`.

**The census helper it shells out to does not write outside `--out`.**
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:44` initialises `OUT=""` and `:699`
does `[ -n "$OUT" ] && : > "$OUT"` — with no `--out` passed (the f29 gate passes only
`validate --file ...`), the census writes stdout only.

**`r46-mutbat.py` subprocess calls carry a timeout** (`:106`, `timeout=1800`).

**`r46-landing-gate.py`'s subprocess calls** — of its seven `subprocess.run` calls, two carry
a timeout (`:79` `timeout=60`, `:118` `timeout=60`); the five without one (`:294`, `:301`,
`:311`, `:373`, `:596`) are `git` calls against **fixture** repos that the gate itself creates
under its own scratch (`:334`, `:563`, both `mkdtemp(dir=work)`), plus the self-invocation at
`:596`, and `:294` is the `rev-parse --show-toplevel` that asserts the fixture's toplevel
before use. The gate is not on the C1/C2 counter path and is not the round's claim surface;
recorded as INFO, not a finding.

---

## Limitations

- **F3's remediation is not demonstrated as landed.** I proved the *coupling* (an amended
  `r46-c1-gate.py:232` breaks the battery's `M20` mutant) on a scratch copy; I did not and may
  not amend the committed counter or the frozen battery. The end-to-end claim re-run
  (`mutbat ... uncaught=0`) after any such erratum is the L1's to perform.
- **F1's `required=True` fix was exercised on scratch copies of the two committed selftests**
  (bare invocation → argparse usage error, exit 2). Both fix forms were then run to completion:
  the `PURE`-repoint copy of the committed C1 selftest, with **no** `--pure` argument, printed
  `selftest cases=76 failures=0` / `EXIT=0`; and the `required=True` copy of the committed C1
  selftest, invoked **with** `--pure`, printed the same `selftest cases=76 failures=0` /
  `EXIT=0`. The patched C2 file was run to completion against the live export and behaved
  correctly (null control 1/7, controls 7/7). The committed files themselves were not edited.
- **F2's remediation was not applied.** It is a design change to a committed selftest, and the
  committed selftests are the round's C1 work surface (L1 integrates; seats draft). The
  evidence is a directory listing, not an interception of syscalls; the conclusion rests on the
  source line (`:282`) plus the observed absence of `c2st-*` under `TMPDIR` and their presence
  under the hardcoded path.
- **Scope.** I audited the round-46 instruments (`corpus/instruments/r46-*`), the round-46 draft
  trees (`wave1`, `wave2`), and the attempt-2 wave-1 drafts. I did not audit the pre-existing
  corpus instruments (`density.py`, `resolve.py`, `capture-binding-check.py`,
  `kill-rule-check.py`, `frontier-recheck-count.py`, `r36`-`r41-closure.sh`) that also mention
  `/tmp` or `/fast` — those are outside this round's surface, and the `wave2` sentinel item
  `SentFinal` scopes the `/fast` + `/tmp` grep to the landed tree.
- **No live-target testing.** Everything above is local-file evidence only; the corpus is
  documentation.
- **No commits, pushes, or mutating git/jj calls.** Only `git log`/`status`/`ls-files`-class
  reads were used, on the lane repo. The committed counters and the frozen claims file were
  read, never written.
- **No credentials, session URLs, or operator-session references** appear in this report.
- **Tooling.** No tool was installed or upgraded for this seat; no pacman transaction was
  attempted. Only Python 3.14 (`/usr/lib/python3.14`) stdlib was used — `ast`, `shutil`,
  `subprocess`, `hashlib` — plus coreutils (`ls`, `grep`, `diff`, `cp`).

## Scratch hygiene

This seat's scratch was `/fast/scratch/hyaku/kasegi-r46/R46bSentScratch/` (the `pure` copy,
the two patched selftest copies, the `drift/` counter copy, the run logs). It is removed on exit.
The L1 export `/fast/scratch/hyaku/kasegi-r46/L1/pure2` was copied, never edited.

The two full-baseline run logs quoted in F1 are copied into this seat's draft directory before
the scratch was removed (a `/tmp` or scratch path is never citable evidence):

- `.ufo/waves/round-46/attempt2/wave1/R46bSentScratch.draft/patched-required-c1-with-pure.txt`
  — the `required=True` copy of the committed C1 selftest, run **with** `--pure`:
  `selftest cases=76 failures=0` / `EXIT=0`.
- `.ufo/waves/round-46/attempt2/wave1/R46bSentScratch.draft/patched-pure2-c1-bare.txt`
  — the `PURE`-repoint copy of the committed C1 selftest, run with **no** `--pure`:
  `selftest cases=76 failures=0` / `EXIT=0`.

The shared directory `/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2/` (the hardcoded C2
selftest scratch root, F2) was **not** cleaned by this seat: it is shared with live concurrent
runs from other seats, and deleting inside it could destroy another seat's in-flight scratch.
