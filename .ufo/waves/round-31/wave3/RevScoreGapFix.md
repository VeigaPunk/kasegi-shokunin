# RevScoreGapFix — round 31 wave 3 review receipt

- Seat: `RevScoreGapFix` (reviewer; leaf, one write scope: this file). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, lane base `b374feb`, claims freeze `738a779`, reviewed at lane `HEAD a155310d1ee9aacc07c3ce62328105a46c0392b4` (wave-2 repair commit `fd29aac`).
- Subject: the wave-2 repair to `corpus/instruments/score-gap.py`, judged against `.ufo/waves/round-31/wave2/RevScoreGap.md` **D1** and **D2**. All work in `/tmp` scratch copies; no lane write except this receipt.
- Reviewed bytes = committed bytes: `sha256sum corpus/instruments/score-gap.py` → `d9cebe99044bebb4ffea72b725d7cb458dd4bd4806740dfacb3b9ed4ce526927`, identical to `git show HEAD:corpus/instruments/score-gap.py | sha256sum` and to `git show fd29aac:…`; `git diff --stat HEAD -- <the four docs below>` is empty. Pre-repair (wave-1 landing `eecad59`) was `855869bf…e3f201fb`, so this is post-repair, quiescent bytes.
- Answering model: `opencode-go/deepseek-v4.1-flash` (per the route table; never passed by this seat).
- Tools installed/upgraded: **none**. `pyflakes 4.0.3` and `python3 3.14.8` were already on the host (`/home/vgpnk/.local/bin/pyflakes`); no pacman transaction, no network fetch, no `uv`/`npx` install.

## Verdict: `defect` — D1 fixed and verified; D2 **not** fixed (the repair is inert), and the repair left three committed digest pins stale

The D1 repair does what D1 asked: the census `cmd:` now reproduces `census-lane` and `census-skill` on today's bytes **and** on mutated bytes. The D2 repair changed the fixture writer to `json.dumps(...)` but never added `import json` to the module, so the advertised `recheck-mode=stub` fallback still dies with a traceback — a different one (`NameError`) at the same place. The second half of D2 (`selftest()` indexing a field the report did not produce → `KeyError`) was not touched at all and is still reachable. Separately, the repair changed the file's bytes without updating any of the three committed documents that pin its digest, so `corpus/instruments/README.md`'s own "Re-verify … Targets: the six digests above" procedure is now red for `score-gap.py`.

### Repair delta under review

```
$ git diff eecad59 fd29aac -- corpus/instruments/score-gap.py
  @@ -180,7 +180,7 @@ def field_census(root):
  -        "cmd": "grep -nE '^Numerator = |^- (lane total|SKILL\\.md alone): ' %s" % CENSUS_REL,
  +        "cmd": "grep -nE '^Numerator = |^- lane total \\(SKILL\\.md \\+ corpus\\): |^- SKILL\\.md alone: ' %s" % CENSUS_REL,
  @@ -406,7 +406,7 @@ def _make_fixture(parent, variant, real_instruments, recheck_mode):
  -               "".join('%s: %d,\n' % (k, v) for k, v in spec["recheck"].items()))
  +               json.dumps(spec["recheck"]))
```

Two lines. No import change, no selftest-arm change, no digest-document change.

## 1. D1 — census `cmd:` provenance: **FIXED** (verified three ways)

### 1a. The printed command reproduces the printed values, on today's bytes

Report from the lane (exit 0, stderr empty):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/score-gap.py; echo "EXIT=$?"
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
EXIT=0
```

Each `cmd:` line was extracted from that output and executed verbatim (nothing retyped), cwd = lane root, with the ` (cwd=…)` annotation stripped from `[2]` only:

```
### [1] rechecks | verbatim-runnable=True
CMD> python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
RC=0
OUT: strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0\nexecutes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)\nlines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0\nexpect=present expected=44 missing=0 unexpected=0 exit=0\n

### [2] anchors | verbatim-runnable=False
CMD> python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
RC=0
OUT: \n== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0\n…

### [3] citation-survival census (committed figures) | verbatim-runnable=True
CMD> grep -nE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
RC=0
OUT: 29:Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).\n31:- SKILL.md alone: **32/506 = 6.32%**\n33:- lane total (SKILL.md + corpus): **134/1480 = 9.05%**\n

### [4] score-5 threshold | verbatim-runnable=True
CMD> grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
RC=0
```

`census-lane: 134/1480 = 9.05%` and `census-skill: 32/506 = 6.32%` both appear verbatim in the `[3]` command's output at lines 33 and 31 — exactly the two lines the wave-2 finding said were missing. `[1]`'s `lines=44 executes=20 gated=24 broken=0 exit=0` and `[2]`'s seven buckets match their printed blocks. `[4]`'s quoted sentence is a verbatim substring of `SCORECARD.md:331` and occurs once:

```
$ grep -Fc 'Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims.' SCORECARD.md
1
$ grep -c 'unsupported current claims' SCORECARD.md
1
```

Pattern counts on the census file show the new pattern is exactly selective (no extra lines, no missing line):

```
$ grep -cE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
3
$ grep -cE '^- lane total \(SKILL\.md \+ corpus\): ' corpus/instruments/citation-survival.md
1
$ grep -cE '^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
1
```

### 1b. The `cmd:`↔value coupling holds on **non-today** bytes (not a coincidence)

Scratch root `S3` = copy of `SKILL.md`, `SCORECARD.md`, `corpus/instruments/{citation-survival.md,recheck-audit.py,anchorcheck.py}`, with both census rates mutated (`134/1480 = 9.05%` → `141/1490 = 9.46%`, `32/506 = 6.32%` → `33/509 = 6.48%`). The report and the printed command move together:

```
$ cd "$S3" && python3 <lane>/corpus/instruments/score-gap.py --root "$S3"
[3] citation-survival census (committed figures)
census-lane: 141/1490 = 9.46%
census-skill: 33/509 = 6.48%
EXIT=0
$ cd "$S3" && bash -c "<the printed [3] cmd>"
29:Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
31:- SKILL.md alone: **33/509 = 6.48%**
33:- lane total (SKILL.md + corpus): **141/1490 = 9.46%**
CMD_EXIT=0
```

This rules out "the string happens to match today's file": the printed pattern tracks the parsed value. **D1 closed on both counts** (value provenance; reproducibility from the printed string). No doc quotes the old census pattern (`grep -rn "Numerator = |" --include='*.md' . --exclude-dir=.ufo` → only `corpus/lessons/round-31.md:127`, which quotes the *wave-2 finding*, not a pinned expected output).

## 2. D2 — stub fallback: **NOT FIXED**. The repair is inert; `--selftest` still dies with a traceback

### 2a. Forced stub on the landed bytes → `NameError`, exit 1, traceback

Forcing is the wave-2 recipe: a scratch copy of the instrument directory whose `recheck-audit.py` prints nothing, so the pre-flight fails and `mode` flips to `stub`. `_make_fixture` copies from `here` (the directory holding `score-gap.py`), so this is the exact advertised fallback path.

```
$ S1=$(mktemp -d); mkdir -p "$S1/corpus/instruments"
$ cp <lane>/corpus/instruments/{score-gap.py,anchorcheck.py,recheck-audit.py} "$S1/corpus/instruments/"
$ printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' > "$S1/corpus/instruments/recheck-audit.py"
$ cd / && python3 "$S1/corpus/instruments/score-gap.py" --selftest; echo "STUB_EXIT=$?"
selftest recheck-mode=stub reason=corpus/instruments/recheck-audit.py --quiet printed no executes/gated/broken summary (exit 0)
STUB_EXIT=1
stderr:
Traceback (most recent call last):
  File "/tmp/revsg-stub.Tae7by/corpus/instruments/score-gap.py", line 548, in <module>
    sys.exit(main())
  File "/tmp/revsg-stub.Tae7by/corpus/instruments/score-gap.py", line 532, in main
    return selftest()
  File "/tmp/revsg-stub.Tae7by/corpus/instruments/score-gap.py", line 474, in selftest
    roots[variant], envs[variant] = _make_fixture(tmp, variant, here, mode)
  File "/tmp/revsg-stub.Tae7by/corpus/instruments/score-gap.py", line 409, in _make_fixture
    json.dumps(spec["recheck"]))
    ^^^^
NameError: name 'json' is not defined. Did you forget to import 'json'?
```

So the `JSONDecodeError` is gone (the fixture data is valid JSON now — that half of D2 is done) but the branch still cannot run: the module never imports `json`. Note the masking detail that let this land: `grep -n '^import json' corpus/instruments/score-gap.py` matches **line 293**, which is inside the `STUB_RECHECK` triple-quoted string (the stub script's own import), not module scope.

AST + pyflakes, base vs repaired:

```
$ python3 -c "import ast; …print module-level Import names…"
module imports: ['argparse', 'contextlib', 'hashlib', 'io', 'os', 're', 'shutil', 'subprocess', 'sys', 'tempfile']
json imported: False

$ /home/vgpnk/.local/bin/pyflakes corpus/instruments/score-gap.py; echo "PYFLAKES_EXIT=$?"
corpus/instruments/score-gap.py:409:16: undefined name 'json'
PYFLAKES_EXIT=1

$ git show eecad59:corpus/instruments/score-gap.py > /tmp/base.py && /home/vgpnk/.local/bin/pyflakes /tmp/base.py; echo "PYFLAKES_BASE_EXIT=$?"
PYFLAKES_BASE_EXIT=0
```

The repair introduced a static error the wave-1 file did not have.

### 2b. One line proves the repair is sufficient once `json` is in scope

Same scratch copy, only `import io\nimport os` → `import io\nimport json\nimport os`:

```
$ cd / && python3 "$S1/corpus/instruments/score-gap.py" --selftest; echo "STUB_PATCHED_EXIT=$?"
selftest recheck-mode=stub reason=corpus/instruments/recheck-audit.py --quiet printed no executes/gated/broken summary (exit 0)
selftest exit-a                       ok rc=0 want=0 err=''
selftest no-write-a                   ok tree digest unchanged=True
selftest exit-b                       ok rc=0 want=0 err=''
selftest no-write-b                   ok tree digest unchanged=True
selftest recheck.lines                ok a=2 b=3
selftest recheck.executes             ok a=1 b=2
selftest recheck.gated                ok a=1 b=0
selftest recheck.broken               ok a=0 b=1
selftest anchorcheck.in-range         ok a=1 b=2
selftest anchorcheck.bad              ok a=2 b=0
selftest anchorcheck.lost-recorded    ok a=1 b=3
selftest anchorcheck.origin           ok a=0 b=1
selftest anchorcheck.outside-base     ok a=1 b=0
selftest anchorcheck.base-absent      ok a=1 b=0
selftest anchorcheck.exit             ok a=1 b=0
selftest census-lane                  ok a='100/200 = 50.00%' b='3/4 = 75.00%'
selftest census-skill                 ok a='10/20 = 50.00%' b='3/8 = 37.50%'
selftest census-definition            ok a='Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denomin' b='Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denomin'
selftest threshold                    ok a='SCORECARD.md:5 "Threshold for 5: a non-author audit passing ' b='SCORECARD.md:10 "Threshold for 5: all source chains passing '
selftest gap                          ok a='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims' b='0 of 3 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims'
selftest gap-computed                 ok got='1 of 2 rechecks…' want='1 of 2 rechecks…'
selftest exit2-missing-census         ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/citation-survival.'
selftest exit2-missing-recheck        ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/recheck-audit.py ('
selftest exit2-missing-scorecard      ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: SCORECARD.md (/tmp/score-gap-selftest'
selftest exit2-no-threshold           ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE SCORECARD.md no longer names the score-5 threshold ('
selftest fields=7 failures=0
STUB_PATCHED_EXIT=0
```

pyflakes on the patched copy is clean (`PATCHED_EXIT=0`). Required fix: one `import json` in the module import block (`score-gap.py:45-55`). Nothing else in the stub path is broken.

### 2c. D2's **second** fault (`KeyError`) is untouched and still reachable

`selftest()` reads `a["recheck"]` (`score-gap.py:485`) and `a["anchorcheck"]` (`:488`) without checking that the report produced those fields. Any fixture report that exits non-zero yields `reports[variant] == []` (`main()` prints nothing before `report()` returns), so the next section raises. Demonstrated with the reachable trigger — a concurrently-edited `anchorcheck.py` in the instruments directory, which the pre-flight does **not** probe (it probes only `recheck-audit.py`, then `shutil.copy`s `anchorcheck.py` unconditionally at `score-gap.py:411-412`):

```
$ S2=…; cp <lane>/corpus/instruments/{score-gap.py,anchorcheck.py,recheck-audit.py} "$S2/corpus/instruments/"
$ printf '#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n' > "$S2/corpus/instruments/anchorcheck.py"
$ cd / && python3 "$S2/corpus/instruments/score-gap.py" --selftest; echo "ANCH_FAIL_EXIT=$?"
selftest recheck-mode=real
selftest exit-a                       FAIL rc=2 want=0 err='score-gap: INPUT-UNREADABLE corpus/instruments/anchorcheck.py printed no summary line for SKILL.md (exit 0) (/tmp/score-'
selftest no-write-a                   ok tree digest unchanged=True
selftest exit-b                       FAIL rc=2 want=0 err='score-gap: INPUT-UNREADABLE corpus/instruments/anchorcheck.py printed no summary line for SKILL.md (exit 0) (/tmp/score-'
selftest no-write-b                   ok tree digest unchanged=True
ANCH_FAIL_EXIT=1
stderr:
  File "/tmp/revsg-anch.rKcEwN/corpus/instruments/score-gap.py", line 485, in selftest
    ra, rb = _split_counts(a["recheck"]), _split_counts(b["recheck"])
                           ~^^^^^^^^^^^
KeyError: 'recheck'
```

The `FAIL` lines print first (good), then the run still ends in a raw `KeyError` traceback instead of a named failure. This is the same defect class wave-2 filed as "make the field loops skip/declare a missing field instead of raising" (`wave2/RevScoreGap.md` D2, second sentence) — **not addressed** by `fd29aac`.

### 2d. Why no gate caught it: the stub branch has no committed coverage

`_values()`' prefix list (`score-gap.py:435-436`) collects only *value* lines; no `cmd:` and no stub arm. The only committed invocation of the fallback is inside the instrument itself:

```
$ grep -rn 'recheck-mode' --include='*.md' --include='*.py' . --exclude-dir=.ufo
./corpus/instruments/score-gap.py:469:        print("selftest recheck-mode=%s%s" % (mode, (" reason=%s" % why) if why else ""))
./corpus/lessons/round-31.md:127: … (prose describing the wave-2 finding)
./corpus/lessons/round-31.md:154: … (prose describing the wave-2 finding)
$ grep -rln 'no executes/gated/broken summary\|printed no executes' --include='*.md' --include='*.py' --include='*.sh' . --exclude-dir=.ufo
./corpus/instruments/score-gap.py
```

`python3 … --selftest` in real mode passes (`recheck-mode=real`), which is why both waves' receipts are green while the branch is dead. A committed arm is needed, not a bigger claim.

## 3. Repair-induced provenance defect: three committed documents pin the pre-repair digest

The repair changed the file but no document that pins it. Every pin in the lane still names `855869bf…` while the file is `d9cebe99…`:

```
$ grep -rn '855869bf' --exclude-dir=.ufo --exclude-dir=.jj --exclude-dir=.git .
./corpus/instruments/README.md:463:| `corpus/instruments/score-gap.py` | absent | `855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb` |
./corpus/knowledge/considerthese-proposals-ledger.md:28:| 2. Track “distance to the next score,” … `corpus/instruments/score-gap.py` (sha256 `855869bf…`
./corpus/lessons/round-31.md:127:… Instrument `sha256 855869bf…e3f201fb` …
$ sha256sum corpus/instruments/score-gap.py
d9cebe99044bebb4ffea72b725d7cb458dd4bd4806740dfacb3b9ed4ce526927  corpus/instruments/score-gap.py
$ git log --format=%h\ %s -2 -- corpus/instruments/README.md
eecad59 …  (README last touched at wave-1 integration; the file moved at fd29aac and no README byte moved with it)
```

`README.md` says "run after any edit to these files" and "Targets: the six digests above" (`README.md:478-490`); running that exact line now shows two mismatches — `score-gap.py` (mine) and `limb-mutation-check.py` (C1's, both changed by the same commit `fd29aac`, `c660a95f…` → `237fd07c…`):

```
$ bash -c "$(sed -n '480p' corpus/instruments/README.md)"
5d4842da…  corpus/instruments/recheck-audit.py          # matches pin
fd2e01e8…  corpus/instruments/source-recheck.py         # matches pin
aa60b581…  corpus/instruments/frontier-recheck-count.py # matches pin
237fd07c…  corpus/instruments/limb-mutation-check.py    # PIN SAYS c660a95f…  (C1 row; routing)
c042adf6…  corpus/instruments/limb-ledger.json          # matches pin
d9cebe99…  corpus/instruments/score-gap.py              # PIN SAYS 855869bf…  (this subject)
```

This is the M31-3/O5 class (a fix that changes bytes and leaves the pinned literal behind) recurring inside the repair under review. It is not a wave-1/wave-2 residual: it was created by `fd29aac`.

## 4. Properties re-verified good (no finding)

**(a) The reporter writes nothing.** Whole-lane digest (excluding `.ufo/`, `.jj/`, `.git/`, where sibling seats write receipts) before/after a full report run, and no file newer than a marker:

```
$ digest() { find . -type f -not -path './.ufo/*' -not -path './.jj/*' -not -path './.git/*' -print0 | sort -z | xargs -0 sha256sum | sha256sum; }
$ before=$(digest)   # 1b9dd166f9363c11b6f0ff1d952dcef1abaa726d24f55920281c950913dee329
$ python3 corpus/instruments/score-gap.py >/dev/null 2>&1; echo "run_exit=$?"   # run_exit=0
$ after=$(digest)    # 1b9dd166f9363c11b6f0ff1d952dcef1abaa726d24f55920281c950913dee329
DIGEST_UNCHANGED=yes
$ touch /tmp/mark; sleep 1; python3 corpus/instruments/score-gap.py >/dev/null 2>&1; echo "run2_exit=$?"   # run2_exit=0
$ find . -newer /tmp/mark -type f -not -path './.ufo/*' -not -path './.jj/*' -not -path './.git/*' | wc -l
0
```

`--selftest` writes nothing either, and leaves no tempdir:

```
$ digest around `python3 corpus/instruments/score-gap.py --selftest`
selftest_exit=0
SELFTEST_DIGEST_UNCHANGED=yes
leftover_selftest_dirs=0
```

Corroboration: the shared `corpus/instruments/__pycache__/` (untracked, from other seats' runs; 8 `.pyc`) contains no `score-gap` entry, and the reporter passes `-B` to both children (`score-gap.py:121,148`). A `chmod -R a-w` lane copy still runs to completion (`RO_EXIT=0`).

**(b) cwd invariance.** From the lane and from `cd / … --root <lane>`: exit 0 both, stderr empty both, stdout byte-identical:

```
$ cmp lane.out root.out && echo BYTE_IDENTICAL=yes   # BYTE_IDENTICAL=yes
$ wc -c root.err   # 0
```

**(c) `--selftest` from the lane and from `cd /`.** Both exit 0, byte-identical output, stderr empty, `selftest fields=7 failures=0`:

```
ST_LANE_EXIT=0 / ST_ROOT_EXIT=0 / SELFTEST_OUTPUT_IDENTICAL=yes
selftest recheck-mode=real … selftest fields=7 failures=0
```

**(d) Fail-closed exit 2, no partial report.** Missing input and a census file whose lane line is reworded to the old non-parenthetical form both exit 2 with a single stderr line and **zero stdout bytes** (so no half-report can be mistaken for a measurement):

```
$ cd / && python3 <lane>/corpus/instruments/score-gap.py --root "$S7"   # S7 lacks SCORECARD.md
E3_EXIT=2 stdout_bytes=0
score-gap: INPUT-UNREADABLE missing input: SCORECARD.md (/tmp/revsg-e3.PAmWwT/SCORECARD.md)
$ … --root "$S6"   # census lane line mutated to `- lane total: **134/1480 = 9.05%**`
BAD2_EXIT=2 stdout_bytes=0
score-gap: INPUT-UNREADABLE corpus/instruments/citation-survival.md no longer states both the lane and SKILL.md rates (/tmp/revsg-bad2.5oeVAE/corpus/instruments/citation-survival.md)
```

**(e)** The `gap:` line is still computed from field 1 (`24` of `44` = field 1 `gated`/`lines`) and `selftest gap-computed ok`.

## 5. Low findings (new, not blocking)

- **L1 — `[3]`/`[4]` `cmd:` are cwd-relative; `[1]` prints an absolute root.** Run the report with `--root` from another cwd and the census/threshold commands as printed fail there:

  ```
  $ cd / && bash -c "grep -nE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md"; echo "C3_FROM_ROOT_EXIT=$?"
  grep: corpus/instruments/citation-survival.md: No such file or directory
  C3_FROM_ROOT_EXIT=2
  ```

  The `root:` header makes the interpretation recoverable and the lane-cwd reading is the documented one (`README.md:478`), so this is low — but D1's acceptance test ("run the printed command") only works from the lane root, while `[1]` works from anywhere. Printing `(cwd=<root>)` or `cd <root> && …` for `[3]`/`[4]` would close it.
- **L2 — `[2]`'s `cmd:` is not verbatim-runnable** (`python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=…)`; the annotation is part of the printed string), unlike `[1]`/`[3]`/`[4]`.
- **L3 — `[1]`'s `cmd:` interpolates `root` unquoted** (`score-gap.py:137`): a lane path containing a space yields a non-runnable string. Cosmetic; the lane path has no space today.

## 6. Residual (wave-1/wave-2 findings; listed, not demanded)

- **W1 (open)** — `anchorcheck.py` remains an undigested input: `python3 corpus/instruments/score-gap.py | grep -c 'sha256='` → `4`; its digest (`d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912`) does not occur in any report line (`grep -c` → `0`). Dead parsed fields (`anchors`, `pin_broken`, `total`) unchanged.
- **W2 (open)** — printed `python3 …` vs invoked `[sys.executable, "-B", …]` (`score-gap.py:121,148` vs `:137,163`); the `-B` no-write flag still absent from the printed strings.
- **R1** — `gap:` still renders one conjunct of the `SCORECARD.md:331` threshold as "0 gated unsupported claims"; `gated` is `recheck-audit.py`'s fail-closed class, and the 25/25 source-chain conjunct is measured nowhere in the report.
- **R2** — a copied root still reports a red `exit=1` for field 1 (absolute lane paths in the audited `recheck:` lines), with no "root ≠ the root the rechecks name" note.
- **R3 (open, confirmed)** — the census block still prints the r18 census of record as a committed figure with no revision/date; `README.md:410` discloses it.
- **R4** — `census-definition` remains a near-vacuous arm (moves only by trailing fixture wording).
- **R5** — threshold parsing still depends on one English sentence; removing it exits 2 (verified arm `exit2-no-threshold ok`), two matches are flagged.

## 7. Exact fixes the L1 should route (this seat writes nothing but this file)

1. `corpus/instruments/score-gap.py`: add `import json` to the module import block (after `import io`, before `import os`) — one line; §2b shows the stub branch then passes `fields=7 failures=0` exit 0.
2. `corpus/instruments/score-gap.py:485,488`: guard the missing-field crash — if a fixture report did not yield a field, print a named `selftest <field> FAIL` for it (or skip the section) instead of raising `KeyError`; §2c is the reproducer.
3. Update the three digest pins the repair invalidated (`corpus/instruments/README.md:463`, `corpus/knowledge/considerthese-proposals-ledger.md:28`, `corpus/lessons/round-31.md:127`) to `d9cebe99…` — or, if those files are append-only this round, append the correction as the lane's convention requires and say so at `README.md:478-490`. The C1 owner has the same job for `limb-mutation-check.py`'s row (`c660a95f…` → `237fd07c…`).
4. Add one committed arm that forces `recheck-mode=stub` (e.g. point the pre-flight at a no-print copy) so the fallback cannot rot again; today `grep -rn 'recheck-mode' --include='*.py' --exclude-dir=.ufo` finds only the instrument itself.
5. Optional, low: print `-B` in `[1]`/`[2]`'s `cmd:` (W2); make `[3]`/`[4]`'s `cmd:` runnable from any cwd (L1); quote `root` in `[1]`'s `cmd:` (L3).

## 8. Verification gaps

- No `lsp` device is mounted in this seat (only `ast_edit`/`debug`), so `references`/`definition`/`diagnostics` were unavailable; caller/definition checks used `grep` as the literal fallback plus AST parsing (`ast.parse` import inventory) and execution. Recorded as unavailability, not as evidence of absence.
- Out of scope and untouched: the C1 limb ledger/counter, C2 census/harness numbers, and every score judgement. Nothing here asserts or suggests a score move.
- I did not re-run the mutated-copy census test against a *second* reworded form beyond the two mutations in §1b, and did not test a root path containing spaces (L3 is by inspection plus the code line).
- Concurrency: reviewed bytes were quiescent (`git diff --stat HEAD` empty for the four documents; lane digest identical across my two runner windows).

## 9. Cleanup

Scratch removed: `/tmp/revsg.l7TEdX`, `/tmp/revsg-stub.Tae7by`, `/tmp/revsg-anch.rKcEwN`, `/tmp/revsg-census.*`, `/tmp/revsg-ro.yt0dVF`, `/tmp/revsg-e2.*`, `/tmp/revsg-e3.*`, `/tmp/revsg-bad*.*`, `/tmp/revsg-base-sg.py`; `ls -d /tmp/revsg-* | wc -l` → `0`; `/tmp/score-gap-selftest-*` → `0`.

Write footprint: this receipt. No lane file, no `.ufo` state/watchdog/manifest, no fleet-root/sibling-lane/shokuknow write; no git/jj mutation (read-only `log`/`show`/`diff`/`rev-parse` only, no git fixture needed); no pacman transaction; no tool install; no network fetch; no live bounty-target contact; no credential or vault material.
