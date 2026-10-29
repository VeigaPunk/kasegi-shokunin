VERDICT: BROKEN

Seat R46W2CritMistake (mistake-mining critic). Scope: mined row M46-1 (class `landing`; round-45 report named lane commit `2998baa` by a clock that preceded it; fix = `corpus/instruments/r46-landing-gate.py` `date-order-author` check + a QUALITY R50 row). Lane tree = commit `5437afe`. Every command below was run by me, read-only against the lane and fleet (`git show`, `git log`, `git reflog`, `jj metaedit --help`, the gate in `--post-report` mode, and the gate's own `--selftest` in scratch). Nothing was committed, installed or mutated. No jj command was run against any repo (jj snapshots the working copy).

Summary: (1) the defect is not on the report or the landed content; it is on the AUTHOR clock the gate and the round-45 spot-check read as "time the text was written". (2) The `date-order-author` fix fails honest histories (round-44 and round-28 pairs and a constructed honest amend), so it is a false positive, not a repair. (3) `landing` is the wrong class; `stale-premise` (C06) fits. (4) QUALITY R50 does not exist in the integrated tree. (5) `captured-by: none` is mechanically true but describes a non-defect.

## F1 — The clocks on the round-45 pair (what the spot-check read, and what the gate reads)

Attacked: `a1f7761` (fleet, `.ufo/reports/round-45/kasegi.md`) and `2998baa` (lane, cited as final).

```
$ git -C /home/vgpnk/Projects/shokunin show -s --format='%H|author %an %ad %at %aI|committer %cn %cd %ct %cI|%s' a1f7761b572e8c78d9d3b64d5d1e6a655f152a11
a1f7761b572e8c78d9d3b64d5d1e6a655f152a11|author kasegi-shokunin Wed Oct 28 19:30:06 2026 -0300 1793226606 2026-10-28T19:30:06-03:00|committer kasegi-shokunin Wed Oct 28 19:37:42 2026 -0300 1793227062 2026-10-28T19:37:42-03:00|round-45: kasegi report
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show -s --format='%H|author %an %ad %at %aI|committer %cn %cd %ct %cI|%s' 2998baab4c39e6f0c1b50b150c5965e1643c4e11
2998baab4c39e6f0c1b50b150c5965e1643c4e11|author kasegi-shokunin Wed Oct 28 19:36:30 2026 -0300 1793226990 2026-10-28T19:36:30-03:00|committer kasegi-shokunin Wed Oct 28 19:36:31 2026 -0300 1793226991 2026-10-28T19:36:31-03:00|round-45: wave 2 results, final measurement, errata, lesson, LOG, SCORECARD
```

Reading: the spot-check's "19:30:06" (`corpus/lessons/round-45-verifier-spotcheck.md:22`) is the fleet commit's AUTHOR stamp. Its COMMITTER stamp is 19:37:42, which is after the cited commit's committer stamp (19:36:31). The author stamp was not updated by the 19:37:42 rewrite.

Existence corroboration, independent of author stamps (export reflogs, read-only):

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin reflog --date=iso --format='%h %gd %gs' | grep 2998baa
2998baa HEAD@{2026-10-28 19:36:31 -0300} export from jj
$ git -C /home/vgpnk/Projects/shokunin reflog --date=iso --format='%h %gd %gs' | grep a1f7761
a1f7761b HEAD@{2026-10-28 19:37:42 -0300} export from jj
```

Lane HEAD was `2998baa` from 19:36:31 until the next lane export at 19:50:18 (`914ca0b`), so `2998baa` was the lane tip when the report was filed; the report's "final" is correct at filing time.

## F2 — Red-before receipt, round-45 pair (live and replay)

Command (live; the lane has since moved, so `final-is-tip` fails honestly):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-landing-gate.py --post-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --report .ufo/reports/round-45/kasegi.md --fleet /home/vgpnk/Projects/shokunin
check report-readable pass=1 read=bytes=15428
check cited-hashes pass=1 read=n=6,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=0 read=final-not-tip=2998baab4c39,tip=0d121a201fe7(ls-remote)
check date-order pass=1 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-committer=2026-10-28T19:37:42-03:00
check date-order-author pass=0 read=latest-cited=2998baab4c39@2026-10-28T19:36:31-03:00,report-commit-author=2026-10-28T19:30:06-03:00
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=8 fail=2 exit=1
```

Replay at the report's own tip (`--tip 2998baab4c39e6f0c1b50b150c5965e1643c4e11`): identical except `check final-is-tip pass=1 read=final-not-tip=0,tip=2998baab4c39(override)`, and the last line `landing-gate mode=post-report checks=8 fail=1 exit=1`. So on the round-45 pair the only red is `date-order-author`; the committer-clock `date-order` is green.

Note: `0d121a201fe7` is the live `ls-remote` tip I read at run time (network was available); it is not a result claim about the lane beyond that.

## F3 — Should-pass control: the round-44 pair (report `18f5a1f5`, lane `5e4d6bf`)

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h|ad=%aI|cd=%cI|%s' -- .ufo/reports/round-44/kasegi.md
18f5a1f5|ad=2026-10-28T17:40:44-03:00|cd=2026-10-28T17:43:29-03:00|round-44: kasegi report
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show -s --format='%h ad=%aI cd=%cI' 5e4d6bf
5e4d6bf ad=2026-10-28T17:42:35-03:00 cd=2026-10-28T17:42:35-03:00
$ python3 .../r46-landing-gate.py --post-report --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --branch master --report .ufo/reports/round-44/kasegi.md --fleet /home/vgpnk/Projects/shokunin --tip 5e4d6bf4324421d0e393f4da9bc623165bb5b0b7
check report-readable pass=1 read=bytes=13008
check cited-hashes pass=1 read=n=1,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=1 read=final-not-tip=0,tip=5e4d6bf43244(override)
check date-order pass=1 read=latest-cited=5e4d6bf43244@2026-10-28T17:42:35-03:00,report-commit-committer=2026-10-28T17:43:29-03:00
check date-order-author pass=0 read=latest-cited=5e4d6bf43244@2026-10-28T17:42:35-03:00,report-commit-author=2026-10-28T17:40:44-03:00
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=8 fail=1 exit=1
```

Reflogs (read-only): lane `5e4d6bf HEAD@{2026-10-28 17:42:35 -0300}`, next lane export `dc5bb8c HEAD@{2026-10-28 17:47:59 -0300}`; fleet `18f5a1f5 HEAD@{2026-10-28 17:43:29 -0300} export from jj`. So `5e4d6bf` was the lane tip when the round-44 report was filed, and the report names it correctly.

Result: the author-clock fix is RED on a pair that is in order by every existence clock. Identical shape to round 45, smaller gap.

Round-28 pair (`361c31bd` fleet, ad 14:46:45 / cd 15:03:02; cites lane `32f694b`, ad=cd 15:02:08) gives the same author-only red: `date-order` pass=1, `date-order-author` pass=0 (`latest-cited=32f694b38e02@2026-10-25T15:02:08-03:00,report-commit-author=2026-10-25T14:46:45-03:00`). Its `final-is-tip` also fails because the report names a second "final" hash (`1265fe11`); that is an extraction artifact, not used.

## F4 — Discrimination table (fixtures are built in scratch; the fixture repo is removed on exit)

A constructed honest history. The report text is first committed at author stamp 1793226606 (19:30:06) without the hash; the hash of the lane commit (committer 1793226991 = 19:36:31) is written into the report and the commit is amended with a later committer stamp and no `--reset-author`:

```
$ git -C "$FLEET" log -1 --format='ad=%ad %at  cd=%cd %ct  subject=%s' --date=raw
ad=1793226606 +0000 1793226606  cd=1793227062 +0000 1793227062  subject=report
```

Gate over the three fixture reports (`--tip` = the fixture lane commit):

```
== report.md   (honest amend)
  add-commit ad=1793226606 cd=1793227062
check date-order pass=1 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-committer=2026-10-28T22:37:42Z
check date-order-author pass=0 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-author=2026-10-28T22:30:06Z
landing-gate mode=post-report checks=8 fail=1 exit=1
== report2.md  (genuine defect: report committed before the hash existed)
  add-commit ad=1793226606 cd=1793226606
check date-order pass=0 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-committer=2026-10-28T22:30:06Z
check date-order-author pass=0 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-author=2026-10-28T22:30:06Z
landing-gate mode=post-report checks=8 fail=2 exit=1
== report3.md  (clean: filed after landing)
  add-commit ad=1793227062 cd=1793227062
check date-order pass=1 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-committer=2026-10-28T22:37:42Z
check date-order-author pass=1 read=latest-cited=f54b5a467256@2026-10-28T22:36:31Z,report-commit-author=2026-10-28T22:37:42Z
landing-gate mode=post-report checks=8 fail=0 exit=0
```

Discrimination (do-nothing control = a gate that exits 0 on everything; expected verdict = defect present only for report2):

| case | expected | committer `date-order` | author `date-order-author` | do-nothing |
|---|---|---|---|---|
| round-45 `a1f7761` | clean (F1, F2) | pass | FAIL | agrees |
| round-44 `18f5a1f5` | clean (F3) | pass | FAIL | agrees |
| round-28 `361c31bd` | clean (heuristic-free pair, F3) | pass | FAIL | agrees |
| honest amend fixture | clean | pass | FAIL | agrees |
| genuine defect fixture (report2) | defect | FAIL | FAIL | disagrees |
| clean fixture (report3) | clean | pass | pass | agrees |

The author check fires on every honest history and on the genuine defect alike; it does not discriminate. The committer check separates the genuine defect (report2) from honest histories. The do-nothing control disagrees only on the genuine defect, so the author check adds false positives and no true positives.

## F5 — The committed gate's own selftest encodes the premise

```
$ TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46W2CritMistake/selftest-work python3 corpus/instruments/r46-landing-gate.py --selftest --work .../selftest-work
selftest case=post-date-inversion-author-only-round45-shape expect=date-order-author got=date-order-author verdict=pass
selftest cases=30 failures=0
```

The fixture for that case sets author < cited commit < committer by construction, so it confirms the gate's reading of the author stamp, not the premise. The gate docstring states the premise (`corpus/instruments/r46-landing-gate.py:32-35`): "the author time is when the report text was written, and it is the clock the round-45 defect inverted." F1–F4 show the first clause is false under the jj export and git amend behaviour.

## F6 — Which clock is the defect on

- Author clock: the defect. Git amend keeps the author date by default (demonstrated by the F4 fixture); jj keeps it on rewrite. `jj metaedit --help` (jj 0.45.1, read-only help text) states: "--update-author-timestamp: Update the author timestamp. This updates the author date to the current time, without modifying the author." So the author stamp is the change's first-commit stamp, not the write time.
- Committer clock: the sound one. A commit hash covers its committer stamp, so a cited hash's committer stamp is its creation instant (the lane reflog confirms: `2998baa` exported 19:36:31 = its committer stamp). A report commit's committer stamp is its last write, an upper bound on the text it contains. Validity needs cited committer <= report committer; the author stamp bounds neither.
- The lane's own convention agrees: `corpus/instruments/r40-closure.sh:110-116` ("`time-basis=ref-commit` states exactly what `run-utc` is: the committer instant of `export-ref` ... NOT a wall-clock stamp ... a wall-clock stamp that outran its own commit was the round-39 R1/M39-1 false-provenance defect"); `corpus/instruments/r43-closure.sh:173` (`git show -s --format=%cI`); `corpus/QUALITY.md:351` (R39: "a receipt whose only instant equals the named ref's committer instant"); `corpus/QUALITY.md:370` (R44: "not later than the commit that contains it").

## F7 — The class is wrong: `landing` is not the defect

- `CORPUS.md:175` lists the vocabulary; `landing` is C09 "Evidence landing — marker, missing SHONEN, placeholder, overwrite" (`.ufo/waves/kaika-w1/mistakes.md:244`). Every C09 row is a defect in what lands at a canonical path. The round-45 report landed with resolvable, ancestor, tip-correct hashes (F1, F2) and no marker or overwrite.
- The defect, as the spot-check framed it, is a premise: "the report was written at 19:30:06, so it named a commit that did not yet exist". That premise is the author stamp read as write time. C06 "Stale premise — claim built on superseded state" (`mistakes.md:191`) is the fitting class.
- Sibling class C01 (reference drift: "quote/pointer does not say what is claimed") is a weaker alternative; the quoted stamp is accurate as a stamp, the inference drawn from it is the error.

## F8 — captured-by: none (grep of corpus/QUALITY.md)

- R33 (`corpus/QUALITY.md:292`): "...the report is filed after the last lane commit." Its clause holds on the round-45 pair (committer 19:37:42 > cited 19:36:31; reflog export order agrees, F1). So R33 is not violated by round-45; `none` is the mechanical truth for an order criterion, but nothing was missed.
- R33 is prose-only for this clause. The mechanised parts, `corpus/instruments/r38-closure.sh:65-100` (G2 judged-head binding, G4 closure order = results files present), read no report or lane clock. A genuine report-before-commit defect (the report2 shape) would pass every existing instrument. That is the real gap, and it is an R33 gap, not an M46-1 gap.
- R43 (`corpus/QUALITY.md:369`) grades committed counter output by its bytes; it has no clock clause. Not applicable.
- R44 (`corpus/QUALITY.md:370`) is the nearest mechanised clock criterion, and it binds to the containing commit's committer stamp, which is the convention in F6.
- QUALITY R50 does not exist in the integrated tree. My check (python over `corpus/QUALITY.md` rows matching `^\| (R\d+) \|`) printed `R-rows total: 49 max: 49`. The fix's "QUALITY R50" row is absent, so the lesson cannot cite it.

## F9 — Fix status under CORPUS "a fix is shown able to fail"

The red receipt (F2) does exit 1 for the named check, and the committed selftest passes 30/30 (F5). That shows the check can fail. It also fails on the round-44 control, the round-28 control and an honest fixture (F3, F4). A check that fails on honest history is not a repair. The fix does not count.

## Required lesson row (what the Mistakes row must say)

Replace the M46-1 row with:

| ID | Class | Error | Evidence pointer | Captured by | Fix | Evidence the fix can fail |
|---|---|---|---|---|---|---|
| M46-1 | stale-premise | The round-45 spot-check (`corpus/lessons/round-45-verifier-spotcheck.md:22`, routed item :95) read report commit `a1f7761`'s AUTHOR stamp (19:30:06) as when its text was written and concluded it named lane commit `2998baa` (committed 19:36:31) before that commit existed. Report COMMITTER stamp is 19:37:42; export reflogs put `2998baa` (19:36:31) before `a1f7761` (19:37:42). No landed artifact was wrong. | `git show -s --format=... a1f7761 2998baa`; `git reflog`; fixture `ad=1793226606 cd=1793227062` | none: no criterion reads report-versus-lane order by commit clock; R33 (`QUALITY.md:292`) holds on this pair; R33's clause is prose-only (r38-closure G2/G4 read no report clock) | Retract the routed item with an appended correction to `round-45-verifier-spotcheck.md`. Do not ship the `date-order-author` check: it fails round-44 (`18f5a1f5` vs `5e4d6bf`), round-28 (`361c31bd` vs `32f694b`) and an honest amend fixture. Keep only the committer-clock `date-order`. | Author-only red on honest history: F3, F4. |

Do not mint QUALITY R50. If the lane wants a capture, the candidate is a R33 mechanisation of the report-filing clause on the committer instant (the F6 convention), and that needs its own red-before on a genuine defect (the report2 shape), not on round-44 or round-45.

## Limitations

- The export reflogs (`export from jj`) show when the lane and fleet were exported, not when text was typed. Existence ordering uses them only as corroboration of hash existence and export order; the argument that the text naming `2998baa` postdates 19:36:31 rests on hash determinism (a commit id covers its committer stamp), not on the reflog alone.
- The fleet reflog holds one entry for the round-45 report (`a1f7761`), so no earlier version was observed. Whether the round-44 and round-28 reports were amended is an inference from the stamps (cd > ad with the cited commit between), not an observed rewrite.
- The F4 honest-amend fixture proves the mechanism (git amend keeps author stamp, so honest text can show author < cited < committer); it does not prove round-45 was amended. The conclusion does not depend on that: any text naming `2998baa` postdates 19:36:31.
- jj behaviour is taken from `jj metaedit --help` (jj 0.45.1). I did not run any jj command against the repos (jj snapshots the working copy, a mutation).
- The cross-round batch I attempted (every `kasegi` report, final hash by regex) produced noisy picks for rounds 1–43 and 45's neighbours (`final-is-tip` and `date-order` failures on hashes that are not the lane final); those rows are discarded and only the hand-verified pairs (rounds 28, 44, 45) are used.
- ls-remote needs network; the live run used it.
- Round-44's own lane spot-check (`kasegi-shokunin/corpus/lessons/round-44-verifier-spotcheck.md`) raised no ordering defect (grep for order/clock found only a dispatch digest); I did not audit the rest of that file.
- No installs. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2CritMistake`) is removed on exit; the fixture repos lived only there.
