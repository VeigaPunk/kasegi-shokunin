VERDICT: BROKEN

Seat R45RevLimbR5 · C1 limb attack on `corpus/instruments/r45-routed-defects.py` `def limb_r5` (lines 225-242, counter sha256 `82004c70…f04ee`, identical at freeze 8cf62c8, HEAD 5242db6 and the working copy). Defect stood for: spot-check §6 item 5, "Receipt wording: re-file the selftest invocation without the failed bare call" (`corpus/lessons/round-44-verifier-spotcheck.md:83`).

## What the limb grades (read, not inferred)

`limb_r5` reads only the bytes of `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` in `--root` and returns fixed=1 when all of these hold:
- no line matches `^(usage:|.*error:)` (re.M | re.I), i.e. the substring `error:` anywhere on a line is refused;
- a line `^selftest cases=20 failures=0\s*$` exists;
- a line `(^|\s)exit=0\s*$` exists;
- `--root \S+ --selftest --work \S+` appears somewhere;
- `final-attempt3.txt` in root is byte-identical to the base copy.

Nothing in the limb runs the selftest, checks a run's provenance, or binds the text to the tree. The predicate is lexical and presence-only. That is the class the lesson itself says no criterion caught (§6 item 2: "presence-only predicates accept denials and fabricated trees").

## Finding 1 — cheapest construction: hand-typed three-line receipt (fixed=1, defect present)

Recipe (base export `dc5bb8c` + one new file; no run performed):
```
printf '%s\n' '$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>' 'selftest cases=20 failures=0' 'exit=0' > .ufo/waves/round-44/controls/final-attempt3-refiled.txt
```
File is 128 bytes (`bytes=128`). Minimal tree = only `final-attempt3.txt` (copied from base) and that file (2 files total). Frozen counter, run as `python3 counter/r45-routed-defects.py --root $M --baseline $BASE`:
```
limb R5 fixed=1 read=refiled=ok original=unchanged
routed-defects total=5 fixed=1 unresolved=4 exit=1
```
The defect condition is still present: the same base tree, when its real selftest is run (`python3 corpus/instruments/r44-routed-defects.py --root $BASE --selftest --work $W`), prints
```
selftest cases=20 failures=1
exit=1
```
So the receipt asserts `failures=0` for a tree whose real selftest prints `failures=1`. The limb accepts it.

## Finding 2 — edited real failure passes (fixed=1)

Start from the real selftest output at the closure tip (`tip-5e4d6bf`, which prints `selftest cases=20 failures=1` / `exit=1`), prepend the invocation line, and rewrite the two tokens to `failures=0` / `exit=0`. Diff against the real output:
```
21,22c21,22
< selftest cases=20 failures=1
< exit=1
---
> selftest cases=20 failures=0
> exit=0
```
Counter: `limb R5 fixed=1 read=refiled=ok original=unchanged`. Result is a fabricated receipt of a failing run, accepted.

## Finding 3 — stub emitter passes (fixed=1)

Tree with `corpus/instruments/r44-routed-defects.py` replaced by a 5-line stub that prints `selftest cases=20 failures=0` and `sys.exit(0)`; the refiled file is the stub's real stdout plus the invocation line. Counter: `limb R5 fixed=1 read=refiled=ok original=unchanged`. The limb cannot distinguish a stub's output from a real run.

## Discriminating controls (same counter, same base baseline)

| tree | construction | limb R5 line printed |
|---|---|---|
| t0 | do-nothing base | `limb R5 fixed=0 read=refiled-absent` |
| t1 | marker-only (`# refiled`) | `limb R5 fixed=0 read=selftest-token-absent` |
| t6 | honest real run, failing (5e4d6bf) + invocation line | `limb R5 fixed=0 read=selftest-token-absent` |
| t7 | honest real run, passing (c950fa3) + invocation line | `limb R5 fixed=1 read=refiled=ok original=unchanged` |
| t8 | honest disclosure quoting the failed bare call (`usage:` / `error:` lines kept) + real passing run | `limb R5 fixed=0 read=usage-or-error-line-present` |
| t2/t3/t4/t5/t9 | attack trees above | `fixed=1` |

Reading: the verdict tracks lexemes, not provenance. The honest disclosure of the failed bare call (t8) is refused; the fabricated three-liner (t2/t9), a copy of the lane's on-disk file (t3), an edited failing run (t4) and a stub emitter (t5) all pass. t6 vs t4 differ only in the two tokens, showing the limb reads text, not the run.

## Finding 4 — refiled receipt is not in any commit (observation, not an attack)

`git status --porcelain -- .ufo/waves/round-44/controls/` prints `?? .ufo/waves/round-44/controls/final-attempt3-refiled.txt`; `git ls-files` on that path prints nothing. Counter on the HEAD export (`git archive 5242db6`):
```
limb R5 fixed=0 read=refiled-absent
```
So the honest refile the lane wrote is invisible to a committed-tree replay until it is committed. The lane must commit it (not done by this seat).

## Limitations

- I attacked R5 only. Its fixed=1 is one of five; I did not construct a full C1 fixed=5 control, so the C1 kill rule ("control grades fixed=5") is not tested here. R5's gameability is shown at limb level.
- The frozen `c1-marker-only` control tree is named in `controls/freeze-controls.txt` but not supplied in the lane; I used my own marker tree (t1).
- Out-of-limb observation (not graded, not in my C1-R5 scope): the receipt header names tip `c950fa3`, where the real `r44-routed-defects.py --selftest` prints `selftest cases=20 failures=0` (exit 0) and the counter prints `fixed=8`. The lesson names closure tip `5e4d6bf`, where the same selftest prints `failures=1`, and the r44 counter prints `limb R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping` / `routed-defects total=8 fixed=7 unresolved=1 exit=1`. I did not investigate why; `git diff --stat c950fa3 5e4d6bf` shows `LOG.md | 7 +++` and `final-attempt3.txt | 38 +++`.
- Base export is a fresh `git archive dc5bb8c`, verified identical to `/fast/scratch/hyaku/kasegi-r45/L1/pure` (`diff -rq` empty). Read-only git only; no commit, push, index or fleet-root writes. Scratch `/fast/scratch/hyaku/kasegi-r45/R45RevLimbR5/` removed on exit.

## Suggested repair (for the lane; not applied here)

Bind R5 to a run, not text: have the limb re-execute `r44-routed-defects.py --root <tree> --selftest --work <tmp>` on the tree and require its stdout to equal the refiled body (or pin the receipt by sha in the freeze record), and refuse on any `error:` line only in the original, not in the refile that documents it. Then add t2/t4/t5 as committed counter controls that must grade fixed=0.

## Tool installs

None. No tools installed or upgraded.
