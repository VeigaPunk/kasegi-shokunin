VERDICT: BROKEN

# R46SentinelGate: security review of the frozen round-46 counters

Scope: `corpus/instruments/r46-c1-gate.py`, `corpus/instruments/r46-c2-gate.py`, `.ufo/waves/round-46/controls/freeze-controls.py` at freeze commit 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5. Counters were run as the frozen bytes (sha256 b0c730c8… C1, 0ee95857… C2, 6560c0f2… controls; these equal the live lane files at the time of the run). Base export: `git archive 914ca0b6… corpus`. No counter was edited. No git mutation. No live target touched. Scratch under `/fast/scratch/hyaku/kasegi-r46/R46SentinelGate/` (removed on exit).

Functional controls are not the problem: `controls total=9 red=9 green=0`, exit 0. None of the 9 controls tests execution, confinement, or write behaviour, so they cannot falsify S1-S3 below.

## Answer to the assignment question

Executing tree-supplied `recheck:` lines is the lane's existing model: `recheck-audit.py:97` runs `subprocess.run(["bash", "-c", cmd], cwd=cwd, ..., timeout=300)` with no sandbox. So for lane-owned, committed, human-read history on the operator's workstation it is an accepted trust level.

It is NOT acceptable for a candidate tree that a builder seat wrote, because C1 aggregate mode is the first thing that executes that tree. Builder drafts are LLM output, and round-46 reads web captures (S073), so an injected instruction can place a shell line in a `recheck:` field [INFERENCE: path not reproduced end-to-end]. The gate would then run it with the operator's full environment, which holds credential-bearing variables (see T1).

Smallest safe change is in the Fix section: an argv allow-list before execution, a sandboxed run, and instrument resolution from the grader's lane. The allow-list alone is insufficient (T6).

## S1 HIGH: aggregate C1 runs every tree-supplied recheck line under `bash -c` with the full environment

Code:
- `r46-c1-gate.py:160` `bash -n -c line` (parse only).
- `r46-c1-gate.py:163` `cmd = CD_RE.sub("", line, count=1)` strips `cd <lane> && `.
- `r46-c1-gate.py:165` `subprocess.run(["bash", "-c", cmd], cwd=root, capture_output=True, timeout=180)`. cwd is the candidate TREE. No `env -i`, no netns, no uid drop. Runs for BASE and TREE.
- `r46-c1-gate.py:186-188` (L3 `~/` and `/home/` rejection) runs only after `classify()` has already executed every line.

PoC T1 (benign marker, hostile line in an unrelated entry `citation-bases.md`). Command: `python3 -I frozen/r46-c1-gate.py --root poc/t1-hostile-exec --baseline base --work work/t1`. Marker payload writes `id -un`, `pwd` and presence (not values) of four variables. Marker printed:

```
vgpnk
/fast/scratch/hyaku/kasegi-r46/R46SentinelGate/poc/t1-hostile-exec
HOME=set
SSH_AUTH_SOCK=set
GITHUB_TOKEN=unset
OP_SERVICE_ACCOUNT_TOKEN=set
```

Counter output for the same run (do-nothing control: `gated=24`, `L2 regrounded=0`):
```
gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=1 citation-bases.md
gate L3 pass=0 read=bad=citation-bases.md
c1-gate fixed=1/7 exit=1
```
The hostile line also lowered the gated count (24 -> 23) by exiting 0. L1 alone is therefore tree-controlled. L2-L4 catch it here, but only because of a separate check.

Impact: arbitrary command execution as the grader user with its environment. Presence of `SSH_AUTH_SOCK` and `OP_SERVICE_ACCOUNT_TOKEN` in the grader environment is shown above; values were not read or recorded.

Discrimination: do-nothing control on the same counter gives `gated=24 ... fixed=1/7 exit=1` with no marker written.

## S2 HIGH: L6 mutation writes outside `--root` and `--work` (absolute anchor, or in-tree symlink)

Code:
- `r46-c1-gate.py:209` anchor regex `` `([A-Za-z0-9_./-]+):(\d+)(?:-(\d+))?` `` accepts a leading `/`.
- `r46-c1-gate.py:218` `fp = os.path.join(sc, m.group(1))`. Python's `os.path.join` discards `sc` when the second argument is absolute.
- `r46-c1-gate.py:216` `shutil.copytree(..., symlinks=True)` copies in-tree symlinks as links, so `open(fp,"w")` at :222/:228 writes through them.
- L6 never calls `check_row()`, which has the confinement (`:110-114`: ANCHOR_DIRS, no `..`, `islink`, `realpath` under root). The check exists but is not applied on the mutation path.

PoC T2 (absolute anchor in a regrounded entry; `claim-gates.md` recheck set to `true`, so it is base-gated and becomes "executes", i.e. in R):
```
--- T2 victim BEFORE: .../poc/victim/victim.txt
line one VICTIM-TOKEN here
line two keep
=== T2 absolute anchor in a regrounded entry (L6 mutation path)
gate L6 pass=0 read=mutants=2 survivors=none
--- T2 victim AFTER: .../poc/victim/victim.txt
line one ############ here
line two ####
```
PoC T3 (in-tree symlink `corpus/instruments/linkvictim.txt -> <outside>/victim2.txt`):
```
--- T3 victim2 BEFORE: .../poc/victim/victim2.txt
VICTIM2-TOKEN untouched-line
gate L6 pass=0 read=mutants=1 survivors=none
--- T3 victim2 AFTER: .../poc/victim/victim2.txt
############# untouched-line
```
The same row fails per-entry mode, which is the protection that L6 bypasses:
```
$ python3 -I frozen/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md --root poc/t2-abs-anchor-write
row G1 ok=0 read=anchor-dir-or-self
reground entry=claim-gates.md rows=2 ok=0 files=0 exit=1
$ (T7: corpus/instruments -> outside dir symlink, 6 rows)
row G5 ok=0 read=anchor-not-a-regular-file-in-tree
```

Impact: the grader overwrites any file it can read and write, selected by line range or token, before any verdict is printed. Only one base-gated entry needs its recheck line changed (for example to `true`), which is trivial. The write happens even though the run exits 1.

Discrimination: the do-nothing control writes nothing (`mutants=0`). The T7 per-entry run shows that confinement holds on the per-entry path.

## S3 MEDIUM: the timeout does not contain child processes; the hostile tree controls grader time

`subprocess.run(..., timeout=180)` kills only the direct `bash` (`:165-167`). PoC T4, recheck line `sleep 4321 & echo started`:
```
gate L7 pass=0 read=still-gated=24 changed=citation-bases.md
c1-gate fixed=0/7 exit=1
elapsed=185s
orphan still alive (pgrep -af 'sleep 4321'):
2007353 sleep 4321
```
The child survived the counter's exit. I killed that orphan (pid 2007353) afterwards. Lines run serially, so the worst case is 64 lines x 180 s, about 3 h [INFERENCE from the code, not run].

## S4 LOW: `--entry` reads outside `--root`

`r46-c1-gate.py:126` `os.path.relpath(entry, root)` for an absolute entry yields `../..` paths, and `:127` reads them with no confinement. PoC: entry `poc/outside.md` (outside the root) with a `## Re-ground (round 46)` table:
```
$ python3 -I frozen/r46-c1-gate.py --entry $S/poc/outside.md --root $S/base
row G1 ok=0 read=anchor-not-a-regular-file-in-tree
reground entry=outside.md rows=1 ok=0 files=0 exit=1
```
Read-only. It prints row ids and the first cell of rows from that file, so the disclosure is minimal.

## S5 LOW: C2 pin override by environment; tree-level instrument is refused when pins are on

Pins work by default. `r46-c2-gate.py:243-245` checks the sha of `source-recheck.py` against the pin, and `:246` runs it with `-I`. PoC T5 (counter copied into a tree, malicious `source-recheck.py` that writes a marker):
```
gate G4 pass=0 read=source-recheck-not-the-pinned-bytes
marker exists: False
```
But `r46-c2-gate.py:66-67` `if os.environ.get("R46_PINS_OVERRIDE"): PINS.update(json.load(open(...)))` lets the environment null the pin. PoC T5b with `R46_PINS_OVERRIDE={"source-recheck.py": null}`:
```
gate G4 pass=0 read=recheck-rc=0 quotes-ok=0 frozen-cores-missing=0
marker exists after override: True
```
Impact: a grader environment that inherits this variable runs tree code. The variable is documented as selftest-only, but nothing enforces that. Also, the usage line at `:39` (`python3 corpus/instruments/r46-c2-gate.py --root TREE`) runs the counter copy from the tree; `TOOL_ROOT` is then the tree, which the pin catches (T5) but which should not be the documented form.

## S6 LOW: `freeze-controls.py` interpolates operator arguments into a shell

`freeze-controls.py:29` `subprocess.run("git -C %s archive %s corpus | tar -x -C %s" % (lane, a.base, d), shell=True)`. Operator-supplied only, not tree-supplied. PoC with `--lane "/nonexistent;touch <scratch>/poc/marks/inject-via-lane-arg"`:
```
[exit=1] (AssertionError expected after the injected touch)
-rw-r--r-- 1 vgpnk vgpnk 0 ... inject-via-lane-arg
```
The injected `touch` ran. Also `freeze-controls.py:18` `shutil.rmtree(work, ignore_errors=True)` accepts any `--work` path with no guard (code-read; not run).

## S7 LOW: C2 G7 runs an unpinned fleet-root script

`r46-c2-gate.py:54` `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` and `:295` run by list form with `--file <tree>/corpus/SOURCES.md`. The list form has no shell injection. The census script was read-only (grep for `eval`, `git`, command substitution on tree data; `--file` at lines 498-502; use of tree paths at 562-566 is `[ ! -e "$dir/$path" ]` only). So the tree cannot execute census code. The script itself has no sha pin, so any change to the fleet file changes C2 G7 without a lane-visible change.

## S8 INFO: negative results (checked, holding)

- No argument injection: every C2 `run()` call and every C1 `subprocess.run` is list-form; `--entry` values are built from filenames prefixed `corpus/knowledge/`.
- C1 per-entry confinement holds (`check_row`, :110-114): T7 symlinked `corpus/instruments` is rejected (`anchor-not-a-regular-file-in-tree`); absolute anchors and `..` are rejected (T2 per-entry).
- `source-recheck.py` path handling holds: `source-recheck.py:120` rejects absolute `path`, `:159-160` resolve + `commonpath` keeps the capture under the manifest directory. Its only `subprocess` (`:304`) is inside `selftest()`, which runs itself.
- C2 pins hold without the override (T5).

## Fix (recommended, smallest first; do not edit the counters without the lane's approval)

1. Allow-list before execution (C1 `classify`, before :165). Accept only the line shapes the corpus uses: an optional `cd <path> && ` prefix; then `&&`-joined segments of `test -d|-e|-f|-s|! -e` on `~/Projects/...` or `corpus/...`; `python3 corpus/instruments/<name>.py <args>`; `git -C ~/Projects/... rev-parse HEAD`; `set -o pipefail`; and a single literal `| grep -x '...'` pipe. Reject everything else as "not gated, unrecognised". Metacharacters `; ` $ < > ( ) { } \` and quotes are rejected except in that grep literal.
   Verified: `poc/allowlist.py` allowed 64/64 current corpus recheck lines. Rejected: `sh -c`, bare `true`, `sleep 4321 & echo`, `;`-chained `curl|sh`, `$(id)`, `python3 -I /tmp/evil.py`.
2. Sandbox the run (replace :165). `env -i PATH=$PATH HOME=$HOME LANG=C.UTF-8 TMPDIR=$TMPDIR unshare -rn timeout -k 5 60 bash -c <cmd>` in its own session, kill the process group on timeout, and refuse to run aggregate mode when `unshare -rn` is unavailable (fail closed). Verified: `poc/sandbox-compare.py` ran the same 64 lines plain and sandboxed; rc changed for 0 lines (40 rc=0, 24 gated in both). `unshare -rn` on this host shows only `lo` inside the netns. The `~/Projects/bounties` tests keep their meaning because HOME is kept.
3. Resolve instruments from the grader's lane, not the tree (T6). An allow-listed line `python3 corpus/instruments/anchorcheck.py ...` executed a tree-supplied `anchorcheck.py` (`poc/t6`: `verdict: allow`, `rc=0`, `tree instrument ran as allow-listed line`). Rewrite `corpus/instruments/X.py` to `<TOOL_ROOT>/corpus/instruments/X.py` (or pin sha). Not verified against the 64 lines; expected to be neutral because the lane copy is the same bytes.
4. Move the L3 `~/` / `/home/` and `--entry` shape checks before classify executes anything (currently :186-188 run after :160-168).
5. L6 (:204-236): call `check_row()` first, skip rows that fail, and assert `os.path.realpath(fp)` starts with `os.path.realpath(sc)` before writing. Drop absolute and `..` anchors. Writes must go through a copied file, not a symlink.
6. `entry_mode` (:125-127): reject any `--entry` whose realpath is outside `--root`.
7. C2 (:66-67): ignore `R46_PINS_OVERRIDE` unless a selftest flag is set and `TOOL_ROOT != root`; change the usage line to the lane path; optionally pin the census script's sha.
8. `freeze-controls.py:29`: use list-form `subprocess.run(["git","-C",lane,"archive",base,"corpus"], stdout=PIPE)` piped into `tar` by list; guard `--work` (refuse `$HOME`, `/`, or a path not under scratch) before `rmtree`.
9. Add controls to the freeze set that exercise S1, S2 and S3 (hostile line writes a marker; absolute anchor leaves an outside file unchanged; `sleep` child dies). Today's 9 controls cannot falsify them.

Breaking-change check: items 1, 2 keep all 64 current recheck return codes (verified). Item 3 is unverified. Items 4-6 affect only lines the corpus does not contain.

## Limitations

- Did not edit any counter, did not commit, and did not touch the fleet repo or shared files. The only lane-tree write I made was `py_compile` at 23:10 UTC, which created `corpus/instruments/__pycache__/r46-c1-gate.cpython-314.pyc` and `r46-c2-gate.cpython-314.pyc`; I deleted both (verified present then removed).
- Read the fleet census script only with grep and the `--file` section (lines 490-570), not in full.
- The sandbox parity was measured with `~/Projects/bounties` absent (the current host state). The on-restoration case, where those tests flip, was not exercised.
- The allow-list was tested only on the 64 current lines plus hand-written hostile samples. Item 3 is not tested at all.
- Probes ran only on this host (kernel 7.2.11-arch1-1, user namespaces enabled). No network traffic was generated; only the netns interface list was read.
- G2 symlinked `corpus/knowledge` directories and the census `validate` internals were code-read only, not exercised.
- Credential presence was recorded as set/unset; no value was read or written.
- Scratch was removed on exit.
