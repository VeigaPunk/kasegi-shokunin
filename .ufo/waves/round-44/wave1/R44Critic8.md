# R44Critic8 — falsification attempt: exit-code correction (C1 / spot-check §6 item 8)

- seat: `R44Critic8` (critic, leaf, read-only); item: *"Try to falsify exit-code correction by replaying exact absent-script vs control command semantics."*
- lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; frozen round-44 base `66314015122b9aa32dc40f2f1815df56624c26d1` (claims/controls frozen at `6631401`, wave-1 dispatch open).
- bases replayed: round-43 base `ab98fac9dce87130bc4f66de89e30650d63943dc` (the base the before-cell names) and round-44 base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`.
- method: `git archive <ref> | tar -x` into scratch (read-only on the lane object store), then literal command replays with `echo exit=$?`. No lane byte, index, git/jj state or shared file was written; scratch removed (§9).
- writes: this receipt only.

## 0. Verdict

**The exit-code correction survives every falsification attempt I could build; it is not falsified.** Three precision defects remain in the in-flight wording/receipt (none fatal, none changing the verdict), and one operational trap can make a *correct* correction look false if the replay is run at the wrong base. Details in §4–§6.

The frozen defect itself is **real and reproduced**: spot-check `corpus/lessons/round-43-verifier-spotcheck.md:108` states the before-cell cites `c1-controls/do-nothing.txt` for `127` while that control's only measured token is `exit=2`; both halves reproduce from committed bytes (§2).

## 1. The claim under attack, at its exact committed locations

| surface | committed location | literal |
|---|---|---|
| routed defect 8 | `corpus/lessons/round-43-verifier-spotcheck.md:108` (committed `5ab3a60a`) | "…say the base suite run exits `127`, citing `c1-controls/do-nothing.txt`, which prints `exit=2` for its `ls` (§A). 127 is the shell's not-found code for running the missing script, not a value the cited control prints…" |
| claims before-cell | `.ufo/waves/round-43/claims.json:38` (committed `ab98fac9`…`dbd2e106`) | "see .ufo/waves/round-43/c1-controls/do-nothing.txt (measured-at line present): the r43 suite is absent at base (exit 127); …" |
| report C1 before cell | fleet repo commit `fdf719a9`, `.ufo/reports/round-43/kasegi.md:56` | "\| C1 \| depth:verifiability \| suite absent (run exit 127); the r42 stand-in over the base export prints `closed=12/13 exit=1` … (`c1-controls/do-nothing.txt`) \|" |
| cited control, §A | `.ufo/waves/round-43/c1-controls/do-nothing.txt:3-5` (committed) | `--- A. r43 suite absent at base` / `ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory` / `exit=2` |
| control's only other `127` byte | same file `:41` | "see .ufo/waves/round-42/c1-controls/do-nothing.txt — …: r42 suite absent (exit 127, cannot print closed=13/13)…" — **quoted round-42 before-cell prose, not a measured exit** |
| in-flight correction (untracked) | `.ufo/waves/round-43/claims-erratum-6.md` (sha256 `bcfa0f18…`, `??`) | "the before-cell's missing-suite `exit 127` is a direct `bash corpus/instruments/r43-closure.sh` attempt on the exported base, not a value printed by `c1-controls/do-nothing.txt`; that control's `exit=2` belongs to its failed `ls` in §A." |
| in-flight receipt (untracked) | `.ufo/waves/round-44/controls/missing-suite-base.txt` (sha256 `6a602e35…`, `??`) | `base=ab98fac9…` / `command: cd <git archive base> && bash corpus/instruments/r43-closure.sh` / `exit=127` |

Note on location: the round-43 report is **not** in the lane repo (`git cat-file -t fdf719a9` in the lane → `fatal: Not a valid object name`); it lives in the fleet repo, which is where the spot-check's pointer resolves. The lane tree has no `.ufo/reports/round-43/`.

## 2. Replay: exact absent-script vs control semantics

Export used: `git archive ab98fac9 | tar -x -C $S/base-ab98fac9` (suite confirmed absent: `ls … | grep -c r43-closure` → `0`).

Verbatim, at `ab98fac9`:

```
$ ls corpus/instruments/r43-closure.sh
ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
exit=2

$ bash corpus/instruments/r43-closure.sh
bash: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

$ bash corpus/instruments/r43-closure.sh --export-ref ab98fac9… --work … --scratch-root …
bash: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

$ bash -c './corpus/instruments/r43-closure.sh'
bash: line 1: ./corpus/instruments/r43-closure.sh: No such file or directory
exit=127

$ sh corpus/instruments/r43-closure.sh
sh: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

$ bash -c 'source corpus/instruments/r43-closure.sh'
bash: line 1: corpus/instruments/r43-closure.sh: No such file or directory
exit=1

$ command -v corpus/instruments/r43-closure.sh
exit=1

$ git -C <lane> cat-file -e ab98fac9:corpus/instruments/r43-closure.sh
fatal: path 'corpus/instruments/r43-closure.sh' exists on disk, but not in 'ab98fac9'
exit=128
```

`/bin/sh` resolves to `/usr/bin/bash` on this host (`readlink -f $(command -v sh)` → `/usr/bin/bash`), so the `sh` row is bash semantics, not dash; dash is not installed (`command -v dash` → not found). That bounds the "interpreter-dependent" hypothesis to bash only — see §8.

At the round-44 base (`5ab3a60a` export), the same command string does **not** mean absence:

```
$ ls -l corpus/instruments/r43-closure.sh   → 21046 bytes; sha256 a832908e15f49de89066d8168a833d3ffa0f5fad432ba1c2b5a813ba45bef168
$ bash corpus/instruments/r43-closure.sh
r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>
exit=2
```

So `exit=2` has at least three distinct producers at the two bases, and `127` has exactly one:

| producer | code | evidence |
|---|---|---|
| `ls` on a missing path | 2 | control §A (`:4-5`), replayed |
| plain run of a **present** suite (r43) | 2 | `5ab3a60a` export, replayed |
| plain run of a **present** suite (r42) | 2 | `ab98fac9` export: `r42-closure: a plain run is refused…`, `exit=2` |
| bash usage error | 2 | `bash -c 'exit 2'` → `exit=2` (trivial control) |
| executing an **absent** path via `bash <path>` | 127 | `ab98fac9` export, replayed twice (with and without the documented args) |
| `source` of an absent path | 1 | replayed |
| `command -v` on an absent path | 1 | replayed |
| `git cat-file -e <ref>:<absent path>` | 128 | replayed |

## 3. Exit-code semantics bounded (what 127 does and does not prove)

In real bash 5.2.37 (`bash -c` form, so no wrapper mediation):

```
$ bash -c './absent.sh'      → bash: line 1: ./absent.sh: No such file or directory      exit=127
$ bash -c './noexec.sh'      → bash: line 1: ./noexec.sh: Permission denied              exit=126
$ bash -c './adir'           → bash: line 1: ./adir: Is a directory                      exit=126
$ bash -c './badinterp.sh'   → bash: ./badinterp.sh: /nonexistent/interp: bad interpreter: No such file or directory   exit=126
$ bash noexec.sh             → hi                                                        exit=0   (bash ignores the mode bit)
```

So within bash, `127` discriminates *not-found* from *found-but-unexecutable* (`126`). It is **not** a proof of absence by itself — a missing shebang interpreter also yields a "No such file or directory" message; bash 5.2 assigns it `126`, but this host's tool-wrapper shell assigned the same case `127` (`./badinterp.sh` → `error: command not found`, `exit=127`). Consequence: the only authoritative form is `bash <path>` executed by bash, not `./<path>` through a wrapper, and the code must be read together with the message naming the path.

## 4. Falsification attempts and results

| # | attempt | expected if correction false | observed | result |
|---|---|---|---|---|
| FA-1 | Replay the erratum's literal command at the named base: export `ab98fac9`, `bash corpus/instruments/r43-closure.sh` | exit ≠ 127 | `bash: … No such file or directory`, `exit=127` | **correction survives** |
| FA-2 | Argued the control *does* print 127 (`grep -c '127' control` → `1`) | correction's "not a value printed by" is false | the single occurrence is `:41`, inside the RD42-8 quotation of round-42's before-cell; §A's measured token is `exit=2` at `:5` | **survives, with a wording gap** (F-1 below) |
| FA-3 | Attribute the 127 to the control by re-running only what the control ran (`ls`) | 127 would appear | `exit=2` | **survives** — the defect is real, the correction's attribution fix is the right one |
| FA-4 | Replay the same command string in the lane worktree at the r44 frozen base (present suite) | 127 | `exit=2` (refusal) | **survives only because the receipt carries `base=ab98fac9…`**; this is the trap (F-3) |
| FA-5 | Test whether 127 is a generic "unexecutable" code (would make the claim ambiguous) | absent and unexecutable both 127 | bash separates them: 127 vs 126 | **survives under `bash <path>`** |
| FA-6 | Try to find a sound origin for the carried token in the r42 control (would make the new receipt unnecessary, not false) | r42 control's 127 unbacked | `git archive 5053a7f4 corpus/instruments`, then `bash corpus/instruments/r42-closure.sh` → `bash: … No such file or directory`, `exit=127`, matching the control's `:5-7` line for line | **correction survives; a cheaper citation exists** (F-2) |
| FA-7 | Bind the control's B section to committed bytes (the correction leans on it) | digest mismatch | `sha256sum` of `ab98fac9` export `corpus/instruments/r42-closure.sh` = `fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b` = the control's `suite-sha256=` line | **survives** |

No attempt produced a state in which the correction's factual content is false.

## 5. Degenerate acceptance a counter must not permit (mutant target)

The assigned conflater ("control-command exit=2 with script exit=127") is reachable by two cheap predicates; both must be excluded from `corpus/instruments/r44-routed-defects.py` (absent at this revision — `ls corpus/instruments/r44-routed-defects.py` → absent):

1. **Grep-the-control.** `grep -c '127' .ufo/waves/round-43/c1-controls/do-nothing.txt` → `1`, satisfied by quoted prose at `:41`. A check of the form "the cited control contains 127" accepts a *false* correction (and would have accepted the original defective before-cell). Measured.
2. **Bare integer comparison.** Accepting "the base run exits 127" by comparing against any recorded `2` (or vice versa) cannot distinguish the three `2`-producers in §2 from the one `127`-producer. Measured.

The discriminating predicate that survives all of the above:

- replay **at the base the before-cell names** (`ab98fac9`, an export that provably lacks the suite — `git cat-file -e ab98fac9:corpus/instruments/r43-closure.sh` → rc `128`);
- invoke `bash <path>` (not `./<path>`), capture **code and message**, require code `127` *and* the message naming that path;
- separately replay the control's own operation (`ls <path>`) and require code `2` there;
- require the erratum to state both codes with their commands, and require the control's `:5` token to be `exit=2`.

## 6. Defects found in the in-flight correction (precision only; verdict unchanged)

- **F-1 (minor, wording).** Erratum-6 says the 127 is "not a value printed by `c1-controls/do-nothing.txt`". Measured sense: correct (§A prints `exit=2`). Literal sense: the file *does* contain `127` at `:41`. Smallest safe fix: "not a **measured exit** in that control; its only `127` occurrence (`:41`) is the quoted round-42 before-cell, and §A's measured token is `exit=2`."
- **F-2 (minor, provenance economy).** The receipt invents a new measurement where the r42 control already supplies one: `bash corpus/instruments/r42-closure.sh` at `5053a7f4` → `exit=127`, reproduced (FA-6). Either citation is sound; citing the committed r42 control would remove an untracked dependency.
- **F-3 (operational, must be fixed in the counter).** `missing-suite-base.txt:2` writes `command: cd <git archive base> && bash corpus/instruments/r43-closure.sh` — a placeholder, not a literal command. The literal replay requires `git -C <lane> archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x -C <dir>`. Without that, the command is not reproducible and FA-4's trap (worktree replay → `2`) is one keystroke away.
- **F-4 (integration risk, not yet a defect).** Erratum-6 (`??`) and its receipt (`??`) are both untracked. If the erratum lands without `missing-suite-base.txt` in the same commit, its pointer dangles. Neither is committed evidence at this revision; I grade the *content*, not a commit.

## 7. Do-nothing discrimination

Do-nothing cannot satisfy the corrected predicate: at `ab98fac9` the absent-path replay is `127` **because the suite is absent**, and the control's token is `2` **because it ran `ls`**; neither fact is produced by an unchanged replay, and the frozen before-cell's *attribution* (the thing defect 8 grades) is wrong in committed bytes and is only changed by an appended erratum. The round-44 control (`.ufo/waves/round-44/controls/do-nothing.txt:2`) names base `5ab3a60a`, where the same command yields `2` — so a do-nothing replay at the round-44 base cannot even reproduce the `127` the before-cell claims.

## 8. Limitations

- `/bin/sh` is bash on this host and dash is absent, so the "other shell prints a different code for an absent script" branch is **untested**, not refuted. If any lane instrument invokes the suite as `sh <path>` on a dash host, the code could differ; no committed command in round 43/44 does (`counting_commands` all use `bash`).
- All `127`/`126` claims are bash 5.2.37 measurements on this host; a different bash minor is not replayed.
- The report C1 cell was read from fleet commit `fdf719a9` (read-only `git show`); the lane holds no copy, so I could not re-derive it from lane bytes.
- I did not run the round-43 suite, any limb, or the (absent) r44 counter; I replayed only the two exit-code operations this item names.
- The in-flight erratum/receipt were read at sha256 `bcfa0f18…` / `6a602e35…`; a later rewrite by their author is not covered.

## 9. Scratch, installs, mutations

- scratch: `HYAKU_SCRATCH` was **unset** in this shell; used `/fast/scratch/hyaku/kasegi-r44/R44Critic8/` (exports `base-ab98fac9`, `base-5ab3a60a`, sparse `sparse-5053a7f4`, `sem/`, `replay-absent.log`), removed on exit — see the removal check in the seat result.
- installs: none. No pacman, no package manager, no PATH write.
- mutations: none. `git archive`/`cat-file`/`ls-tree`/`show` only; no `git`/`jj` write, no commit, no index touch; no lane or fleet file written except this receipt.
