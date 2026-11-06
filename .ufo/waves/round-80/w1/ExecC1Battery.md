# ExecC1Battery — scored receipt of C1 (round 80, attempt 1)

Seat: ExecC1Battery. Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch: `/fast/scratch/hyaku/kasegi-r80/ExecC1Battery` (deleted at hand-off). No tool installs.
Frozen bytes were **not** edited. All commands run from the lane root over the frozen commit bytes.

## 0. Frozen-byte identity (sha256 file vs `git show 4ab545865f747fca8456370b5927fe51236fe579:<p>`)

Command: `for p in ...; do a=$(sha256sum "$p"); b=$(git show 4ab5458...:"$p" | sha256sum); ...`

```
MATCH .ufo/waves/round-80/c1/recheck-cwd-census.py 420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698
MATCH .ufo/waves/round-80/c1/mutbat.py b47276d1f96795d8b430de0be195f26122ffa6d673fb4b25e88250d8fcb7d450
MATCH .ufo/waves/round-80/c1/mutant-table.json 08d7f3cebc5b40dfb6a03a0ba5caa1f1aa848b3bbc3d9e0b6b969497098ea418
MATCH .ufo/waves/round-80/c1/build-table.py e0a8c714c6941cb70b5b2a2436409dcbd75c3614455ff4b558593bccb9ee0ef3
```

Candidate 420151fd…5698, counter b47276d1…d450, table 08d7f3ce…e418 all match the frozen commit and the
hashes in `claims.json`. The working tree bytes the counter scored are the frozen bytes.

## 1. P1 — selftest

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r80/ExecC1Battery python3 -B .ufo/waves/round-80/c1/recheck-cwd-census.py --selftest`

```
selftest case=prefix-census ok got=entries=6,exit0_foreign=3,exit1_foreign=1,exit2_foreign=1,exit_other=1,noprefix=5,norecheck=0 want=entries=6,exit0_foreign=3,exit1_foreign=1,exit2_foreign=1,exit_other=1,noprefix=5,norecheck=0
selftest case=result-main ok nonconformant ret=1 conformant ret=0
selftest case=tmpdir-parent ok calls=6 dirs='/fast/scratch/hyaku/kasegi-r80/ExecC1Battery','/fast/scratch/hyaku/kasegi-r80/ExecC1Battery','/fast/scratch/hyaku/kasegi-r80/ExecC1Battery','/fast/scratch/hyaku/kasegi-r80/ExecC1Battery','/fast/scratch/hyaku/kasegi-r80/ExecC1Battery','/fast/scratch/hyaku/kasegi-r80/ExecC1Battery'
selftest case=scratch-cleanup ok calls=6 leftover=0
selftest case=first-line ok got=entries=1,exit0_foreign=0,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=1,norecheck=0 want=entries=1,exit0_foreign=0,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=1,norecheck=0
selftest case=restoration-only ok got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 marker_present=False
selftest case=both-headers ok got=entries=2,exit0_foreign=2,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=0 want=entries=2,exit0_foreign=2,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=0 first_ran=True restoration_ran=False
selftest case=relabel-detection ok unpatched got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=1,restoration_only=0 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=1,restoration_only=0; patched got=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1 want=entries=2,exit0_foreign=1,exit2_foreign=0,noprefix=0,norecheck=0,restoration_only=1
selftest case=tmpdir-refusal ok ret=2 stdout='' stderr='recheck-cwd: TMPDIR /fast/scratch/hyaku/kasegi-r80/ExecC1Battery/recheck-cwd-selftest-6mpi5i5b/no-such-tmpdir is not a directory\n'
selftest case=gate-predicates ok rows=28 expect=28 bad=[]
selftest case=gate-wiring ok findings=[]
selftest case=gate-regs ok registered=['restoration-only-result']
selftest case=gate-consume ok clean_ok=True limb_log=[True]
selftest case=gate-negpolarity ok neg_ok=False neg_ret_ok=False
selftest case=gate-checkids ok missing=[] extra=[] side_logs=[[True], [True], [True]]
selftest cases=15 failures=0
RC=0
```

Captured verbatim (stdout redirected to scratch; stderr empty). Two runs agree line-for-line except the random
`recheck-cwd-selftest-*` scratch suffix inside the `tmpdir-refusal` detail; all 15 case lines report `ok`, `FAIL`
count 0.

## 2. P3 — mutation battery with `--keep`

Command: `python3 -B .ufo/waves/round-80/c1/mutbat.py --target .ufo/waves/round-80/c1/recheck-cwd-census.py --table .ufo/waves/round-80/c1/mutant-table.json --expect-cases 15 --work $S --keep /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/ExecC1Battery-mutants`

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=2 counted=yes
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
MUTANT K-T1 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N10 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N11 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N21 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N25 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N26 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N27 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT N30 verdict=KILLED rc=1 fails=1 counted=yes
MUTANT T1 verdict=KILLED rc=1 fails=2 counted=yes
MUTANT T2 verdict=KILLED rc=1 fails=1 counted=yes
MUTBAT target_sha256=420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698 baseline=ok rows=28 killed=28 survived=0 dirty=0 notderived=0
RC=0
```

The nine r79 routed survivors are in the scored set and all counted killed: **N10 N11 N21 N25 N26 N27 N30 T1 T2**.

### 2a. Kept transcripts (`ExecC1Battery-mutants/`)

28 files, one per row (`K-M1.out` … `T2.out`), 112K total. Each carries `rc=1` then the mutant's real selftest
output. Spot checks, verbatim:

```
K-M3.out:
rc=1
...
selftest case=gate-consume FAIL exception=NameError("name 'out6' is not defined")
selftest case=gate-negpolarity FAIL not-evaluated-after-exception
...
selftest cases=15 failures=2

T1.out:
rc=1
...
selftest case=gate-wiring FAIL findings=['F4:gate-consume:526']
...
selftest case=gate-checkids FAIL missing=[] extra=[] side_logs=[[True], [False], [True]]
...
selftest cases=15 failures=2
```

K-M3 is the exact shape R129 exists for: an assertion FAIL whose detail begins `exception=` scores
EXCEPTION-KILL `counted=yes` (the r79 free-text classifier scored this class `counted=no`). Every kept file shows
a genuine selftest FAIL from the mutation, not an import/crash artifact.

## 3. P3 second run — stability (no `--keep`)

Command: same as §2 without `--keep`/`--keep` argument.

```
MUTBAT target_sha256=420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698 baseline=ok rows=28 killed=28 survived=0 dirty=0 notderived=0
RC=0
```

Identical summary line and rc across both runs; per-row verdict lines also identical.

## 4. P8 — counter selftest

Command: `python3 -B .ufo/waves/round-80/c1/mutbat.py --selftest --work /fast/scratch/hyaku/kasegi-r80/ExecC1Battery`

```
mutbat selftest ok got={'T-KILL': 'KILLED', 'T-SURV': 'SURVIVED', 'T-ABSENT': 'NOT-DERIVED', 'T-EXC': 'EXCEPTION-KILL', 'T-EXCA': 'EXCEPTION-KILL'} counted={'T-KILL': 'yes', 'T-SURV': 'no', 'T-EXC': 'yes', 'T-EXCA': 'no'} all_killed_exit=True
RC=0
```

The show-able-to-fail control is internal and observable: `T-KILL` (assertion FAIL whose detail contains the word
exception) → KILLED counted=yes; `T-EXCA` (a true `exception=` detail that is not an assertion) → EXCEPTION-KILL
counted=no; `T-SURV` → SURVIVED counted=no. `all_killed_exit=True`.

## 5. P4 — TMPDIR refusal

### 5a. Nonexistent TMPDIR

Command: `TMPDIR=/nonexistent-kasegi-r80 python3 -B .ufo/waves/round-80/c1/recheck-cwd-census.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`

```
rc      = 2
stdout  = (empty)
stderr  = recheck-cwd: TMPDIR /nonexistent-kasegi-r80 is not a directory
Traceback occurrences = 0 (stdout) + 0 (stderr)
```

### 5b. TMPDIR is a regular file (beyond the frozen predicate, extra probe)

Command: same with `TMPDIR=/fast/scratch/hyaku/kasegi-r80/ExecC1Battery/regular-file-not-dir` (`: > file`).

```
rc      = 2
stdout  = (empty)
stderr  = recheck-cwd: TMPDIR /fast/scratch/hyaku/kasegi-r80/ExecC1Battery/regular-file-not-dir is not a directory
Traceback occurrences = 0 (stdout) + 0 (stderr)
```

Same named-refusal class for a non-directory that exists, no uncaught OSError.

## 6. P7 — static literals in the candidate

Command: `grep -c 'subprocess.run(' …; grep -c '"bash", "-c"' …; grep -cE "[\"']/tmp" …`

```
subprocess.run(  = 1
"bash", "-c"     = 1
/tmp literals    = 0   (grep rc=1, no match)
```

One subprocess call site, one `bash -c`, no `/tmp` literal in the instrument (581 lines).

## 7. Table rebuild vs frozen table

Command: `python3 -B .ufo/waves/round-80/c1/build-table.py .ufo/waves/round-80/c1/recheck-cwd-census.py $S/table.json && cmp $S/table.json .ufo/waves/round-80/c1/mutant-table.json`

```
TABLE rows=28 not_unique=[]
BUILD_RC=0
CMP_RC=0
08d7f3cebc5b40dfb6a03a0ba5caa1f1aa848b3bbc3d9e0b6b969497098ea418  $S/table.json
08d7f3cebc5b40dfb6a03a0ba5caa1f1aa848b3bbc3d9e0b6b969497098ea418  .ufo/waves/round-80/c1/mutant-table.json
```

The builder deterministically regenerates the frozen table byte-for-byte; 28 unique rows.

## Verdicts (frozen C1 predicates, scored over the frozen bytes)

```
P1 = met    (selftest cases=15 failures=0, rc 0)
P3 = met    (MUTBAT baseline=ok rows=28 killed=28 survived=0 dirty=0 notderived=0, rc 0, twice, identical)
P4 = met    (nonexistent TMPDIR: rc 2, stderr 'recheck-cwd: TMPDIR … is not a directory', 0 Traceback; regular-file TMPDIR same)
P7 = met    (1 / 1 / 0)
P8 = met    ('mutbat selftest ok … all_killed_exit=True', rc 0)
```

C1's predicate set as scored by this seat: **all five predicates assigned to this battery are met**; the frozen
counter reports 28/28 killed with none survived/dirty/not-derived.

## Observations (advisory; not verdict changes)

- Determinism: two independent P3 runs and a byte-identical table rebuild — the kill set is a property of the
  frozen bytes, not of run order or scratch state.
- `ExecC1Battery-mutants/*.out` embed absolute scratch paths (`/fast/scratch/hyaku/kasegi-r80/ExecC1Battery/mutbat-run-*`)
  in the `tmpdir-parent`/`tmpdir-refusal` case lines. Those are transcript artifacts in the wave dir, harmless, but
  the wave-dir bytes are not reproducible verbatim across seats. The verdict-bearing `MUTBAT`/`MUTANT` lines are
  scratch-independent.
- P1 `tmpdir-parent` proves the candidate honors the caller's TMPDIR (all six calls land in `$TMPDIR`, zero
  leftovers per `scratch-cleanup`), consistent with the SCRATCH directive.
- Landing-bytes equality (read-only check): the worktree `corpus/instruments/recheck-cwd-census.py` now hashes
  `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698` — byte-identical to the frozen candidate this
  receipt scored — and `SKILL.md`/`corpus/instruments/README.md` carry the `selftest cases=15 failures=0` pin. So the
  P1/P3/P4/P7/P8 scores above transfer to the landed instrument unchanged (P2/P5/P6 belong to other seats).
- No mutation outside the frozen table was attempted; nothing here re-scores r79 or edits frozen bytes.

## Files written

- `.ufo/waves/round-80/w1/ExecC1Battery.md` (this report)
- `.ufo/waves/round-80/w1/ExecC1Battery-mutants/{K-M1..T2}.out` (28 kept mutant transcripts, from the named `--keep` run)
