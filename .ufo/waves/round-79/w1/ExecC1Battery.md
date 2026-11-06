# ExecC1Battery — round-79 attempt 1, C1 frozen-candidate scoring

Seat: ExecC1Battery (leaf). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Freeze commit: 9d0b1eb0709e47c3c6decc09138b5012a8968924 (base d16d2124fd5262f5a8088aa598f1e628f897d3ab)
Scratch: /fast/scratch/hyaku/kasegi-r79/ExecC1Battery (TMPDIR passed explicitly; removed at end)
Frozen bytes edited: **none**. Candidate, counter and table were opened read-only.

## 0. Byte freeze check (item 1)

Command:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum .ufo/waves/round-79/c1/recheck-cwd-census.py .ufo/waves/round-79/c1/mutbat.py .ufo/waves/round-79/c1/mutant-table.json
for f in <each>; do printf '%s  ' "$f"; git show 9d0b1eb0709e47c3c6decc09138b5012a8968924:"$f" | sha256sum; done
```

Working-tree hashes:

```
eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f  .ufo/waves/round-79/c1/recheck-cwd-census.py
735d2336550850a0c72c6049e5d7ee1f92dd345332b624578a8b627bcfba3ea9  .ufo/waves/round-79/c1/mutbat.py
0cb50dc858d0fc5548bc6c22a49171be3326298763c64d5344afe83de2d731e2  .ufo/waves/round-79/c1/mutant-table.json
```

Freeze-commit blobs (`git show 9d0b1eb:<path> | sha256sum`):

```
.ufo/waves/round-79/c1/recheck-cwd-census.py  eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f  -
.ufo/waves/round-79/c1/mutbat.py  735d2336550850a0c72c6049e5d7ee1f92dd345332b624578a8b627bcfba3ea9  -
.ufo/waves/round-79/c1/mutant-table.json  0cb50dc858d0fc5548bc6c22a49171be3326298763c64d5344afe83de2d731e2  -
```

All three match. Candidate sha equals the frozen P2 value `eda49d32…091f2f`. Table has 19 rows (`len(json.load(...)) == 19`).

## 1. P1 — selftest

Command:

```
TMPDIR=$S python3 -B .ufo/waves/round-79/c1/recheck-cwd-census.py --selftest
```

Full stdout (15 case lines + summary), rc=0:

```
selftest case=prefix-census ok got=entries=3,exit0_foreign=2,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=2,norecheck=0 want=entries=3,exit0_foreign=2,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=2,norecheck=0
selftest case=result-main ok nonconformant ret=1 conformant ret=0
selftest case=tmpdir-parent ok calls=3 dirs='/fast/scratch/hyaku/kasegi-r79/ExecC1Battery','/fast/scratch/hyaku/kasegi-r79/ExecC1Battery','/fast/scratch/hyaku/kasegi-r79/ExecC1Battery'
selftest case=scratch-cleanup ok calls=3 leftover=0
selftest case=first-line ok got=entries=1,exit0_foreign=0,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=1,norecheck=0 want=entries=1,exit0_foreign=0,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=1,norecheck=0
selftest case=restoration-only ok got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 marker_present=False
selftest case=both-headers ok got=entries=2,exit0_foreign=2,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=0 want=entries=2,exit0_foreign=2,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=0 first_ran=True restoration_ran=False
selftest case=relabel-detection ok unpatched got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=1,restoration_only=0 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=1,restoration_only=0; patched got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1
selftest case=tmpdir-refusal ok ret=2 stdout='' stderr='recheck-cwd: TMPDIR /fast/scratch/hyaku/kasegi-r79/ExecC1Battery/recheck-cwd-selftest-xlvyzn6i/no-such-tmpdir is not a directory\n'
selftest case=gate-predicates ok rows=17 bad=[]
selftest case=gate-wiring ok findings=[]
selftest case=gate-regs ok registered=['restoration-only-result']
selftest case=gate-consume ok clean_ok=True limb_log=[True]
selftest case=gate-negpolarity ok neg_ok=False
selftest case=gate-checkids ok missing=[] extra=[] side_logs=[[True], [True], [True]]
selftest cases=15 failures=0
```

rc=0. **P1 = met.**

## 2. P3 — frozen mutant battery (19 rows)

Run 1 (with `--keep` into the wave dir), rc=1:

```
TMPDIR=$S python3 -B .ufo/waves/round-79/c1/mutbat.py \
  --target .ufo/waves/round-79/c1/recheck-cwd-census.py \
  --table .ufo/waves/round-79/c1/mutant-table.json \
  --expect-cases 15 --work $S \
  --keep /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ExecC1Battery-mutants
```

Verbatim output:

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-X1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-X2a verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-X2b verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-M8 verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-W1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-W2 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-N1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-P1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-P2 verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-G1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-C1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-NP verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-CL verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-T1 verdict=EXCEPTION-KILL rc=1 fails=1 counted=no
MUTBAT target_sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0
```

rc=1.

Run 2 (stability, no `--keep`), rc=1 — identical MUTBAT line:

```
MUTBAT target_sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0
```

All 19 `MUTANT` lines identical between runs (same verdicts, same fails, same counted). Stable, and stably short of the predicate.

P3 requires `killed=19 survived=0 dirty=0 notderived=0` and rc=0. Measured `killed=18 survived=0 dirty=1 notderived=0`, rc=1. **P3 = unmet.**

Retained evidence: `.ufo/waves/round-79/w1/ExecC1Battery-mutants/` — 19 files `K-*.out`, each `rc=<n>` plus the mutant's full selftest output.

## 3. P3 root cause — K-T1 is EXCEPTION-KILL on an assertion-class row

`ExecC1Battery-mutants/K-T1.out` (verbatim tail):

```
selftest case=tmpdir-refusal FAIL ret=-99 stdout="exception=FileNotFoundError(2, 'No such file or directory')" stderr=''
...
selftest cases=15 failures=1
```

Table row K-T1 (`class: "assertion"`):

- anchor: the whole `def tmpdir_refused():` body (the TMPDIR refusal)
- replacement: `def tmpdir_refused():\n    return False`
- expect: `TMPDIR refusal removed -> tmpdir-refusal FAIL (exception caught as ret=-99)`

Defect chain, each step measured:

1. The mutant removes the refusal, so the selftest's `tmpdir-refusal` case runs `main()` with a nonexistent TMPDIR and `tempfile.mkdtemp` raises `FileNotFoundError`.
2. The candidate's own harness catches it at `recheck-cwd-census.py:428` — `out13, ret13 = "exception=%r" % (exc13,), -99` — and renders the FAIL detail containing the literal token `exception=`.
3. The counter's classifier `EXC_RE = re.compile(r"^selftest case=\S+ FAIL .*exception", re.M)` (`mutbat.py:41`) matches that caught-exception detail, so `verdict()` returns `EXCEPTION-KILL` (`mutbat.py:57-63`).
4. K-T1's class is `"assertion"`, so `counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row.get("class") == "exception")` is False → `dirty += 1`, `killed` stays 18.
5. rc=1, and the frozen kill rule names this exact case: *"Any of the nineteen rows not counted killed by the frozen counter (SURVIVED, DIRTY, NOT-DERIVED, or **EXCEPTION-KILL on an assertion-class row**) = NOT VERIFIED."*

So C1 is **NOT VERIFIED** under its own frozen kill rule, on one row.

Note the internal inconsistency: the row's own `expect` text already predicts the caught-exception mode (`exception caught as ret=-99`), yet the row is classed `assertion`, which the counter refuses to count in that mode. The table and the counter disagree about what K-T1's kill looks like.

Minimal repair, measured in scratch on a **copy** of the table (frozen bytes untouched, no row added/removed, one field changed):

```
python3 -c "... K-T1['class']='exception' ... " > $S/table-k-t1-as-exception.json
TMPDIR=$S python3 -B .ufo/waves/round-79/c1/mutbat.py --target .ufo/waves/round-79/c1/recheck-cwd-census.py \
  --table $S/table-k-t1-as-exception.json --expect-cases 15 --work $S
```

```
MUTANT K-T1 verdict=EXCEPTION-KILL rc=1 fails=1 counted=yes
MUTBAT target_sha256=eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f baseline=ok rows=19 killed=19 survived=0 dirty=0 notderived=0
```

rc=0. One field (`K-T1.class: "assertion" → "exception"`) is the whole gap between killed=18 dirty=1 and killed=19 dirty=0.

**Routed defect (for the L1, not applied by this seat):** the frozen table row K-T1 is classed `assertion` while its only failure mode is a caught exception, so the frozen counter scores it `EXCEPTION-KILL counted=no` and P3 cannot reach `killed=19 dirty=0`. Two candidate repairs, both outside this seat's authority because the table, counter and candidate bytes are frozen and "no row is added, removed or edited after any seat has scored":

- (a) table: `K-T1.class` → `"exception"` (measured above: killed=19 dirty=0 rc=0);
- (b) counter: `EXC_RE` must not match the candidate's own caught-exception detail (`exception=` rendered at `recheck-cwd-census.py:428`), only a genuine uncaught-exception marker — otherwise every assertion-class row that the candidate's harness catches is silently uncountable.

Either way this is a routed defect, not a rule change: the frozen predicate P3 stands as written and is unmet at the frozen bytes.

## 4. P4 — nonexistent TMPDIR refusal

Command (a), rc=2:

```
TMPDIR=/nonexistent-kasegi-r79 python3 -B .ufo/waves/round-79/c1/recheck-cwd-census.py \
  --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

stdout: (empty)
stderr:

```
recheck-cwd: TMPDIR /nonexistent-kasegi-r79 is not a directory
```

rc=2. `grep -c Traceback` on both streams: `0` and `0`.

Command (b), TMPDIR set to a regular (non-directory) file created in scratch (`$S/regular-file-not-a-dir`, 0 bytes), rc=2:

```
TMPDIR=$S/regular-file-not-a-dir python3 -B .ufo/waves/round-79/c1/recheck-cwd-census.py \
  --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

stdout: (empty)
stderr:

```
recheck-cwd: TMPDIR /fast/scratch/hyaku/kasegi-r79/ExecC1Battery/regular-file-not-a-dir is not a directory
```

rc=2. `grep -c Traceback` on both streams: `0` and `0`.

Both forms exit 2, emit a stderr line beginning `recheck-cwd: TMPDIR`, and contain no `Traceback`. **P4 = met.**

## 5. P7 — exec surface unchanged

```
grep -c 'subprocess.run('  -> 1
grep -c '"bash", "-c"'     -> 1
grep -n '/tmp'             -> 25:path come from tempfile, which honors TMPDIR; no path is hard-coded under /tmp.
```

The single hit for each exec pattern is the same call, `recheck-cwd-census.py:81`:

```
proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,
```

The only `/tmp` occurrence is prose inside the module docstring (line 25, in the conformance/exit-code paragraph), asserting the opposite of a hard-coded path; it is not a string literal path. **P7 = met.**

## 6. Verdicts

```
P1 = met
P3 = unmet
P4 = met
P7 = met
```

C1 overall: **NOT VERIFIED** at freeze 9d0b1eb. P1/P4/P7 hold; P3 is short by exactly one row (K-T1), and the frozen kill rule treats that row's `EXCEPTION-KILL` on an `assertion`-class row as NOT VERIFIED.

## 7. Files written by this seat

- `.ufo/waves/round-79/w1/ExecC1Battery.md` (this report)
- `.ufo/waves/round-79/w1/ExecC1Battery-mutants/K-*.out` (19 retained mutant outputs)

No candidate, counter, table, instrument, corpus, SKILL.md, PROVINCE.md, SCORECARD.md, LOG.md or lane file was modified. `git status --porcelain .` after the runs shows changes only under `.ufo/waves/round-79/` (the pre-existing untracked dispatch/ready files and this seat's `w1/`). No git/jj write was issued. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r79/ExecC1Battery` was removed at the end.

## 8. Risks / blockers

- The counter writes only under the `--work` TMPDIR and the `--keep` dir named on the command line; no write outside TMPDIR was observed. Not a defect.
- If the L1 re-scores, the same K-T1 result is expected: both runs produced byte-identical `MUTANT`/`MUTBAT` lines.
- Repair (a) is a one-field table edit but the table is frozen post-scoring; repair (b) touches the counter's classifier. Both need an L1 decision on how a frozen-bytes defect is remediated (new freeze vs. routed finding), which is outside this seat's authority.
