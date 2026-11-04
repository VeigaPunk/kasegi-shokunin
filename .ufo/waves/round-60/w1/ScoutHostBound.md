FAIL — the round's new instrument, five ledger derives, F41 entry and S093 row are host-free and reproduce from committed bytes on a fresh clone, but the round's harness bytes are not: the C1 selftest count depends on a bare `python` (20/20 cases fail on a python3-only host), the new probe runner depends on GNU `realpath -m` and `hostname` (inetutils) and is not fail-closed (rc 0 with empty or exit=1 evidence when its scratch or instrument is unusable), and new committed receipts/wave tooling hardcode `/home/vgpnk`, `/fast/scratch` and `host=plazir27`. Full list in §7.

L = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Target commit `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`. Scratch `S=/fast/scratch/hyaku/kasegi-r60/ScoutHostBound` (removed before yield; nothing left behind). Read-only on L throughout; no tool installed; `pacman -Qo` queries only, no transaction.

# 1. Lane identity and the exact bytes swept

```
$ git -C L rev-parse HEAD
b8c77fb9fa13710f46d8f564a00af640de5108cd
$ git -C L diff --stat 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD
 .ufo/waves/round-60/build-spec.py    | 207 ++++++++++++
 .ufo/waves/round-60/w1-dispatch.json | 251 +++++++++++++++++++++
 .ufo/waves/round-60/w1-plan.json     |  67 +++++
 .ufo/waves/round-60/w1-spec.json     |  78 +++++
 4 files changed, 603 insertions(+)
```

The lane HEAD is one commit past the target commit; the four added files are wave plan/dispatch only, and none of the target paths changed (`git diff --stat 7f7dd26 HEAD -- <target paths>` is empty). All target-byte facts below are from committed bytes at 7f7dd26.

The probe runner is not in 7f7dd26: it was added by the freeze commit and is unchanged since.

```
$ git -C L log --oneline -- .ufo/waves/round-60/controls/c1-probe-run-r60.sh
66e6241 round-60: freeze — ... probe runner, S093 capture and manifest, assimilation id check
$ git -C L show 66e6241:.ufo/waves/round-60/controls/c1-probe-run-r60.sh | sha256sum
2967d9326b0038c11543144c14fb73ed735918d46e58a1bce6c33113ad8be440  -
$ sha256sum L/.ufo/waves/round-60/controls/c1-probe-run-r60.sh
2967d9326b0038c11543144c14fb73ed735918d46e58a1bce6c33113ad8be440  ...
$ git -C L diff --stat 66e6241 HEAD -- .ufo/waves/round-60/controls/c1-probe-run-r60.sh
(no output, rc 0)
```

Tool baseline read on this host (versions only; nothing installed): bash 5.3.20, git 2.56.0, GNU coreutils 9.12-2 (`realpath`, `date`, `sha256sum`, `mkdir`, `rm`, `ls`, `head`, `cat`, `tr`, `cut`, `wc`), `hostname` from inetutils 2.8-1, python 3.14.8.

# 2. Target 1 — added lines grepped for absolute host paths and host-only tool names

```
$ git -C L show 7f7dd26 -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json \
  | grep '^+' | grep -nE '/fast/scratch|/home/vgpnk|/tmp|/var/tmp'
(no output) ; rc=1
$ git -C L show 7f7dd26 -- corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md \
    corpus/README.md PROVINCE.md | grep '^+' | grep -nE '/fast/scratch|/home/vgpnk|/tmp|/var/tmp'
(no output) ; rc=1
```

The instrument/ledger new lines carry no absolute host path and no host-only tool name. The entry and S093 row do not either: `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:3,6` and `corpus/SOURCES.md:100` cite only lane-relative paths (`corpus/source-snapshots/round-60/S093.txt`, `corpus/source-snapshots/round-60/manifest.json`, `corpus/instruments/source-recheck.py`); `corpus/README.md:1005` and `PROVINCE.md:209` are the same relative shapes.

The runner's added lines do contain host-only tool names (file-line numbers from the committed file):

```
$ git -C L show 66e6241 -- .ufo/waves/round-60/controls/c1-probe-run-r60.sh \
  | grep '^+' | grep -nE '/fast/scratch|/home/vgpnk|/tmp|/var/tmp|hostname|realpath|sha256sum|date -u|git |python3'
10:+INSTR=$(realpath "$1")
11:+S=$(realpath -m "$2")
15:+echo "instrument=$INSTR sha256=$(sha256sum "$INSTR" | cut -c1-16)"
16:+echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname)"
...
25/26:+  python3 -c ... / ( cd "$r" && python3 "$INSTR" ... )
39-43:+  git -C "$r/repo" init/commit/rev-parse ... 
```

No `/fast/scratch`, `/home/vgpnk`, `/tmp` or `/var/tmp` in the runner: its scratch is an argument (`c1-probe-run-r60.sh:9-10`), not a baked path. `hostname` (`:15`) is the one host-only tool name in the runner's own lines; `realpath` (`:9-10`), `shasum` (`:14`) and `date` (`:15`) are tool dependencies, covered in §4.

A wider `git grep` at HEAD over the whole round-60 directory and the five target paths finds host paths only outside the target files:

```
$ git -C L grep -nE '/(fast|home|tmp|var/tmp)/|plazir' HEAD -- .ufo/waves/round-60 <five target paths>
.ufo/waves/round-60/build-spec.py:13:L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
.ufo/waves/round-60/build-spec.py:14:SCR = "/fast/scratch/hyaku/kasegi-r60"
.ufo/waves/round-60/controls/c1-lane-after-r60.txt:1:run-utc=... host=plazir27
.ufo/waves/round-60/controls/c1-lane-after-r60.txt:4:instrument=/home/vgpnk/.../figure-audit.py sha256=35f7bcd3e673b81b
.ufo/waves/round-60/controls/c1-probes-base-r60.txt:1:instrument=/home/vgpnk/... sha256=32e1cddb2291a643
.ufo/waves/round-60/controls/c1-probes-standin-r60.txt:1:instrument=/fast/scratch/hyaku/kasegi-r60/l1/standin/... sha256=35f7bcd3e673b81b
.ufo/waves/round-60/controls/freeze-digests-r60.txt:1-2:... /fast/scratch/hyaku/kasegi-r60/l1/standin/...
.ufo/waves/round-60/claims.json:20:  ... /fast/scratch/hyaku/kasegi-r60/l1/c1-after ...
.ufo/waves/round-60/claims.json:49:  "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md ..."
```

These are described in §7 (H4/H6); none of them is in the five target files, and none changes the frozen-host measurement of C1/C2 (§8).

# 3. Target 2 — each counting/recheck line judged from committed bytes alone

## 3.1 The F41 entry's recheck line (the deliberate no-absolute-`cd` line)

The line is `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:6`. Its command portion (before the `#` note) contains no `cd` and no absolute path:

```
$ sed -n '6p' corpus/knowledge/...md | cut -d'#' -f1 | grep -c 'cd '
0 ; rc=1
$ sed -n '6p' corpus/knowledge/...md | cut -c1-120
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source
```

The frontier counter runs every recheck line with `cwd=root`, exactly as the entry states:

```
$ sed -n '266,270p' corpus/instruments/frontier-recheck-count.py
    if not problems:
        proc = subprocess.run(["bash", "-c", recheck], cwd=root,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        exit_code = proc.returncode
```

Fresh-clone execution (toplevel asserted equal to the clone before the checkout; cwd = clone root, i.e. the counter's `root`; no network, `source-recheck.py:2-6` says "reads only local files"; imports are stdlib only):

```
$ git clone -q --shared L $S/fixture-.../clone && git -C <clone> rev-parse --show-toplevel
<clone>  (assert equals clone) ; rc 0
$ git -C <clone> checkout -q 7f7dd26 ; git -C <clone> rev-parse HEAD
7f7dd267283d2a16ca38d4cb05bed92165cb35cd
$ cd <clone> && python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-60/manifest.json --source S093
rc 0, 16 stdout lines = 1 `S093:sha256 OK` + 15 `S093:Q<n> OK ...` lines
first: S093:sha256 OK
last:  S093:Q15 OK occurrences=1 anchor=281-ok
Q1 = occurrences=2 anchor=12-ok; Q2-Q14 = occurrences=1 with anchors 16/40/51/61/65/68/71/74/82/88/16/16/281
```

The fail-closed semantics stated in the same line are real:

```
missing manifest    -> rc 2, last line "manifest UNAVAILABLE reason=missing"
one appended byte   -> rc 1, "S093:sha256 MISMATCH expected=46f69d32...d96 actual=7f10dfd2...b278"
restored capture    -> rc 0
command from parent -> rc 2 (relative script path absent), i.e. the line is cwd=root-only by design
```

Committed capture numbers agree with the entry/S093 row/manifest: `wc -c -l` on `corpus/source-snapshots/round-60/S093.txt` = `283 40649` and sha256 `46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96`.

Verdict on this line: it resolves from committed bytes alone on a fresh host under the counter's `cwd=root` rule, has no absolute `cd`, no network, and no host tool beyond `python3`. The no-absolute-`cd` choice is correct for export replay.

## 3.2 The runner's lines

The counted shape was re-run from a fresh clone root with the instrument argument relative, exactly as the counting command does (`bash .ufo/.../c1-probe-run-r60.sh corpus/instruments/figure-audit.py <scratch>`):

```
rc 0; 12 stdout lines
header: instrument=<clone>/corpus/instruments/figure-audit.py sha256=35f7bcd3e673b81b   # resolved absolute before cd (R77 holds)
probe=Q1... exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q1-...
probe=Q2... exit=2 markers=0 :: ... reason=derive-not-read-only ... 
probe=Q7... exit=2 markers=0 :: ... reason=derive-not-read-only ...
probe=CTRL-quoted-semicolon ... exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count ... exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
probe=RESIDUAL-python-traversal ... exit=1 markers=0 :: FIG RESIDUAL-python-traversal ... reason=derive-exit-2 stale
scratch removed by trap: yes
```

Every probe derives its inputs from stdin/argv and the scratch root (`c1-probe-run-r60.sh:18-48`); no probe line embeds a host path. The lines do depend on the tools listed in §4. The instrument SHA is printed as 16 hex characters only and is never compared with the claimed full digest (`:14`); the refusal reason is printed but never asserted.

# 4. Target 3 — runner dependencies beyond bash/python3/sha256sum, and writes

Dependency census: a scratch `PATH` shim logged every external command invocation (wrapper: `printf '%s\n' "${0##*/}" >> "$LOGF"; exec <real> "$@"`), then the full runner was run from the fresh clone with `PATH=$shim:/usr/bin:/bin`:

```
$ LOGF=$S/shim.log PATH=$S/shim:/usr/bin:/bin TMPDIR=$S \
  bash <clone>/.ufo/waves/round-60/controls/c1-probe-run-r60.sh $S/instr/figure-audit.py $S/run1
rc 0
TOOLS USED: {'cat': 12, 'cut': 1, 'date': 1, 'git': 6, 'grep': 11, 'head': 10,
             'hostname': 1, 'ls': 10, 'mkdir': 11, 'python3': 21, 'realpath': 2,
             'rm': 2, 'sha256sum': 1, 'tr': 10, 'wc': 1}
```

So beyond bash, python3 and sha256sum the runner needs GNU coreutils (`realpath -m`, `date`, `rm`, `mkdir`, `ls`, `head`, `cat`, `tr`, `cut`, `wc`), `git`, and `hostname` from inetutils — `hostname` is not coreutils (`pacman -Qo /usr/bin/hostname` → "owned by inetutils 2.8-1"). `sed`, `awk`, `sort` and `touch` were shimmed but never invoked: Q3-Q5 are refused at the settings screen before their programs run, so the refusal rows do not need those tools on the host.

`realpath -m` is GNU-only (`-m` is not POSIX); in a script run by bash it resolves to `/usr/bin/realpath` (GNU coreutils 9.12):

```
$ bash --noprofile --norc -c 'type realpath; realpath --version' | head -2
realpath is /usr/bin/realpath
realpath (GNU coreutils) 9.12
```

Writes outside the scratch argument: in a normal run, none observed.

- `realpath -m "$2"` resolves a path string and creates nothing (`$S/relpath` absent after `realpath -m relpath`).
- `realpath "$1"` only resolves the instrument.
- With `HOME` and `XDG_CONFIG_HOME` redirected to scratch, the full run created 0 files under the fake home (walked before/after), and the trap removed the scratch dir (`run1` absent after exit).
- `git init/commit/rev-parse` write only inside `$S/r-*/repo`; the fixture root is asserted (`:40`).

Failure modes (new bytes; no `set -e`, only `set -u` at `:8`; the runner exits 0 in all three):

```
nonexistent instrument:
  instrument= sha256=                     # empty, no error
  probe=Q1... exit=1 markers=0 :: /usr/bin/python3: can't find '__main__' module in '<scratch>/r-Q1-...'
  ... every probe exit=1 markers=0 ; runner rc 0

unusable scratch (`/proc/does-not-exist/hyaku`):
  probe=Q1... exit= markers=0 ::           # empty exit, no rc file
  probe=Q6... FIXTURE-ROOT-MISMATCH
  probe=Q7... FIXTURE-ROOT-MISMATCH
  runner rc 0

empty $2:
  realpath -m '' -> rc 1, stdout empty, so S='' and the per-probe root is '/r-Q1'
```

A host with a global `commit.gpgsign = true` makes the fixture commit fail (stderr `gpg failed to sign the data`), but Q6/Q7 still exit 2 because the write-flag screen refuses before git runs; the runner never checks that the fixture has a HEAD, only the toplevel (`:40`). So the host git config does not change the measured Q6/Q7 rows, but the fixture is not what is being tested.

# 5. Target 4 — compile and Python-version floor

```
$ cp L/corpus/instruments/figure-audit.py $S/compile/ && cd $S/compile \
  && TMPDIR=$S python3 -m py_compile figure-audit.py
rc=0 ; python3 --version = Python 3.14.8
$ python3 - <<'EOF'
import ast
src=open('figure-audit.py').read()
for fv in [(3,8),(3,9),(3,10),(3,12)]:
    ast.parse(src, feature_version=fv); print(fv,"PARSE-OK")
EOF
(3, 8) PARSE-OK
(3, 9) PARSE-OK
(3, 10) PARSE-OK
(3, 12) PARSE-OK
```

The 3.8 grammar check covers the whole file, including the new `split_segments` (line 88), `denied_flag` (156), `segment_ok` (170), `check_read_only` (180) and the six new selftest lines (299-304). No 3.9+ construct was found (no assignment expressions, `match`, `removeprefix`/`removesuffix`, `tomllib`, `except*`, builtin-generic annotations). The new code is plain string/dict logic; no host API.

Pre-existing, but load-bearing on this round's claim: the selftest harness at `corpus/instruments/figure-audit.py:277` runs its per-case subprocess as

```
subprocess.run([bash, "-c", 'python "%s" --ledger "%s" --root "%s"' % (me, lp, tmp)], ...)
```

i.e. it requires a bare `python`, not the interpreter it is running under. Controlled test, same file, same `TMPDIR`, only `PATH` changed to a scratch bin holding symlinks for `bash` and `python3` (the host's `python` is `/usr/bin/python`):

```
PATH=<bash+python3 only>:  python3 figure-audit.py --selftest  -> rc 1, last line "selftest cases=20 failures=20"
normal PATH:               python3 figure-audit.py --selftest  -> rc 0, last line "selftest cases=20 failures=0"
```

`grep -c '^    run_case(' figure-audit.py` = 20 calls, matching `EXPECTED_CASES = 20` at line 63.

# 6. Target 5 — the five rewritten ledger derives

Five derive strings were replaced in 7f7dd26, all to remove `awk`:

```
$ git -C L show 7f7dd26 -- corpus/instruments/figure-audit-ledger.json | grep -c '^-.*"derive"'
5
$ ... | grep '^+.*"derive"' | grep -cE 'awk|sed'
0
$ python3 -c "... all 35 derives ..."
n figures 35 ; awk in any derive: 0 ; sed in any derive: 0
$ python3 -c "... re.search('/fast|/home|/tmp|/var/tmp|(^|[|&;] *)cd ', derive) ..."
derives: 35 with host/absolute/cd: 0
```

The five are `entries-r54`, `figure-audit-mentions-base-log`, `figure-audit-mentions-base-knowledge-expected`, `entries-r55`, `entries-r56`. Their shapes are exactly `git show <rev>:<path> | grep … | cut -d'|' -f5 | tr ',' '\n' | wc -l`, `git cat-file -e <rev>:<path> && git show … | grep … | wc -l`, i.e. only `git show`/`git cat-file`/`grep`/`cut`/`tr`/`wc`. Executed from the fresh clone root (cwd=root, as the instrument does):

```
entries-r54                                   rc=0 out='38'
figure-audit-mentions-base-log                rc=0 out='0'
figure-audit-mentions-base-knowledge-expected rc=0 out='0'
entries-r55                                   rc=0 out='39'
entries-r56                                   rc=0 out='40'
```

All five equal their `want` in the ledger. No host dependency: relative repo paths only, POSIX tools, and the four revs (`5108584…`, `32782bd…`, `133c575…`, `8a5d753…`) are committed history (present in a normal clone; a `--depth` clone would make them `derive-exit-128`, which is a history requirement, not a host dependency).

# 7. Defect list

H1 (pre-existing line, load-bearing on C1; portability, medium). `corpus/instruments/figure-audit.py:277` runs the selftest subprocess as bare `python`. On a GNU/Linux fresh host that ships only `python3` (Debian/Ubuntu default), `python3 corpus/instruments/figure-audit.py --selftest` prints `selftest cases=20 failures=20` and exits 1, so C1's claimed `selftest cases=20 failures=0` is host-conditional. Demonstrated in §5. The six new selftest lines (299-304) are themselves host-free; they are measured through this harness line. Fix (report only, not applied): `sys.executable` instead of `python`.

H2 (new runner; portability, medium). `.ufo/waves/round-60/controls/c1-probe-run-r60.sh:10` uses `realpath -m`, a GNU coreutils extension (absent from BSD/macOS `realpath` and from a POSIX-only userland), and `:15` calls `hostname`, which is inetutils on this host (`pacman -Qo /usr/bin/hostname` → inetutils 2.8-1), not coreutils. Neither is in the shell's declared baseline (bash/python3/sha256sum). On a host without GNU `realpath -m`, `S` becomes empty and the runner continues (§4).

H3 (new runner; verifiability, high). The runner is not fail-closed: no `set -e` (`:8` is `set -u` only), and it returns 0 in every failure mode. A nonexistent instrument yields `instrument= sha256=` and `exit=1`, not an abort; an unusable scratch yields `exit=` empty and two `FIXTURE-ROOT-MISMATCH` rows, not an abort; the printed SHA is 16 hex characters (`:14`) and is never compared with the claimed digest; `reason=derive-not-read-only` is printed but never asserted. A per-probe PASS is therefore readable as "exit=2 markers=0" only while the harness is healthy, and the command's exit status (always 0) carries no information. On a host where the counted scratch path cannot be created, C1's counting command still returns 0 with empty evidence.

H4 (new committed data; host-stamped evidence, low). New committed receipts embed this host's absolute lane path and hostname: `c1-lane-after-r60.txt:1` (`host=plazir27`) and `:4` (`instrument=/home/vgpnk/Projects/shokunin/kasegi-shokunin/...`); same in `c1-probes-base-r60.txt:1-2`, `c1-probes-standin-r60.txt:1-2` (`/fast/scratch/...`), `c1-standin-after-r60.txt:1`, `c2-lane-after-r60.txt:1`, `do-nothing-c1-r60.txt:1`, `freeze-digests-r60.txt:1-2`. New round-60 wave tooling hardcodes the same roots: `.ufo/waves/round-60/build-spec.py:13-14` (`L = "/home/vgpnk/..."`, `SCR = "/fast/scratch/..."`). These are data/tooling, not the claim path; they make round receipts non-identical across hosts.

H5 (new runner; hazard, low). `S=$(realpath -m "$2")` is not guarded (`:10`, `:11`): an empty `$2` fails to resolve (rc 1, empty stdout) and the per-probe root becomes `/r-Q1`; `--` does not prevent anything; passing `.` resolves to the caller's cwd and `rm -rf -- "$S"` deletes it. The runner needs a `case "$S" in /|"") exit 2;; esac`-style guard and an explicit "scratch under the designated root" check; report only.

H6 (carried convention, not new). C2 counting command 9 (`claims.json:49`) invokes `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane. The path is a long-standing convention, not a round-60 introduction:

```
$ grep -rl 'scripts/sources-census.sh' .ufo/waves/*/claims.json | head -10
round-25 ... round-34 claims.json
$ grep -rc 'scripts/sources-census.sh' .ufo/waves/*/claims.json | grep -v ':0' | tail -5
round-43:1  round-47:1  round-58:1  round-59:1  round-60:1
```

It is host-bound but pre-dates this round; a lane-local copy or a lane-relative invocation would make C2's last command portable. Report only.

# 8. What is clean (no defect found)

- The new instrument lines (`split_segments` 88, `denied_flag` 156, `segment_ok` 170, `check_read_only` 180, selftest 299-304, `EXPECTED_CASES` 63) contain no host path, no host-only tool and no API outside the standard library; the file parses under Python 3.8 grammar (§5) and compiles (§5).
- The five rewritten derives are exactly `git show`/`git cat-file`/`grep`/`cut`/`tr`/`wc`, have no `awk`/`sed`, no absolute path and no `cd`, and reproduce 38/0/0/39/40 from a fresh clone (§6).
- The F41 entry's recheck line (entry:6) is relative, has no `cd`, runs green from a fresh clone under the counter's `cwd=root` rule (1 sha OK + 15 Q lines, Q1 occurrences=2 anchor=12-ok, the rest occurrences=1), fails closed on a missing manifest (2) and a tampered capture (1), and needs only `python3` (§3.1).
- The S093 row (`corpus/SOURCES.md:100`), README F41 row (`corpus/README.md:1005`) and PROVINCE amendment (`PROVINCE.md:209`) contain no absolute host path; the capture's committed numbers match (`283` lines, `40649` bytes, sha `46f69d32…7d96`).
- The runner's probes match the lane receipt row-for-row on this host: Q1-Q7 exit 2 markers 0 with `reason=derive-not-read-only`, both controls exit 0 with derived 35 and 1, RESIDUAL exit 1 (not gate-refused), and the instrument resolves absolute before the per-probe `cd` (R77) (§3.2).
