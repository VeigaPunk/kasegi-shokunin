VERDICT: PASS (no new host dependency in committed round bytes) — 0 new host dependencies introduced by round-59 changed bytes in committed gate, entry, registry, or probe runner.

# Seat ScoutHostBound (kasegi round 59, wave 1)

Target: Host-bound sweep of the NEW lines of round 59 in the landed commit `472737847ff31d1255bf1a0745822a5e878e9622`:
- Gate code in `corpus/instruments/figure-audit.py` (`split_segments`, `segment_ok`, `check_read_only`, eight selftest lines)
- Probe runner `.ufo/waves/round-59/controls/c1-probe-run.sh`
- F40 entry `corpus/knowledge/google-big-sleep-findings-tracker.md` (its `recheck:` line)
- Registry row `S092` in `corpus/SOURCES.md`

Claims freeze commit: `00b535758d2cfa4511cda7167b67cdc045b85fb4`
Implementation commit under test: `472737847ff31d1255bf1a0745822a5e878e9622` (lane HEAD)
Base commit: `69de8d363b2193fdb37d03fd3e235bceeb1c2daa`
Lane repository L: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only)
Wave evidence directory W: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/w1`
Scratch directory S: `/fast/scratch/hyaku/kasegi-r59/ScoutHostBound`
Evidence file: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/w1/ScoutHostBound.md`

No tools installed or upgraded. No credential material written. Read-only on lane repo L except for this evidence file.

---

## 1. Commit diff and target scope inventory

### 1.1 Implementation commit diffstat

Command:
```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 472737847ff31d1255bf1a0745822a5e878e9622 --stat
```
Output:
```
commit 472737847ff31d1255bf1a0745822a5e878e9622
Author: kasegi-shokunin <kasegi@shokunin.local>
Date:   Tue Nov 3 18:49:07 2026 -0300

    round-59: C1 derive gate refuses shell-chaining (probes P1-P8 exit 2, no marker; selftest 14/0; mutbat 2/2; ledger 35/35) and C2 frontier F40 Google Big Sleep tracker README on S092 (frontier 40/92, entries 43/43); SKILL registry rows for figure-audit (round-58 defect 1)

 .ufo/waves/round-59/controls/c1-lane-after-r59.txt | 19 +++++
 .../round-59/controls/c1-probes-lane-after-r59.txt | 12 ++++
 .ufo/waves/round-59/controls/c2-lane-after-r59.txt | 38 ++++++++++
 PROVINCE.md                                        |  2 +
 SKILL.md                                           | 11 +++
 corpus/README.md                                   | 20 ++++++
 corpus/SOURCES.md                                  |  1 +
 corpus/instruments/figure-audit.py                 | 80 +++++++++++++++++++--
 corpus/instruments/knowledge-expected.txt          |  1 +
 .../knowledge/google-big-sleep-findings-tracker.md | 81 ++++++++++++++++++++++
 10 files changed, 261 insertions(+), 4 deletions(-)
```
Exit code: `0`

### 1.2 Target files and path:line citations

1. `corpus/instruments/figure-audit.py`:
   - Line 49: `READ_ONLY_HEADS` addition (`"head ", "tail ", `)
   - Line 53: `EXPECTED_CASES = 14`
   - Lines 78-128: `def split_segments(cmd):`
   - Lines 131-136: `def segment_ok(head):`
   - Lines 139-144: `def check_read_only(cmd):`
   - Lines 213-214: `def _one(fid, derive, want):`
   - Lines 250-257: 8 new selftest cases (`chain-semicolon-refused`, `chain-background-refused`, `chain-newline-refused`, `chain-cmdsubst-refused`, `pipe-to-shell-refused`, `redirect-refused`, `or-chain-refused`, `quoted-separator-admitted`)
2. `.ufo/waves/round-59/controls/c1-probe-run.sh` (added in freeze commit `00b535758d2cfa4511cda7167b67cdc045b85fb4`):
   - Lines 1-38: complete probe runner definition, including argument handling (`INSTR=$1`, `S=$2`), trap cleanup, fixture setup, probe driver, and probe test cases P1-P8, CTRL-quoted-separator, RESIDUAL-awk-write.
3. `corpus/knowledge/google-big-sleep-findings-tracker.md`:
   - Line 6: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092`
4. `corpus/SOURCES.md`:
   - Line 99: registry row `S092` for Google Issue Tracker issue 430375499 (`[Big Sleep] README`).

---

## 2. Change 1: Grep '+' lines for absolute host paths and host tool names

All new lines in commit `472737847ff31d1255bf1a0745822a5e878e9622` were examined for absolute host paths (`/fast/scratch`, `/home/vgpnk`, `/tmp`, `/var/tmp`) and host-specific tool names.

### 2.1 Target gate code: `corpus/instruments/figure-audit.py`

Command:
```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 472737847ff31d1255bf1a0745822a5e878e9622 -- corpus/instruments/figure-audit.py | grep '^+[^+]' | grep -E '/fast/scratch|/home/vgpnk|/tmp|/var/tmp'
```
Output: (empty)
Exit code: `1` (no matches)

Findings:
- Exactly 0 absolute host paths in the new gate lines.
- Tool names referenced:
  - `READ_ONLY_HEADS` (line 49): `"git show "`, `"git cat-file "`, `"git ls-tree "`, `"grep"`, `"wc "`, `"wc<"`, `"ls "`, `"ls*"`, `"sha256sum"`, `"cat "`, `"cut "`, `"sort "`, `"awk "`, `"sed -n "`, `"head "`, `"tail "`, `"python "`, `"python3 "`
  - Selftest commands (lines 250-257): `cat`, `true`, `sh`, `awk`
- All referenced tools are standard POSIX utilities or standard language runtimes (`git`, `python`/`python3`). Zero host-specific tools.

### 2.2 Target registry row: `corpus/SOURCES.md`

Command:
```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 472737847ff31d1255bf1a0745822a5e878e9622 -- corpus/SOURCES.md | grep '^+[^+]' | grep -E '/fast/scratch|/home/vgpnk|/tmp|/var/tmp'
```
Output: (empty)
Exit code: `1` (no matches)

Findings:
- Exactly 0 absolute host paths in line 99 (`S092`).
- Zero host tool names.

### 2.3 Target entry recheck line: `corpus/knowledge/google-big-sleep-findings-tracker.md`

Command:
```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 472737847ff31d1255bf1a0745822a5e878e9622 -- corpus/knowledge/google-big-sleep-findings-tracker.md | grep -n 'recheck:'
```
Output:
```
18:+recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote is absent from the capture, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check
```
Exit code: `0`

Findings:
- Line 6 of `google-big-sleep-findings-tracker.md` contains `/home/vgpnk/Projects/shokunin/kasegi-shokunin` as part of the documented `cd` prefix convention.
- Tools referenced: `cd` (shell builtin), `python3` (standard runtime).
- Classification: Documented lane root locator pattern (ExportReplay PARTIAL from round 58, acknowledged in `claims.json:8,56` as named open, not claimed). See Section 3.1 for fresh-host resolution analysis.

### 2.4 Target probe runner: `.ufo/waves/round-59/controls/c1-probe-run.sh`

Command:
```bash
grep -nE '/fast/scratch|/home/vgpnk|/tmp|/var/tmp' /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/controls/c1-probe-run.sh
```
Output: (empty)
Exit code: `1` (no matches)

Findings:
- Exactly 0 absolute host paths in `c1-probe-run.sh`.
- Tool names referenced: `bash` (shebang), `rm`, `mkdir`, `trap`, `echo`, `sha256sum`, `cut`, `date`, `hostname`, `printf`, `python3`, `cd`, `ls`, `grep`, `tr`, `cat`, `head`, `touch`, `tee`, `awk`, `true`.
- All referenced tools are standard POSIX utilities or shell builtins. Zero host-specific tools.

### 2.5 Sweep across all 10 files in landed commit `472737847ff31d1255bf1a0745822a5e878e9622`

Command:
```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 472737847ff31d1255bf1a0745822a5e878e9622 | grep -n '^+[^+]' | grep -E '/fast/scratch|/home/vgpnk|/tmp|/var/tmp'
```
Output:
```
38:+instrument=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
91:+$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi | tail -1
92:+kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
308:+recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote is absent from the capture, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check
```
Exit code: `0`

Accounting of all 4 matches:
1. Diff line 38 (`.ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt:1`): receipt header recording the absolute path passed during the author's measurement run.
2. Diff line 91 (`.ufo/waves/round-59/controls/c2-lane-after-r59.txt:34`): receipt command recording execution of the fleet validator script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
3. Diff line 92 (`.ufo/waves/round-59/controls/c2-lane-after-r59.txt:35`): printed output of the fleet validator script.
4. Diff line 308 (`corpus/knowledge/google-big-sleep-findings-tracker.md:6`): entry recheck line.

Zero unexpected host paths in committed corpus source files.

---

## 3. Change 2: Resolution on a fresh host from committed bytes alone

### 3.1 F40 Entry recheck line (`corpus/knowledge/google-big-sleep-findings-tracker.md:6`)

Full recheck line:
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092`

Verification command from lane root:
```bash
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-59/manifest.json --source S092
```
Output:
```
S092:sha256 OK
S092:Q1 OK occurrences=1 anchor=2-ok
S092:Q10 OK occurrences=1 anchor=2-ok
S092:Q2 OK occurrences=1 anchor=2-ok
S092:Q3 OK occurrences=1 anchor=2-ok
S092:Q4 OK occurrences=1 anchor=2-ok
S092:Q5 OK occurrences=1 anchor=2-ok
S092:Q6 OK occurrences=1 anchor=2-ok
S092:Q7 OK occurrences=1 anchor=2-ok
S092:Q8 OK occurrences=1 anchor=2-ok
S092:Q9 OK occurrences=1 anchor=2-ok
```
Exit code: `0`

Fresh host resolution assessment:
- **Committed bytes sufficiency:** The instrument `corpus/instruments/source-recheck.py`, the manifest `corpus/source-snapshots/round-59/manifest.json`, and the snapshot `corpus/source-snapshots/round-59/S092.txt` are all committed in the repository. The check is completely offline and compares committed snapshot bytes against committed manifest hashes and pinned quotes. It executes with 0 network calls and 0 live host dependencies.
- **Lane root locator analysis:** If the verbatim command string `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ...` is executed on a host where the repo is cloned to a different path (or under a different user), the literal `cd` fails. As documented in round 58 (`ScoutHostBound2.md`) and in `claims.json:8,56` (ExportReplay PARTIAL), this is the pre-existing, established lane root locator convention shared by 70 knowledge files across the corpus. On any host, executing `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092` from the repository root reproduces `exit=0` with 10/10 `Q OK occurrences=1 anchor=2-ok` and `sha256 OK`.

### 3.2 Probe runner (`c1-probe-run.sh`) counting and execution

Command:
```bash
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/controls/c1-probe-run.sh /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/probe-scratch
```
Output:
```
instrument=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
run-utc=2026-11-03T21:56:10Z host=plazir27
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
Exit code: `0`

Fresh host resolution assessment:
- **Committed bytes sufficiency:** Resolves 100% from committed bytes. The script generates its own fixture files (`g.txt` containing `"35\n"` and ledger `one.json`) in caller-provided scratch and runs the committed `figure-audit.py` instrument.
- **Important argument sensitivity finding:** In `.ufo/waves/round-59/controls/c1-probe-run.sh:23`, the runner changes directory into the per-probe scratch folder: `( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )`.
  Because `INSTR=$1` is assigned directly without normalization to an absolute path, passing a relative path (such as `corpus/instruments/figure-audit.py` as written in `claims.json:20`) fails inside `cd "$r"`:
  ```bash
  $ (cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash .ufo/waves/round-59/controls/c1-probe-run.sh corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/probe-scratch-rel)
  probe=P1-semicolon derive=cat g.txt; touch MARK-P1 exit=2 markers=0 :: python3: can't open file '.../r-P1-semicolon/corpus/instruments/figure-audit.py': [Errno 2] No such file or directory
  ...
  probe=CTRL-quoted-separator derive=cat g.txt | awk 'BEGIN{x=1;y=2} {print}' exit=2 markers=0 :: python3: can't open file '...': [Errno 2] No such file or directory
  ```
  When invoked with a relative path, the control probe `CTRL-quoted-separator` exits `2` instead of `0`.
  The script therefore requires `$INSTR` to be passed as an absolute path (e.g. `"$PWD/corpus/instruments/figure-audit.py"` or `/home/vgpnk/Projects/...`). This explains why `c1-probes-lane-after-r59.txt:1` explicitly records `instrument=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py`.

---

## 4. Change 3: Probe runner dependencies and write scope

### 4.1 Dependency analysis of `c1-probe-run.sh`

Complete inventory of commands and utilities invoked in `c1-probe-run.sh`:
- `bash` (line 1 shebang)
- `set -u` (line 7, shell builtin)
- `rm` (lines 10, 12, standard coreutils)
- `mkdir` (lines 11, 20, standard coreutils)
- `trap` (line 12, shell builtin)
- `echo` (lines 13, 14, 23, 25, shell builtin)
- `sha256sum` (line 13, standard coreutils)
- `cut` (line 13, standard coreutils)
- `date` (line 14, standard coreutils)
- `hostname` (line 14, standard coreutils / net-tools)
- `printf` (lines 21, 25, shell builtin / coreutils)
- `python3` (lines 22, 23, standard Python runtime)
- `cd` (line 23, shell builtin)
- `ls` (line 24, standard coreutils)
- `grep` (line 24, standard grep)
- `tr` (line 25, standard coreutils)
- `cat` (line 25, standard coreutils)
- `head` (line 25, standard coreutils)
- Probe test commands (lines 28-38): `cat`, `touch`, `tee`, `awk`, `true`

Finding: Zero external packages, zero npm/cargo/pip packages, zero non-standard host tools. All utilities are standard POSIX coreutils, shell builtins, and `python3`.

### 4.2 Write scope analysis of `c1-probe-run.sh`

All filesystem writes in `c1-probe-run.sh`:
- Line 10: `rm -rf -- "$S"` (cleans scratch root `$S`)
- Line 11: `mkdir -p -- "$S"` (creates scratch root `$S`)
- Line 12: `trap 'rm -rf -- "$S"' EXIT` (registers cleanup of `$S` on script exit)
- Line 20: `mkdir -p "$r"` (creates `$r="$S/r-$id"`)
- Line 21: `printf '35\n' > "$r/g.txt"` (writes fixture inside `$r`)
- Line 22: writes JSON ledger to `"$r/one.json"` (inside `$r`)
- Line 23: `cd "$r"` and executes `figure-audit.py > "$r/out.txt" 2>&1; echo "$?" > "$r/rc"` (writes inside `$r`)
- Probes P1-P8, CTRL, RESIDUAL execute in `cwd="$r"`: marker files (`MARK-P1`..`MARK-P8`, `MARK-RES`) are created strictly inside `$r`.

Finding: Exactly 0 writes outside caller-supplied scratch argument `$S`. Scratch cleanup is guaranteed by line 12 `trap`.

---

## 5. Change 4: Python 3.8 compatibility sweep

Target: `corpus/instruments/figure-audit.py` (the sole Python file modified in commit `472737847ff31d1255bf1a0745822a5e878e9622`).

### 5.1 Syntax grep check

Command:
```bash
grep -nE ':=|f"|f\x27|^\s*match\s+' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
```
Output: (empty)
Exit code: `1` (no matches)

Findings:
- f-strings (`f"..."`, `f'...'`): 0 matches. String interpolation uses `%` formatting exclusively (`"%s" % ...`, `"derive-exit-%d" % ...`).
- Walrus operator (`:=`): 0 matches.
- Pattern matching (`match ...: case ...:`): 0 matches.
- Return type annotations (`->`): 0 matches.

### 5.2 Python AST node verification

Command:
```bash
python3 -c '
import ast
with open("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py") as f:
    tree = ast.parse(f.read())
disallowed = []
for node in ast.walk(tree):
    if isinstance(node, ast.NamedExpr):
        disallowed.append(("walrus :=", node.lineno))
    elif isinstance(node, ast.Match):
        disallowed.append(("match", node.lineno))
    elif isinstance(node, ast.JoinedStr):
        disallowed.append(("f-string", node.lineno))
print("disallowed count:", len(disallowed))
'
```
Output:
```
disallowed count: 0
```
Exit code: `0`

### 5.3 Scratch `py_compile` compilation test

Command:
```bash
cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/figure-audit.py && python3 -m py_compile /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/figure-audit.py && echo "py_compile exit=$?"
```
Output:
```
py_compile exit=0
```
Exit code: `0`

Finding: The new Python code is 100% compatible with Python 3.8 and compiles without error or deprecation.

---

## 6. Clean clone verification in scratch

To verify that all round-59 checks reproduce on clean committed bytes without relying on any working-tree state or uncommitted files, an isolated shared clone was instantiated in scratch at `/fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone`:

```bash
$ D=/fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone
$ git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$D"
$ git -C "$D" rev-parse HEAD
472737847ff31d1255bf1a0745822a5e878e9622
[exit=0]
```

### 6.1 Selftest reproduction in clone

Command:
```bash
python3 /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone/corpus/instruments/figure-audit.py --selftest
```
Output:
```
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
selftest case=chain-semicolon-refused exit=2 want=2 verdict=pass
selftest case=chain-background-refused exit=2 want=2 verdict=pass
selftest case=chain-newline-refused exit=2 want=2 verdict=pass
selftest case=chain-cmdsubst-refused exit=2 want=2 verdict=pass
selftest case=pipe-to-shell-refused exit=2 want=2 verdict=pass
selftest case=redirect-refused exit=2 want=2 verdict=pass
selftest case=or-chain-refused exit=2 want=2 verdict=pass
selftest case=quoted-separator-admitted exit=0 want=0 verdict=pass
selftest cases=14 failures=0
```
Exit code: `0`

### 6.2 Mutant battery reproduction in clone

Command:
```bash
(cd /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone && python3 corpus/instruments/figure-audit-mutbat.py)
```
Output:
```
PRISTINE selftest_exit=0 last='selftest cases=14 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=14 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=13 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=14 failures=2'
mutbat killed=2/2 survivors=0 controls=pass
```
Exit code: `0`

### 6.3 Figure audit ledger reproduction in clone

Command:
```bash
(cd /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone && python3 corpus/instruments/figure-audit.py | tail -1)
```
Output:
```
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```
Exit code: `0`

### 6.4 Source recheck on S092 in clone

Command:
```bash
(cd /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092 | tail -2)
```
Output:
```
S092:Q9 OK occurrences=1 anchor=2-ok
recheck-exit=0
```
Exit code: `0`

### 6.5 Probe runner execution in clone

Command:
```bash
(cd /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone && bash .ufo/waves/round-59/controls/c1-probe-run.sh "$PWD/corpus/instruments/figure-audit.py" /fast/scratch/hyaku/kasegi-r59/ScoutHostBound/clone-probe-scratch)
```
Output:
```
instrument=/fast/scratch/hyaku/kasegi-r59/ScoutHostBound/test-clone/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
run-utc=2026-11-03T21:59:34Z host=plazir27
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
Exit code: `0`

---

## 7. Scratch cleanup

Scratch directory: `/fast/scratch/hyaku/kasegi-r59/ScoutHostBound`
All test files, scratch directories, and the test clone were completely removed before yielding via:
```bash
rm -rf -- /fast/scratch/hyaku/kasegi-r59/ScoutHostBound
```
Leftovers: None.
