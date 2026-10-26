# ExecScoreGap — round 31 receipt

Seat: `ExecScoreGap`. Item: implement considerthese/2026-10-25.md proposal 2
("distance to the next score, computed from committed bytes") as a read-only
reporter. **Not a claim; asserts no score move.**

- Answering model actually run: `devin/deepseek-v4-1-flash` (route table decides; no model passed by me).
- Write scope used: `corpus/instruments/score-gap.py` (owned) + this receipt. Nothing else touched.
- Lane base `b374feb`; claims-freeze `738a779`; HEAD at my run `8a8916c` (wave-1 spec). All measurements below are on the wave's uncommitted working tree — §5 is the in-flight PRE-STATE, §6 the final run on quiescent bytes.

## 1. File

```
$ sha256sum corpus/instruments/score-gap.py
855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb  corpus/instruments/score-gap.py
$ wc -l corpus/instruments/score-gap.py
548 corpus/instruments/score-gap.py
$ python3 -c "compile(open('corpus/instruments/score-gap.py').read(),'score-gap.py','exec'); print('compile ok')"
compile ok
```

Stdlib only (`argparse contextlib hashlib io os re shutil subprocess sys tempfile`).
No third-party import, no network, no git call, no write path in the reporter.

## 2. What it does (contract, from the docstring)

Five fields, each from a stated command over the lane's bytes:

| field | source | printed line |
|---|---|---|
| 1 rechecks | `python3 corpus/instruments/recheck-audit.py --root <root> --quiet` (subprocess) | `recheck: lines=… executes=… gated=… broken=… exit=…` |
| 2 anchors | `python3 corpus/instruments/anchorcheck.py SKILL.md` (subprocess, cwd=root) | `anchorcheck: in-range=… bad=… lost-recorded=… origin=… outside-base=… base-absent=… exit=…` |
| 3 census | `corpus/instruments/citation-survival.md` (parsed, never retyped) | `census-definition:` / `census-lane:` / `census-skill:` |
| 4 threshold | `SCORECARD.md` line naming the score-5 bar | `threshold: SCORECARD.md:<lineno> "<quoted sentence>"` |
| 5 gap | computed from field 1 (`gated`, `lines`) | `gap: <k> of <n> rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` |

Every run also prints `source: <rel> sha256=<…>` for the four input files, so a
number can always be traced to the exact bytes that produced it. `--root`
defaults to the lane the instrument lives in, so it runs from any cwd. Exit 0 on
a complete read (even when the lane's own gates are red — the reporter reports,
it does not judge), exit 2 when an input is missing/unreadable or no longer
yields its field.

## 3. Selftest — `python3 corpus/instruments/score-gap.py --selftest` (exit 0)

Two fixture lanes (`a`, `b`) built in `tempfile.mkdtemp`, differing in every
reported field; each field must move between them, and each fixture's tree
digest must be unchanged after the run (no-write proof).

```
$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py --selftest
selftest recheck-mode=real
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
selftest gap-computed                 ok got='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims' want='1 of 2 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims'
selftest exit2-missing-census         ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/citation-survival.'
selftest exit2-missing-recheck        ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: corpus/instruments/recheck-audit.py ('
selftest exit2-missing-scorecard      ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE missing input: SCORECARD.md (/tmp/score-gap-selftest'
selftest exit2-no-threshold           ok rc=2 want=2 msg='score-gap: INPUT-UNREADABLE SCORECARD.md no longer names the score-5 threshold ('
selftest fields=7 failures=0
$ echo $?
0
```

This is the run on the FINAL instrument bytes (`recheck-audit.py`
`5d4842da…`, `anchorcheck.py` `d0f35f8c…`, the §6 inputs). Fixture `a`/`b`
differ in every reported field; `anchorcheck` verdicts come from the real
instrument (a PAST-EOF, an `~/Projects/bounties/../outside.md:1` escape, a
BASE-ABSENT against an absent mirror root, and an IN-RANGE(ORIGIN) against a
fixture origin root), so the parse is exercised on real verdict lines, not on a
hand-written summary.

`recheck-mode=real`: the selftest copies the lane's real `recheck-audit.py` into
the fixture lane (it prints that mode). If the copy cannot be run — the
instrument is under concurrent edit this wave — it prints
`recheck-mode=stub reason=…` and falls back to a documented stand-in that emits
the frozen `--quiet` summary shape, so the selftest never fails for someone
else's in-flight bytes. `anchorcheck.py` is always the real instrument.

Unreadable-input cases (each asserted `rc=2`): missing `citation-survival.md`,
missing `recheck-audit.py`, missing `SCORECARD.md`, `SCORECARD.md` with no
score-5 threshold line.

## 4. cwd invariance

```
$ cd /tmp && python3 …/corpus/instruments/score-gap.py            > /tmp/sg-cwd-tmp.txt
$ cd …/kasegi-shokunin && python3 corpus/instruments/score-gap.py --root . > /tmp/sg-cwd-lane.txt
$ diff /tmp/sg-cwd-tmp.txt /tmp/sg-cwd-lane.txt && echo identical
identical
```

## 5. PRE-STATE run (in-flight, M30-3 — non-comparative, superseded by §6)

Run while `corpus/knowledge/vendor-third-party-finding-coordination.md` (F15/S048,
ExecEntryF15) was already on disk but `corpus/instruments/knowledge-expected.txt`
(ExecExpectedList) did not yet list it. `recheck-audit.py` was uncommitted work by
ExecRALimbs at both runs and byte-identical across them
(`5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`), so the only
difference between this block and §6 is the expected-list file. Labelled
PRE-STATE; **do not compare its numbers to §6.**

```
$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=44 executes=20 gated=24 broken=0 exit=1
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
$ echo $?
0
```

The `exit=1` in field 1 was `recheck-audit.py`'s own summary red, not the
reporter's: `expect=present expected=43 missing=0 unexpected=1 exit=1` — the new
F15/S048 entry was on disk and `knowledge-expected.txt` had not yet listed it.
Reporter exit was still 0 (it reports; it does not judge).

## 6. FINAL run on quiescent bytes

Quiescence gate: polled (20 s interval, `[ -s <receipt> ]`) until
`ExecEntryF15.md`, `ExecExpectedList.md` and `ExecRALimbs.md` all existed (200 s),
then re-ran `recheck-audit.py --quiet`: `lines=44 total=44 pass=44
fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` and
`expect=present expected=44 missing=0 unexpected=0 exit=0`.

```
$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py   # exit 0
$ cd …/kasegi-shokunin && python3 corpus/instruments/score-gap.py --root .                            # exit 0
$ diff /tmp/sg-final-tmp.txt /tmp/sg-final-lane.txt && echo CWD-INVARIANT-identical
CWD-INVARIANT-identical
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=7 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- (lane total|SKILL\.md alone): ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

Measured inputs (sha256, final):

```
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912  corpus/instruments/anchorcheck.py
795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d  corpus/instruments/citation-survival.md
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md
a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc  SKILL.md
855869bf97ae2081c24ed28630d587ad2988872b6625f6e0a1f8c7b2e3f201fb  corpus/instruments/score-gap.py
```

Read-only statement of the measured gap (not a claim, no score move asserted):
**24 of 44** recheck lines still run and fail closed on an absent base, so
`gated` has not reached the 0 the score-5 sentence names; field 4's threshold is
`SCORECARD.md:331`. Whether any of the 24 is "unsupported" is a semantic question
this reporter does not decide — it prints `gated`, and the threshold sentence's
own denominator is "25/25 source chains", which the r22 line it lives in states.

## 7. Writes

```
$ ls corpus/instruments/__pycache__ | grep -c score-gap
0
$ git status --porcelain corpus/ SCORECARD.md
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/knowledge-expected.txt
 M corpus/instruments/recheck-audit.py
 M corpus/instruments/source-recheck.py
?? corpus/instruments/limb-fixtures/
?? corpus/instruments/limb-ledger.json
?? corpus/instruments/limb-mutation-check.py
?? corpus/instruments/score-gap.py
?? corpus/knowledge/vendor-third-party-finding-coordination.md
?? corpus/source-snapshots/round-31/
```

Every `M`/`??` above except `corpus/instruments/score-gap.py` belongs to another
seat in this wave (SCORECARD = ScribeErratum, QUALITY = ScribeQuality,
README = ScribeReadmeF15, SOURCES = ExecRegistryAppend,
knowledge-expected.txt = ExecExpectedList, recheck-audit.py = ExecRALimbs,
source-recheck.py = ExecSRLimbs, limb-fixtures/ + limb-mutation-check.py =
ExecCounter/ExecSRLimbs/ExecFRLimbs, limb-ledger.json = ExecLedgerMerge,
vendor-third-party-finding-coordination.md = ExecEntryF15,
source-snapshots/round-31/ = ExecCapManifest). The reporter added nothing: it
opens inputs read-only, runs the two instruments without their
`--json`/`--receipt` options, and writes no `__pycache__` (it invokes them with
`-B`). The selftest's own no-write proof is the `no-write-a`/`no-write-b` lines
in §3 (fixture tree digest unchanged across the run).

## 8. Risks / limits

- The census field is the **committed** r18 census of record, not a live re-run
  of `resolve.py`; it is quoted with its own definition sentence and its file
  sha256, so it cannot silently read as current. Re-running `resolve.py` is a
  write (it rewrites `citation-survival.md`/`.tsv`), which this seat does not own.
- `gated` is `recheck-audit.py`'s own definition ("the line runs and fails closed
  on an absent base"). A recheck line that starts passing when its base returns
  moves this number without any knowledge entry changing — that is the point.
- The threshold field depends on one English sentence in `SCORECARD.md`; if
  ScribeErratum's append rewords it, the reporter exits 2 (loud) rather than
  printing a stale line number.
- `anchorcheck.py` exits 0 with 306 LOST-RECORDED anchors in `SKILL.md`: those
  are recorded-not-checked, so field 2's `bad=0` is a statement about *supported
  anchored token shapes*, not about the 306. The reporter prints the buckets
  separately for exactly that reason.
