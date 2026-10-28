# R44Exec2 — C1 / round-43 routed defect 8: missing-script exit 127 vs cited `ls` exit 2

- seat: **R44Exec2** (leaf executor, kasegi round 44, wave 1). No delegation, no background work.
- assigned item: *"In isolated scratch, probe actual missing script exit code versus cited ls exit code; provide exact outputs."* (dispatch `wave1-dispatch.json:107`, `wave1/swarm-registry.json:89`).
- lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; HEAD at probe time `66314015122b9aa32dc40f2f1815df56624c26d1`; round-44 frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (`.ufo/waves/round-44/controls/do-nothing.txt:2`); round-43 base `ab98fac9dce87130bc4f66de89e30650d63943dc` (`.ufo/waves/round-43/c1-controls/do-nothing.txt:1`).
- writes: this report only. No production/shared file, no git/jj/index mutation, no commit/push.
- scratch: `$HYAKU_SCRATCH` unset → lane default `/fast/scratch/hyaku` → `/fast/scratch/hyaku/kasegi-r44/R44Exec2/` (two `git archive` extractions, 308 MB), removed on exit (see §9).

## 1. The two literals under test

| literal | where committed | exact text | token |
|---|---|---|---|
| claims' `before` token | `.ufo/waves/round-43/claims.json:38` (blob `b611facb53e9…` at HEAD; sha256 `a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`) | `the r43 suite is absent at base (exit 127)` … `see .ufo/waves/round-43/c1-controls/do-nothing.txt` | **127** |
| cited control's observed token | `.ufo/waves/round-43/c1-controls/do-nothing.txt:3-5` (sha256 `221d20331e7d673f3ce3a3778ede2dccb0094620cd51867da0c609f6e2f7a08e`, 3202 B) | `--- A. r43 suite absent at base` / `ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory` / `exit=2` | **2** |
| routed defect | `corpus/lessons/round-43-verifier-spotcheck.md:108` | "`claims.json` C1 `before` and the report's C1 cell say the base suite run exits `127`, citing `c1-controls/do-nothing.txt`, which prints `exit=2` for its `ls` (§A). 127 is the shell's not-found code for running the missing script, not a value the cited control prints; either measure it (run the absent path) or cite the control's own token." | — |

The control's only other occurrence of the numeral is `do-nothing.txt:41`, inside the quoted RD42-8 fragment (`r42 suite absent (exit 127, cannot print closed=13/13)`), which points at `.ufo/waves/round-42/c1-controls/do-nothing.txt:7` — that control *does* carry an observed `(observed suite exit = 127; …)`. So the numeral 127 is real in the lane's history; it is not the token the **cited** control prints for the **r43** suite.

## 2. Environment (why two shells were used)

```
probe-host: Linux 7.2.11-arch1-1 x86_64
probe-utc: 2026-10-28T18:56:58Z
bash-version: GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
sh-target: /usr/bin/bash
```

The harness shell resolves `ls` as a **builtin** (`type ls` → `ls is a shell builtin`; `ls --version` → `ls 0.8.0`) and direct execution of a missing path prints its own message (`error: command not found: …`). To keep the probe independent of harness wrapping, every load-bearing row below was re-run under `env -i /usr/bin/bash --noprofile --norc` with `/usr/bin/ls`. Both shells agree on the exit codes.

## 3. Exact probes at round-43 base `ab98fac9` (suite genuinely absent)

`git ls-tree ab98fac9 corpus/instruments/r43-closure.sh` → **no output** (path absent; introduced later at `ffe197d1378a825705215a36b8e6ee5dfbe4a549`).

Clean-env transcript (`env -i /usr/bin/bash --noprofile --norc -c "cd <base>; <cmd>"`), scratch tree = `git archive ab98fac9 | tar -x`:

```
cmd: bash corpus/instruments/r43-closure.sh
out: bash: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

cmd: sh corpus/instruments/r43-closure.sh
out: sh: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

cmd: ./corpus/instruments/r43-closure.sh
out: /usr/bin/bash: line 1: ./corpus/instruments/r43-closure.sh: No such file or directory
exit=127

cmd: /usr/bin/ls corpus/instruments/r43-closure.sh
out: ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
exit=2

cmd: python3 corpus/instruments/r43-closure.sh
out: python3: can't open file '/fast/scratch/hyaku/kasegi-r44/R44Exec2/base/corpus/instruments/r43-closure.sh': [Errno 2] No such file or directory
exit=2
```

Harness-shell transcript (same base tree), including the non-shell probes and the existing-suite analogue:

```
### P1 ls <missing r43 suite>
cmd: ls corpus/instruments/r43-closure.sh
stdout+stderr: ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
exit=2

### P2 bash <missing r43 suite>
cmd: bash corpus/instruments/r43-closure.sh
stdout+stderr: bash: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

### P3 sh <missing r43 suite>
cmd: sh corpus/instruments/r43-closure.sh
stdout+stderr: sh: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

### P4 direct exec ./<missing r43 suite>
cmd: ./corpus/instruments/r43-closure.sh
stdout+stderr: error: command not found: ./corpus/instruments/r43-closure.sh
exit=127

### P5 python3 <missing r43 suite>
cmd: python3 corpus/instruments/r43-closure.sh
stdout+stderr: python3: can't open file '…/r43-closure.sh': [Errno 2] No such file or directory
exit=2

### P6 bash -c '<missing r43 suite>'
cmd: bash -c corpus/instruments/r43-closure.sh
stdout+stderr: bash: line 1: corpus/instruments/r43-closure.sh: No such file or directory
exit=127

### P7 test -f <missing r43 suite>
cmd: test -f corpus/instruments/r43-closure.sh
stdout+stderr: 
exit=1

### P8 bash <missing nonexistent path>
cmd: bash corpus/instruments/definitely-not-here.sh
stdout+stderr: bash: corpus/instruments/definitely-not-here.sh: No such file or directory
exit=127

### P9 bash <existing r42 suite, plain run>
cmd: bash corpus/instruments/r42-closure.sh
stdout+stderr: r42-closure: a plain run is refused (export mode only)
r42-closure: usage: r42-closure.sh --export-ref <hash> [options]
exit=2

### P10 ls <existing r42 suite>
cmd: ls corpus/instruments/r42-closure.sh
stdout+stderr: corpus/instruments/r42-closure.sh
exit=0
```

Control §A reproduction, byte comparison: `/usr/bin/ls corpus/instruments/r43-closure.sh` at `ab98fac9` prints exactly `ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory` with `exit=2` — identical to `do-nothing.txt:4-5`. The harness builtin `ls 0.8.0` prints the same message and the same `2`, so the control's token is not an artifact of either implementation.

## 4. Exact probes at round-44 frozen base `5ab3a60a` (suite present)

```
cmd: /usr/bin/ls corpus/instruments/r43-closure.sh
out: corpus/instruments/r43-closure.sh
exit=0

cmd: bash corpus/instruments/r43-closure.sh
out: r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>
exit=2
```

Identical results at the lane working tree HEAD `6631401`. `git ls-tree 5ab3a60a corpus/instruments/r43-closure.sh` → `100755 blob 97038e41f7e7cba154c1227e97d6b3bf9d8ebbcb`.

## 5. Findings

**F1 — the cited control's token is `2`, and it reproduces byte-identically.** `do-nothing.txt:4-5` (`ls: cannot access … / exit=2`) is a *filesystem* probe. Reproduced at `ab98fac9` under both `/usr/bin/ls` and the harness builtin. The claims' `before` cites this file for a `127`.

**F2 — `127` is the correct *shell* code, and it is measurable at the round-43 base.** `bash corpus/instruments/r43-closure.sh` → `bash: … No such file or directory`, `exit=127`; same for `sh` (127) and direct `./` execution (127, harness message `error: command not found:`). Defect 8's first remediation branch ("measure it (run the absent path)") is therefore satisfiable with a one-line command; the numeral need not be withdrawn, only re-cited. Precedent in-lane: `corpus/lessons/round-41-verifier-spotcheck.md:54-55` quotes exactly this measurement (`bash: corpus/instruments/r41-closure.sh: No such file or directory`, exit 127) — round 43 dropped the run and cited the `ls` probe in its place.

**F3 — the token is interpreter-dependent, so the correction must name the command.** `python3 <absent path>` exits **2** (`can't open file … [Errno 2]`), not 127; `test -f` exits **1**; `ls` exits **2**; only a shell invocation of the absent path yields 127. A correction that says "the absent script exits 127" without naming `bash <path>` is falsifiable by the `python3` probe — relevant because C1's counter is itself a `python3 corpus/instruments/r44-routed-defects.py` invocation.

**F4 — `127` is not reproducible at the round-44 base.** At `5ab3a60a` the suite exists: `ls` → 0, plain run → `r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>`, exit 2. A do-nothing replay at the round-44 base therefore *cannot* print the claims' 127 token; the correction must pin `ab98fac9` explicitly or the fix becomes unverifiable at the base the round-44 control names. (Sibling `wave1/R44Review8.md:14,20,23` observed the same at the round-44 base and used a generic `/no/such/script` for 127; the direct absent-suite measurement at `ab98fac9` above is the evidence that seat said the correction should state.)

**F5 — the numeral's provenance.** The only `127` inside the r43 control is `do-nothing.txt:41`, a quotation of the round-42 RD42-8 line; `.ufo/waves/round-42/c1-controls/do-nothing.txt:7` carries the observed `(observed suite exit = 127; …)`. So the claims' numeral descends from the round-42 control, not from the r43 control it cites — which is exactly defect 8's mismatch, and it also means the fix is a *citation* repair plus an added measurement, not a retraction of a false number.

**F6 — defect 8 is unresolved at HEAD `6631401`.** `corpus/instruments/r44-routed-defects.py` absent (`ls` → `No such file or directory`); round-44 `claims.json` C1 `before` does not restate the token; `git grep -nE "exit 127|exit=127" HEAD -- .ufo/waves/round-44` matches only dispatch/registry/spec text and the untracked `wave1/R44Review8.md` draft — no appended `Correction (round 44)` anywhere in the tracked tree. C1's `after` (0 of 8 unresolved, one committed read-only counter) is not reachable at this revision.

## 6. Exact correction text this probe supports (draft for the one L1; not written anywhere else)

> **Correction (round 44, RD43-8).** `.ufo/waves/round-43/claims.json:38` states "the r43 suite is absent at base (exit 127)" citing `.ufo/waves/round-43/c1-controls/do-nothing.txt`, whose observed token is `exit=2` (`do-nothing.txt:5`, an `ls` probe). Both numerals are true of different commands at base `ab98fac9`: `ls corpus/instruments/r43-closure.sh` → `ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory`, exit 2 (the control's token); `bash corpus/instruments/r43-closure.sh` → `bash: corpus/instruments/r43-closure.sh: No such file or directory`, exit 127 (the claims' token, now measured at `ab98fac9`). The superseded literal is the citation, not the number: `exit 127` stands with the shell command that produces it, `exit=2` is the `ls` probe, and `python3 <path>` on the same absent file exits 2 — the token is interpreter-dependent. At the round-44 base `5ab3a60a` the suite is present (`ls` → 0; plain run → `r43-closure: a plain run is refused (export mode only); pass --export-ref <hash>`, exit 2), so `127` is reproducible only at `ab98fac9`.

Measurement command for the counter/erratum, verbatim:

```
git archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x -C "$S/base"
(cd "$S/base" && bash corpus/instruments/r43-closure.sh; echo exit=$?)
# bash: corpus/instruments/r43-closure.sh: No such file or directory
# exit=127
(cd "$S/base" && ls corpus/instruments/r43-closure.sh; echo exit=$?)
# ls: cannot access 'corpus/instruments/r43-closure.sh': No such file or directory
# exit=2
```

## 7. Do-nothing discrimination

| candidate do-nothing replay | can it print `127`? | can it print the control's `2`? | measured |
|---|---|---|---|
| replay at round-44 base `5ab3a60a` | no — suite present, plain run exits 2 with a refusal message | no — `ls` exits 0 | §4 |
| replay at round-43 base `ab98fac9`, `ls` only | no — `ls` prints 2 | yes (but says nothing about a run) | §3 |
| replay at `ab98fac9`, `bash <path>` | yes — 127 | no | §3 |
| do-nothing against the 8-defect list | cannot reach 0 unresolved: no r44 counter and no correction exist | — | F6 |

Neither code carries evidence that the suite *ran*: `2` is a filesystem miss and `127` is a shell not-found, so no do-nothing replay can convert either into `closed=NN`. The control's own §B stand-in (r42 suite over the base export, `closed=12/13 exit=1`) remains the only do-nothing run figure.

## 8. Limitations

1. The **report's** C1 cell half of defect 8 is not verifiable from this checkout: `.ufo/reports/round-43/kasegi.md` is absent from every ref (`git log --all -- .ufo/reports/round-43/kasegi.md` → empty; `git ls-tree -r HEAD | grep -c reports/round-43` → 0) and the report commit named by the spot-check, `fdf719a92d8d305d5465f8087c5af90a8900a172`, is not an object here (`git cat-file -t` → `could not get object info`). Only the claims.json half is checkable in this clone; the report half rests on the non-author spot-check's own reading in its clone.
2. `fdf719a9`'s absence also means I cannot confirm whether the report cites the control or only the numeral — the spot-check says both, and I did not re-derive it.
3. Exit codes were measured on this host's `bash 5.3.20` and `ls 0.8.0` builtin plus `/usr/bin/ls`; POSIX fixes 127 for "command not found", so the shell rows are portable, but the exact stderr wording is host-specific and is quoted verbatim rather than generalised.
4. No gate was executed: I ran no lane instrument, and C1's counter does not exist, so I make no claim about the other seven routed defects.

## 9. Scratch, tooling, cleanup

- scratch root `/fast/scratch/hyaku/kasegi-r44/R44Exec2/` (`$HYAKU_SCRATCH` unset → lane default `/fast/scratch/hyaku`); contents: `base/` (`git archive ab98fac9`), `base-r44/` (`git archive 5ab3a60a`), `probe-base.transcript.txt` (59 lines, sha256 `6b6e717f85da10165b97fd975e9faf822acfd437829d321ed1d06336e06702bd`), `probe-cleanenv.transcript.txt` (30 lines, sha256 `9c9af0d92aa60195a24fa7fa34e213b5b1a19f9606e01f6bef0d90a672120f93`), `probe-r44base.transcript.txt` (9 lines, sha256 `7218860b5736b540b4bb9bcd43b9fca23e1a0a3315ea43a33997758a882f0ee0`); 308 MB total, `rm -rf` on exit, verified absent afterwards (see footer).
- no tool installed or updated; no `pacman` invocation; nothing written to any PATH directory; no git/jj command that mutates state (only `rev-parse`, `archive`, `ls-tree`, `log`, `cat-file`, `show`, `grep`).
- no production or shared file touched; this report is the only write.
- cleanup verified: `rm -rf /fast/scratch/hyaku/kasegi-r44/R44Exec2` → `rm-rc=0`; `ls -d <that path>` → `No such file or directory` (rc 2). No scratch failure to report.
