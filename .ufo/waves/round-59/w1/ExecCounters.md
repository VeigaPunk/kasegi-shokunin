MISMATCH (counter-side, not claim-side) — 1/15 frozen counting commands, C1[0], fails its own `# want` when run literally: CTRL-quoted-separator exit=2 want=0 (no derived=35) and RESIDUAL-awk-write exit=2 markers=0 want exit=0 markers=1. C1[0] with an absolute instrument path (twin) and all 14 other commands match every want. Cause: `c1-probe-run.sh` takes `INSTR=$1` at line 8 and then runs the instrument from inside each probe root at line 23, so the frozen relative argument `corpus/instruments/figure-audit.py` cannot be opened.

Seat ExecCounters, kasegi round 59, wave w1. Clone at `472737847ff31d1255bf1a0745822a5e878e9622`, cwd = clone root for every command. Full stdout for all 16 records (15 frozen commands + 1 diagnostic twin) is in `W/ExecCounters.json`; this file quotes the decisive lines and every number it states.

## 1. Provenance and runner

```
$ S=/fast/scratch/hyaku/kasegi-r59/ExecCounters; mkdir -p "$S"
$ D=$(mktemp -d -p "$S") && echo "D=$D" && git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$D/clone" && git -C "$D/clone" checkout -q 472737847ff31d1255bf1a0745822a5e878e9622 && git -C "$D/clone" rev-parse --show-toplevel && git -C "$D/clone" rev-parse HEAD
D=/fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3
/fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone
472737847ff31d1255bf1a0745822a5e878e9622
$ W=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/w1
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/claims.json
becf44d1a29bba94dc8374f63787c8a2a450209506f4282cd9ca0b65614aa0d6  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/claims.json
$ cd "$S" && TMPDIR=$S/tmp python3 "$S/run.py" "$D/clone" "$S" "$W/ExecCounters.json"; echo "SCRIPT_EXIT=$?"
verdict=MISMATCH mismatches=4 records=16
  mismatch C1[0] :: CTRL-quoted-separator: exit=2 want=0
  mismatch C1[0] :: CTRL-quoted-separator: no derived=35
  mismatch C1[0] :: RESIDUAL-awk-write: exit=2 want=0
  mismatch C1[0] :: RESIDUAL-awk-write: markers=0 want=1
SCRIPT_EXIT=1
```

`run.py` reads `claims.json` from the lane (never from the clone), splits each entry at the literal `   # want:` marker, runs the head with `bash -c` and `cwd` = clone root, and records the `# want:` tail as an opaque string. The expectations it checks are hand-written literals, not a parse of that string. Every command ran with `TMPDIR=/fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp` and `LC_ALL=C` exported. For piped commands it records both the as-written shell exit code (last pipeline stage) and a diagnostic `bash -o pipefail` exit code.

Aggregates, recomputed from `W/ExecCounters.json`:

```
$ python3 - <<'PY'
import json
p="/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/w1/ExecCounters.json"
d=json.load(open(p))
recs=d["records"]; frozen=[r for r in recs if not r.get("variant")]
print("frozen_commands=%d records=%d twins=%d" % (len(frozen), len(recs), len(recs)-len(frozen)))
print("verdict=%s mismatches=%d" % (d["verdict"], len(d["mismatches"])))
print("C1_match=%d/6 C2_match=%d/9 twin_match=%s" % (
  sum(r["match"] for r in frozen if r["claim"]=="C1"),
  sum(r["match"] for r in frozen if r["claim"]=="C2"),
  all(r["match"] for r in recs if r.get("variant"))))
prim=[r for r in recs if r["claim"]=="C1" and r["index"]==0 and not r.get("variant")][0]
print("C1[0]_primary_violations=%d open_errors=%d/%d" % (
  len(prim["checks_failed"]), prim["observation"]["probes_with_python_open_error"], prim["observation"]["probes_parsed"]))
c21=[r for r in frozen if r["claim"]=="C2" and r["index"]==1][0]
print("C2[1]_Q_lines=%d all_occurrences_1=%s" % (
  sum(1 for l in c21["stdout"].splitlines() if l.startswith("S092:Q")),
  all("occurrences=1" in l for l in c21["stdout"].splitlines() if l.startswith("S092:Q"))))
c14=[r for r in frozen if r["claim"]=="C1" and r["index"]==4][0]
print("C1[4]_pipeline_exit=%d pipefail_exit=%d" % (c14["exit_code"], c14["pipefail_exit_code"]))
PY
frozen_commands=15 records=16 twins=1
verdict=MISMATCH mismatches=4
C1_match=5/6 C2_match=9/9 twin_match=True
C1[0]_primary_violations=4 open_errors=10/10
C2[1]_Q_lines=10 all_occurrences_1=True
C1[4]_pipeline_exit=0 pipefail_exit=1
```

Two recorded deviations, both forced by the seat contract and both neutral to the measured values:

1. The frozen C1[0] scratch `/fast/scratch/hyaku/kasegi-r59/l1/c1-after` was replaced with `$S/probe-after` so the probe runner's `rm -rf`/recreate touches only this seat's scratch (`run.py` "deviations" in the JSON).
2. C1[0] was run a second time as a diagnostic twin with the instrument passed absolutely (section 3).

## 2. C1 as frozen: C1[0] (the one mismatch)

Executed (frozen text with the scratch substitution; the frozen form is in `claims.json`):

```
bash .ufo/waves/round-59/controls/c1-probe-run.sh corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ExecCounters/probe-after
```

Shell exit 0 (the runner itself), pipefail exit 0. Decisive stdout:

```
instrument=corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
run-utc=2026-11-03T22:00:36Z host=plazir27
probe=P1-semicolon derive=cat g.txt; touch MARK-P1 exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r59/ExecCounters/probe-after/r-P1-semicolon/corpus/instruments/figure-audit.py': [Errno 2] No such file or directory
probe=CTRL-quoted-separator derive=cat g.txt | awk 'BEGIN{x=1;y=2} {print}' exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r59/ExecCounters/probe-after/r-CTRL-quoted-separator/corpus/instruments/figure-audit.py': [Errno 2] No such file or directory
probe=RESIDUAL-awk-write derive=cat g.txt | awk 'BEGIN{print 1 > "MARK-RES"}{print}' exit=2 markers=0 :: python3: can't open file '/fast/scratch/hyaku/kasegi-r59/ExecCounters/probe-after/r-RESIDUAL-awk-write/corpus/instruments/figure-audit.py': [Errno 2] No such file or directory
```

P2-P8 print the same python open error with their own probe ids (10/10 probe lines carry it; JSON `observation.probes_with_python_open_error`). Therefore the P1-P8 `exit=2 markers=0` half of the want is met vacuously — by `python3` failing to start, not by the gate refusing a derive — while the two probes whose want is `exit=0` (CTRL-quoted-separator `derived=35`; RESIDUAL-awk-write `markers=1`) read `exit=2` and violate the want. Four want violations, all in this one command.

Pointer: `.ufo/waves/round-59/controls/c1-probe-run.sh:8` (`INSTR=$1`) and `:23` (`( cd "$r" && python3 "$INSTR" ... )`) — the instrument path is taken relative to the clone root but resolved after `cd` into `$r`. The committed after-receipt `controls/c1-probes-lane-after-r59.txt:1` records `instrument=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py`, i.e. the lead measured the absolute form, not the frozen command.

## 3. C1[0] diagnostic twin (absolute instrument): all wants match

Executed:

```
bash .ufo/waves/round-59/controls/c1-probe-run.sh /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ExecCounters/probe-after-abs
```

Shell exit 0, pipefail exit 0, 12 stdout lines:

```
instrument=/fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
probe=P1-semicolon derive=cat g.txt; touch MARK-P1 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-semicolon
probe=P2-andand derive=cat g.txt && touch MARK-P2 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-andand
probe=P3-background derive=cat g.txt & touch MARK-P3 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-background
probe=P4-newline derive=cat g.txt|touch MARK-P4 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-newline
probe=P5-cmdsubst derive=cat g.txt $(touch MARK-P5) exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P5-cmdsubst
probe=P6-pipe-tee derive=cat g.txt | tee MARK-P6 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P6-pipe-tee
probe=P7-redirect derive=cat g.txt > MARK-P7 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P7-redirect
probe=P8-oror derive=cat nosuch.txt || touch MARK-P8 exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P8-oror
probe=CTRL-quoted-separator derive=cat g.txt | awk 'BEGIN{x=1;y=2} {print}' exit=0 markers=0 :: FIG CTRL-quoted-separator recorded=35 derived=35 ok
probe=RESIDUAL-awk-write derive=cat g.txt | awk 'BEGIN{print 1 > "MARK-RES"}{print}' exit=0 markers=1 :: FIG RESIDUAL-awk-write recorded=35 derived=35 ok
```

(The `run-utc=` line is the second line of the runner header; it is omitted here only for brevity and is present in the JSON.)

## 4. C1[1]-C1[5]: match

Each command is the frozen `counting_commands[n]` text verbatim with the `   # want:` tail removed.

| # | command (executed) | shell exit | pipefail | decisive stdout |
|---|---|---|---|---|
| 1 | `python3 corpus/instruments/figure-audit.py --selftest \| tail -1` | 0 | 0 | `selftest cases=14 failures=0` |
| 2 | `python3 corpus/instruments/figure-audit-mutbat.py \| tail -1` | 0 | 0 | `mutbat killed=2/2 survivors=0 controls=pass` |
| 3 | `python3 corpus/instruments/figure-audit.py \| tail -1` | 0 | 0 | `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` |
| 4 | `python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json \| grep d53-1` | 0 | 1 | `FIG d53-1-trailer recorded=34 derived=33 want=34 stale` |
| 5 | `sha256sum corpus/instruments/figure-audit.py` | 0 | 0 | `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  corpus/instruments/figure-audit.py` |

C1[4]: the frozen command's own exit code is `grep`'s 0; the claim's red-fixture expectation `exit 1` is the instrument's exit and appears as the diagnostic pipefail exit 1.

## 5. C2[0]-C2[8]: all nine match

| # | command (executed) | shell exit | pipefail | decisive stdout |
|---|---|---|---|---|
| 0 | `python3 corpus/instruments/frontier-recheck-count.py \| grep -E 'FRONTIER-CENSUS\|FRONTIER-PASS F40\|entries='` | 0 | 0 | `FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92` / `FRONTIER-PASS F40 ids=S092` / `entries=43 pass=43 exit=0` |
| 1 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092` | 0 | 0 | `S092:sha256 OK` + 10 `S092:Q<n> OK occurrences=1 anchor=2-ok` lines |
| 2 | `python3 corpus/instruments/capture-binding-check.py \| tail -1` | 0 | 0 | `records=75 bound=75 unbound=0` |
| 3 | `ls corpus/knowledge/*.md \| wc -l` | 0 | 0 | `78` |
| 4 | `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` | 0 | 0 | `78` |
| 5 | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` | 0 | 0 | (no output) |
| 6 | `grep -cE '^\| F40 ' corpus/README.md` | 0 | 0 | `1` |
| 7 | `grep 'Google Big Sleep reporting beyond the tracker' corpus/SOURCES.md \| sha256sum` | 0 | 0 | `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432  -` |
| 8 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` | 0 | 0 | W04 duplicate-URL warning lines, then `file	ok	/fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/SOURCES.md` |

C2[1] full stdout (11 lines) is in the JSON; the aggregate block above counts the 10 Q lines and checks each carries `occurrences=1`.

## 6. Mandated caveat: the frontier counter's recheck lines cd to the lane root

Measured, not inferred:

```
$ grep -n '^recheck:' corpus/knowledge/google-big-sleep-findings-tracker.md | cut -c1-200
6:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092
```

The counter itself anchors its root correctly on the clone (`corpus/instruments/frontier-recheck-count.py:494` default root = the instrument's repo root; `:269` runs the recheck with `cwd=root`), but the entry's recheck line then `cd`s to the lane. Demonstration: `run.py` (`caveat_probes`) appended one line to the clone's capture in-process, then ran the two measurements below as subprocesses (both recorded in the JSON):

```
# precondition: run.py caveat_probes() appended "\nCORRUPTED-BY-ExecCounters round-59 caveat probe\n"
#               to /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/source-snapshots/round-59/S092.txt
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F40|entries='   # exit 0
FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92
FRONTIER-PASS F40 ids=S092
entries=43 pass=43 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092   # exit 1
S092:sha256 MISMATCH expected=048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38 actual=dc6ecb6b208dcb323c356ae77f507415cb1e78e2de87b88ee02b9b23c1b345be
```

So C2[0]'s `FRONTIER-PASS F40 ids=S092` is decided against the lane root, while C2[1] reads the clone and fails closed. Recorded as required; not fixed. Restore and cleanliness:

```
$ git -C /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone checkout -- corpus/source-snapshots/round-59/S092.txt   # exit 0
$ sha256sum /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/source-snapshots/round-59/S092.txt
048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38  /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone/corpus/source-snapshots/round-59/S092.txt
$ git -C /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone status --porcelain corpus/source-snapshots/round-59/S092.txt
(no output)
```

## 7. Residual observations (counter shape; reported, not fixed)

- Pipeline masking: for every frozen command ending `| tail -1` or `| grep ...`, the recorded shell exit is the last stage's. C1[1]-C1[3], C2[0] and C2[2] have pipefail exit 0, so nothing is hidden here; C1[4]'s instrument exit 1 is recoverable only via pipefail (section 4). `run.py` records both, so no number here relies on the masked value.
- C2[0]'s `grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F40|entries='` prints only those three lines; a `FRONTIER-FAIL F40` would have made the expected `FRONTIER-PASS F40` line absent and failed the check, but failures of other rows are not visible in stdout — only via the counter's own exit (pipefail 0 here).
- The frozen C1[0] command is the only one that cannot reproduce its wants as written (section 2). Passing the instrument absolutely restores it (section 3); the committed after-receipt used that form (`controls/c1-probes-lane-after-r59.txt:1`).

## 8. Bounds, writes, cleanup

- Lane files written: `W/ExecCounters.json` and `W/ExecCounters.md` only (the two assigned evidence paths). No pre-existing lane file, ledger, claims snapshot, SOURCES.md, knowledge file or instrument was modified; no git mutation against the lane or the fleet root.
- After the caveat demo restore: `git -C /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone status --porcelain | wc -l` prints 0, and `find /fast/scratch/hyaku/kasegi-r59/ExecCounters/tmp.ToYJAxafk3/clone -name 'MARK-*' | wc -l` prints 0.
- Scratch `/fast/scratch/hyaku/kasegi-r59/ExecCounters` removed before yield (runner and clone included); no leftover.
- No tool installed or upgraded (nothing was needed).
