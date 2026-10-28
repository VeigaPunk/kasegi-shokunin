# R45W2MutC1R5 — mutation test of C1 limb R5 (v1.1) and freeze controls

VERDICT: BROKEN

Scope: C1 limb R5 of `corpus/instruments/r45-routed-defects.py` (v1.1) and the do-nothing / marker-only controls in `.ufo/waves/round-45/controls/freeze-controls.py`. Subject: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd). Counter and controls were run from the export only; the moving lane tree was not touched. Read-only: `git archive` and `git show` only; no commit, push, or git mutation; no shared file written.

Integrity of the attacked bytes (re-run):
```
$ sha256sum exp/corpus/instruments/r45-routed-defects.py
680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67
$ git show 6662a42…:corpus/instruments/r45-routed-defects.py | sha256sum
680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67  -
$ sha256sum exp/.ufo/waves/round-45/controls/freeze-controls.py
79e45b985a30a3a11a47de3ef8a319c6b863aba915d17e3a3415abcde677a37e
$ git show 6662a42…:.ufo/waves/round-45/controls/freeze-controls.py | sha256sum
79e45b985a30a3a11a47de3ef8a319c6b863aba915d17e3a3415abcde677a37e  -
```

## Limb R5 under test (counter lines 292-318)

- L297 `if re.search(r"^(usage:|.*error:)", t, re.M | re.I): return False` — the only check against the failed bare call.
- L299 `lines = t.splitlines()`; L300-305 exact-match one invocation line and exactly one `exit=0` line; body = lines strictly between them.
- L316 `sha("\n".join(body)) == PINS["refiled-body"]` and `^selftest cases=20 failures=0$` in body.
- L309 original `final-attempt3.txt` byte-equal to baseline.

The docstring (lines 31-34) states R5 means the receipt carries "the selftest invocation **without the failed bare call**". The code never tests for the bare call; it only tests for a `usage:`/`error:` text line at column 0 (or with `error:`). Anything outside the pinned body that avoids those two literal strings is invisible to R5.

## Baseline and controls (re-run)

Tip export, all limbs green:
```
$ python3 corpus/instruments/r45-routed-defects.py --root exp --baseline base
limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
```
Freeze controls (`freeze-controls.py --base-export base --lane exp --work <scratch>`):
```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
```
Per-limb reason for R5 in those two controls (re-run):
```
do-nothing-base:  limb R5 fixed=0 read=refiled-absent
c1-marker-only:   limb R5 fixed=0 read=invocation-lines=0
```
Finding on the controls: the marker-only control creates `final-attempt3-refiled.txt` from nothing (`append` mode), so R5 is red for "no invocation line", not for the marker content. No freeze control exercises a tree where the receipt exists with the genuine invocation and body. Those controls therefore cannot discriminate any R5 survivor below.

## Mutation recipe

Script in scratch (`recipe.py`, removed on exit). Each mutant: fresh copy of the tip export, one edit to `.ufo/waves/round-44/controls/final-attempt3-refiled.txt`, counter run from the pristine tip (TOOL_ROOT = tip, grader model) with `--baseline` = pristine base. `rejected=1` iff limb R5 prints `fixed=0`. Anchor `$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>` asserted unique before each edit.

Command and output (re-run):
```
$ TMPDIR=<scratch> python3 recipe.py
mutant=C0-tip-unmutated rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=D0-do-nothing-base rejected=1  limb R5 fixed=0 read=refiled-absent
mutant=T1-tip-marker-only rejected=1  limb R5 fixed=0 read=receipt-body-not-the-pinned-run-output
mutant=M01-bare-usage-verbatim rejected=1  limb R5 fixed=0 read=usage-or-error-line-present
mutant=M02-bare-usage-indented rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=M03-bare-error-dash rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=M04-bare-exit2-prefix rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=M05-bare-exit2-suffix rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=M06-bare-exit0-prefix rejected=1  limb R5 fixed=0 read=exit0-line-absent
mutant=M07-usage-after-LS rejected=0  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
mutant=M08-body-embedded rejected=1  limb R5 fixed=0 read=receipt-body-not-the-pinned-run-output
summary mutants=8 rejected=3 survivors=['M02-bare-usage-indented', 'M03-bare-error-dash', 'M04-bare-exit2-prefix', 'M05-bare-exit2-suffix', 'M07-usage-after-LS']
```

## Survivors (listed first)

Each survivor is a re-introduction of the failed bare call that R5 is documented to forbid. Edits are applied to the refiled file only; the rest of the tip stays as shipped.

### S1 — M04-bare-exit2-prefix (strongest)
- Exact edit: insert two lines immediately before the `$ python3 … --root <tip> --selftest …` line (file line 3):
  ```
  $ python3 corpus/instruments/r44-routed-defects.py --selftest
  exit=2
  ```
- Diff (re-run): `2a3,4 > $ python3 corpus/instruments/r44-routed-defects.py --selftest` / `> exit=2`.
- R5: `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`.
- Full counter on this tree (re-run):
  ```
  limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
  routed-defects total=5 fixed=5 unresolved=0 exit=0
  ```
- Contradiction on the artifact itself: the receipt header (line 1) still says the bare call "is not repeated". The bare call is in the file; the counter stays green.
- Why it survives: L297 needs `usage:`/`error:`; `exit=2` is not `exit=0`, so L303 ignores it; the bare-call line is outside the pinned body (L306).

### S2 — M05-bare-exit2-suffix
- Exact edit: append after the final `exit=0` line: `$ python3 corpus/instruments/r44-routed-defects.py --selftest` then `exit=2`.
- R5: `fixed=1 read=refiled=pinned-run-output original=unchanged`.
- Why: L303 takes the first `exit=0` and L306 slices only up to it; L297 finds no usage/error text. Nothing bounds the file after the body.

### S3 — M02-bare-usage-indented
- Exact edit: before the invocation line insert `$ python3 corpus/instruments/r44-routed-defects.py --selftest`, then `  usage: r44-routed-defects.py [-h] --root ROOT` (two leading spaces), then `exit=2`.
- R5: `fixed=1 read=refiled=pinned-run-output original=unchanged`.
- Why: L297 anchors `usage:` at column 0 (`^`); the indented usage line is not matched. No `error:` line is present, so `.*error:` does not fire.

### S4 — M03-bare-error-dash
- Exact edit: before the invocation line insert the bare call, then `r44-routed-defects.py: error -- the following arguments are required: --root`, then `exit=2`.
- R5: `fixed=1 read=refiled=pinned-run-output original=unchanged`.
- Why: L297 requires the literal `error:` (colon). The argparse message with ` -- ` in place of `: ` passes.

### S5 — M07-usage-after-LS
- Exact edit: before the invocation line insert `$ python3 corpus/instruments/r44-routed-defects.py --selftest<U+2028>usage: r44-routed-defects.py [-h] --root ROOT` (U+2028 LINE SEPARATOR instead of newline), then `exit=2`.
- R5: `fixed=1 read=refiled=pinned-run-output original=unchanged`.
- Why: L297 runs with `re.M`, so `^` only matches after `\n`; U+2028 is not that. L299 `t.splitlines()` splits on U+2028, so the same text is one way for the usage check and another way for the invocation/exit check. Contrived as a receipt, but it shows the limb mixes two line models.

## Discriminators (detector works where it should)

- M01 verbatim usage block + exit=2 → `rejected=1 … read=usage-or-error-line-present` (the defect as shipped is caught).
- M06 bare call + second `exit=0` → `rejected=1 … read=exit0-line-absent`.
- M08 bare call + exit=2 inside the body → `rejected=1 … read=receipt-body-not-the-pinned-run-output`.
- T1 markers-only tip receipt → `rejected=1 … read=receipt-body-not-the-pinned-run-output`.
- C0 unmutated tip → `rejected=0`; D0 do-nothing base → `rejected=1 … read=refiled-absent`.

So: body edits and exit-count edits are caught. Edits outside the body that avoid the two literal strings are not. Byte-level pins (body sha, original-receipt equality, counter sha) are not the gap; the gap is the unpinned prefix/suffix and the literal-string predicate.

## Recommendation (not applied; no shared file touched)

Pin the whole refiled file's sha256 (or require `^# ` header lines + exact invocation + body + exact `exit=0` and nothing else), and reject any line matching `^\$ python3 .*r44-routed-defects\.py` not carrying `--root`, and any `exit=` line other than the single `exit=0`. The stated R5 predicate is then enforced rather than approximated by two regexes.

## Limitations

- Only R5 was mutated; R1-R4 were green in every run and were not attacked except via the full-counter re-run (M04, M07).
- Pinned constants (refiled-body, original receipt, counter bytes) were treated as given; their values were not re-derived. Per instructions, byte forgeries under pins are moot and were not pursued.
- The baseline argument is supplied by the grader; I did not attack baseline substitution.
- M07 is a regex/line-model weakness; I do not claim it is a realistic reviewer-facing receipt.
- The R5 receipt body is accepted by sha only; the r44 selftest was not re-run (by design in the counter), so I did not verify the body's semantic truth.
- Each mutant was run once; runtime ~25 s for the recipe. Timing did not affect verdicts (deterministic pure-file checks).
- Freeze-controls output above is from one run; the controls' R5 reasons are as printed, not inferred.

## Tooling

No tools installed or upgraded. Scratch root `/fast/scratch/hyaku/kasegi-r45/R45W2MutC1R5` (exp, base, recipe.py, mutant refiled files, ctl/) removed on exit.
