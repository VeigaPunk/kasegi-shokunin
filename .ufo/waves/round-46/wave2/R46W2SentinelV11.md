VERDICT: BROKEN

Scope: re-attack of the C1 v1.1 allow-list (`allowed()`, `grader_env()`, the instrument rewrite to the grader's own lane) in `corpus/instruments/r46-c1-gate.py`, plus the same questions for `r46-c2-gate.py` and `r46-landing-gate.py`. Lane tree examined at `0d121a201fe7cc3d0604ceb7666d1a85a5bbc174` (working tree, read-only). Every PoC used a fixture tree in scratch, a marker file in scratch, and a do-nothing control. No lane file was edited; no git mutation was run. A patched copy of the instruments lived only in scratch.

Summary: the v1.1 allow-list checks the SHAPE of a recheck line, not what the allowed instrument does with its arguments. Several allowed instruments read a path or command from the tree and execute it. The gate's docstring ("only allow-listed line shapes are executed ... a hostile or careless line turns L1 red instead of running") is false for those lines. Note that L1 still passes on the attack lines, so the attack is invisible to the aggregate.

---------------------------------------------------------------------------
F1 HIGH. C1 v1.1 allow-list runs tree-supplied code through allow-listed instruments.

Fixture: a tree whose only `recheck:` line is shape-legal, run through the aggregate gate as the grader does:
  `env TMPDIR=$S python3 <lane>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <empty-base>`

(a) `freeze-check.py --claims` runs `counter_cmd` from the tree's claims JSON via `bash -c` (freeze-check.py:72-74). Recheck line: `python3 corpus/instruments/freeze-check.py --claims poc-claims.json --tool-root . --base .`
Output (attack):
  `gate L1 pass=1 read=gated=1 broken=0 lines=1/base=0`
  `marker: TREE-CODE-RAN`
  `env names seen by tree code: HOME LANG LC_CTYPE PATH PWD R45_FREEZE_CHECK SHLVL TMPDIR _`
Output (control, recheck line `test -e poc-claims.json`):
  `gate L1 pass=1 read=gated=0 broken=0 lines=1/base=0`
  `marker: ABSENT`

(b) `kill-rule-check.py --instrument <tree path>` runs the tree file as Python (`sys.executable instrument_path ...`, kill-rule-check.py:473-476). Recheck line: `python3 corpus/instruments/kill-rule-check.py --root . --instrument corpus/evil.py` (evil.py appends to a marker in scratch).
Output: `marker: TREE-PYTHON-RAN argv=--selftest --scratch .../selftest/pristine HOME_set=True` followed by two more `TREE-PYTHON-RAN argv=--root .../fixtures/record-without-url` lines (three executions of tree code).

(c) `r46-landing-gate.py --jj-lane <tree path>` runs the tree script via `bash` (landing-gate:116). Recheck line: `python3 corpus/instruments/r46-landing-gate.py --pre-report --lane . --round 46 --jj-lane corpus/evil.sh`. The gate accepts any `r46-*.py` name, so this passes v1.1's allow-list.
Output: `gate L1 pass=1 read=gated=1 broken=0 lines=1/base=0`; `markerJ: FIRED`.

Allow-list evidence: `allowed()` returns True for `python3 corpus/instruments/freeze-check.py --claims poc.json --tool-root . --base .` and `python3 corpus/instruments/kill-rule-check.py --root . --instrument corpus/evil.py` (run via importlib on the lane module, output `allowed=1`). The landing-gate `--jj-lane` shape was not called through `allowed()`; it is proven allowed by the classify run in (c) (the gate ran it, `markerJ: FIRED`). `echo hi` -> 0 and `test -e x; touch y` -> 0 (controls).

Smallest fix (verified on a scratch copy, not applied): restrict the instrument NAME in `SEG_PY` to the five names the lane uses in recheck lines: `anchorcheck|source-recheck|claim-package-check|density|r46-c1-gate`. Result on the patched copy:
  PoC A: `gate L1 pass=0 read=gated=0 broken=1 lines=1/base=0`, `markerA: absent`
  PoC B: `gate L1 pass=0 read=gated=0 broken=1 lines=1/base=0`, `markerB: absent`
  PoC J: `gate L1 pass=0 read=gated=0 broken=1 lines=1/base=0`, `markerJ: absent`
  Same PoC A on the lane's v1.1 gate: `gate L1 pass=1 read=gated=1 broken=0`, `markerA: FIRED` (contrast).
Regression on the lane's own lines: `base recheck lines=65 allowed(orig)=65 allowed(patched)=65 changed=0` (regress.py over corpus/knowledge).
Also add: reject args starting with `/` or `~` or containing `..` (see F3). That part is proposed, not run.

---------------------------------------------------------------------------
F2 HIGH (planner trust boundary; precondition: write access to a lane's `.git/config`). Landing gate runs lane-config commands.

`r46-landing-gate.py` calls `git --no-optional-locks -C <lane> status` and `ls-remote origin` (landing-gate:77, 116-ish, READ_ONLY_GIT at :56). Both honour config that executes commands.

Positive control (git 2.56.0): `git -C <lane> config core.fsmonitor "touch <m>"`; `git -C <lane> status --porcelain` -> `FIRED`.
Landing gate on that lane: `python3 corpus/instruments/r46-landing-gate.py --pre-report --lane <lane> --round 46` -> `marker: FIRED`. Control lane with no fsmonitor -> `control (no fsmonitor): not-fired`.
`remote.origin.uploadpack "touch <m>"`: direct `git -C <lane> ls-remote origin` -> `positive (direct ls-remote with uploadpack): FIRED`; the landing gate on the same lane -> `F2 landing gate with uploadpack: FIRED`.

Fix candidates tested:
  `git -C <lane> -c core.fsmonitor=false status --porcelain` (rerun) -> `fix1 recheck: not-fired`
  `git -C <lane> ls-remote --upload-pack=git-upload-pack origin` -> `fix2 --upload-pack override: not-fired`
  `git -C <lane> -c remote.origin.uploadpack= ls-remote origin` -> `FIRED` (do NOT use an empty `-c` override)
Smallest fix: add `-c core.fsmonitor=false` to `git()` and `--upload-pack=git-upload-pack` to the `ls-remote` call. Not applied.
Note: F2 is also reachable from a tree recheck line under v1.1 (`--lane .`, see F1c), so it is not only a seat-to-planner path.

---------------------------------------------------------------------------
F3 LOW. Host-environment oracles through allow-listed shapes (`~` expansion, absolute paths).

(a) `test` segments: `~` is in the SEG_TEST class and bash expands it; HOME is kept in grader_env (grader_env docstring says the lines test ~/Projects).
  Fixture A: `test -e ~/.bashrc` -> `gate L1 pass=1 read=gated=0 broken=0 lines=1/base=0` (executes)
  Fixture B: `test -e ~/no-such-file-r46-probe` -> `gate L1 pass=1 read=gated=1 broken=0 lines=1/base=0` (gated)
  The grader's class flips on host file existence. One bit per line, visible in the L1 count.
(b) absolute paths in args: `python3 corpus/instruments/r46-c1-gate.py --entry ~/.bashrc --root <S>` -> `reground entry=.bashrc rows=0 ok=0 exit=1 read=section-count=0`; `--entry /nonexistent/r46-probe` -> `read=entry-absent`. Entry mode reads host files outside the tree and prints a section count.
  `source-recheck.py --manifest ~/.bashrc --source S073` -> `manifest UNAVAILABLE reason=unreadable-or-invalid` (rc=2). `--manifest <nonexistent scratch>` -> `reason=missing`. Absolute manifests are read.
(c) `| grep -x '<literal>'`: the literal may begin with `-`, so grep reads it as an option. This host's grep is `pi-uu-grep 0.2.0`.
  `printf 'TREE-PATTERN\n' | grep -x "-f<patfile>"` -> prints `TREE-PATTERN`, `rc=0` (the file was read as patterns).
  Control `printf 'other\n' | grep -x "-f<patfile>"` -> `rc=1`. Control `grep -x -- "-fnot-a-file"` matches the literal as text.
  Patched SEG_PY (`(?!-)` guard on the grep literal): `orig=1 patched=0` for `... | grep -x '-f/etc/hostname'`; `orig=1 patched=1` for `... | grep -x 'literal'`.
Smallest fix: reject args beginning with `/` or `~`, or containing `..`; drop `~` from the SEG_TEST / SEG_PY classes; `(?!-)` on the grep literal (verified as a regex rule; the path rule is proposed, not run).

---------------------------------------------------------------------------
F4 INFO. grader_env docstring: "no tokens, agent sockets or other host secrets reach a tree-supplied line". Env vars are scrubbed (F1a output shows only HOME LANG LC_CTYPE PATH PWD R45_FREEZE_CHECK SHLVL TMPDIR _). HOME is kept and is the same account, so any tree-supplied code (F1) can read files under HOME. The docstring is accurate only for environment variables. PATH has no empty or relative entries on this host (checked), so no PATH shadowing of grep/python3/git.

---------------------------------------------------------------------------
NEGATIVES (checked; not exploitable as stated)

N1 `git -C <tree> rev-parse HEAD` with tree config `core.fsmonitor`: `marker: not-fired` (positive control: `git status` fires). rev-parse does not refresh the index, so fsmonitor does not run. `include.path`: no command-exec key; my probe (a bogus config line) was accepted with rc=0, so it is inconclusive as a read oracle and not exercised further.
N2 textconv via `git show`: `git show HEAD:a.txt` with `diff.evil.textconv` set -> `not-fired`; `git show --textconv` -> `FIRED`; `git log -p` -> `FIRED`. anchorcheck.py:196 calls plain `git -C <repo> show <obj>:<path>` (no `--textconv`), so this is closed today. If anchorcheck ever adds `--textconv`, it becomes exploitable from the tree's `.git/config`.
N3 source-recheck.py: its only `subprocess.run` is at line 304 inside `--selftest`. Normal mode reads local files. Safe to keep on the allow-list.
N4 C2 gate (`r46-c2-gate.py`): planted tree with `corpus/knowledge/poc.md` containing `recheck: touch <m>` and a planted `corpus/instruments/source-recheck.py` writing a marker. Run `python3 <lane>/corpus/instruments/r46-c2-gate.py --root <tree>` -> `c2-gate fixed=0/7 exit=1`; `markerK-knowledge: absent`, `markerK-srcrecheck: absent`. C2 runs its pinned TOOL_ROOT source-recheck (G4) and constant CENSUS (G7); it does not execute tree text.
N5 anchorcheck's `subprocess.run` sites (anchorcheck.py:336, 344) are inside its selftest block (`selftest FAIL` messages).

---------------------------------------------------------------------------
NOT RUN (code read only; reachable under v1.1; the name-allow-list fix blocks them):
- frontier-recheck-count.py:269 `subprocess.run(["bash", "-c", recheck], cwd=root)` with no env scrub, on the tree's own `recheck:` line, when `--root .` is passed. Needs a full F-row fixture; not built.
- limb-mutation-check.py:19-20, 294: `kill` shell string from the tree's ledger run via `bash -c`. Not built.
- r45-counters-selftest-c1.py:95 `shlex.split(cmd)` and r45-routed-defects.py:149 `run(cmd)`: origin of `cmd` not traced.
- Aggregate self-recursion: a line `python3 corpus/instruments/r46-c1-gate.py --root . --baseline .` re-enters classify(root) per level, each with a 180 s timeout (r46-c1-gate.py:207). Not run (resource-exhaustion risk). Low severity (availability).

---------------------------------------------------------------------------
Limitations
- All exploit runs used the lane's v1.1 gate at its current bytes and this host's git 2.56.0 and pi-uu-grep 0.2.0. The HOME-dependent oracles (F3a) depend on host files; `~/.bashrc` existed here.
- The name-allow-list fix was verified on a scratch copy only; the `/`, `~`, `..` argument rule is proposed, not run.
- I did not test the v1 gate bytes; I did not run the full 65-line aggregate on the real base (regression used allowed() over the lane's recheck lines only).
- No network, no remote; ls-remote tests used a local bare repo.
- Scratch under $HYAKU_SCRATCH/kasegi-r46/R46W2SentinelV11, removed at exit.
