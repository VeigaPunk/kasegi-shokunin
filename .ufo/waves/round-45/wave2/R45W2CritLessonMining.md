VERDICT: BROKEN

Seat R45W2CritLessonMining (critic, leaf, falsify wave). Item: propose the three best mistakes for `corpus/lessons/round-45.md` `## Mistakes` from R45ScoutMistakes and the lesson skeleton, each with a red-before command that can fail. Attacked: integration tree `6662a42` (exported with `git archive` to scratch, never the lane tree), freeze commit `8cf62c8`, pure base export `L1/pure` (copied), `c950fa3` and `5e4d6bf` exports (LOG and r44 counter history), counters `corpus/instruments/r45-c2-gate.py` (v1.1) and `r44-routed-defects.py`. Result: all three scout candidates reproduce, and a fourth result shows the v1.1 C2 counter still grades 7/7 on a presence-only entry. Verdict BROKEN is for C2 v1.1, not for the lesson rows.

Common setup (all runs by this seat; `B` = copied base, `F` = freeze export, `T` = tip export, `X5` = `5e4d6bf` export, `X9` = `c950fa3` export, `FX` = presence fixture below; scratch paths elided):

```
$ python3 F/corpus/instruments/r45-c2-gate.py --root B      # freeze-committed counter bytes on pure base
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G4 pass=0 read=manifest-absent
gate G7 pass=1 read=census-rc=0
c2-gate fixed=1/7 exit=1
$ python3 F/corpus/instruments/r45-c2-gate.py --root F      # freeze commit 8cf62c8
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G7 pass=1 read=census-rc=0
c2-gate fixed=2/7 exit=1
$ python3 F/corpus/instruments/r45-c2-gate.py --root T      # integration tree 6662a42
c2-gate fixed=7/7 exit=0
$ python3 F/corpus/instruments/r45-routed-defects.py --root B --baseline B
routed-defects total=5 fixed=0 unresolved=5 exit=1
$ python3 F/corpus/instruments/r45-routed-defects.py --root T --baseline B
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=1 read=selftest-cases=43
limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2
limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
```

These match `.ufo/waves/round-45/controls/freeze-controls.txt:1-2` for the base rows, and the tip C1 and C2 reads reproduce the lane's claimed after-state.

---

## Proposed `## Mistakes` rows

### M45-a — before-cell measured on base, but the frozen commit already reads 2/7 (class: number-drift / stale-premise)

- Error: `claims.json` C2 `expect_before` is `c2-gate fixed=1/7 exit=1` (`.ufo/waves/round-45/claims.json:26`). That is the base reading, and it is correct for base. But the frozen commit `8cf62c8` already carries `corpus/source-snapshots/round-45/S071.txt` (372 lines, sha256 `0918dcfa…`) and `manifest.json` (`git show --stat 8cf62c8`). Those two captures turn gate G4 green before any seat runs, so the freeze tree reads 2/7. The claim's before-text ("held nowhere in corpus/") is still true for the narrow grep it names, but the before-value is tree-relative and the lesson does not say which tree it binds.
- Evidence pointer: `.ufo/waves/round-45/claims.json:22,26`; `.ufo/waves/round-45/controls/freeze-controls.txt:2` (base row only; no freeze-tree row); `git show --stat 8cf62c8` (S071/S072 captures in the freeze commit); `corpus/instruments/r45-c2-gate.py:223-235` (G4 passes on the committed capture).
- Captured-by: none. R47 (`corpus/QUALITY.md:380`) replays the do-nothing control on base, which this does; R43 (`:369`) binds the before-cell to the control it cites, which is base. Nothing requires the before-value to be stated per start tree.
- Red-before (can fail): `python3 F/corpus/instruments/r45-c2-gate.py --root F | tail -1` must print `c2-gate fixed=1/7 exit=1` to match `claims.json:26`. It printed `c2-gate fixed=2/7 exit=1`. Discrimination: the same bytes on `B` print `fixed=1/7`, so the mismatch is the tree, not the counter.
- Fix: keep `1/7` as the base before, and add the freeze-tree reading (`2/7`, G4 and G7 green) as a named row in `freeze-controls.txt` and the claim, so the before is explicit per tree. Rejected fix: rewriting `expect_before` to `2/7` breaks R47, because the base control then prints `1/7` against a declared `2/7`: `python3 F/corpus/instruments/r45-c2-gate.py --root B | tail -1` → `c2-gate fixed=1/7 exit=1`, which is red against the rewritten value.

### M45-b — receipt goes stale after a later LOG append: r44 counter D4 binds the last `## Round 44` heading (class: stale-premise under R18/R19)

- Error: `corpus/instruments/r44-routed-defects.py:404` reads `head = log.rfind("## Round 44")` and takes `log[head:]` to end of file. The `5e4d6bf` commit appends `## Round 44 (attempt 3) — …` at `LOG.md:1994` (7 lines, `git diff c950fa3 6662a42 -- LOG.md`). That heading becomes the last match, so D4 no longer sees the attempt-1 section that holds `planner=L1` (`LOG.md:1980`). D4 flips green to red, and the counter's own POSITIVE selftest case flips with it. The receipt `cases=20 failures=0` that the attempt-3 LOG entry and the r45 R5 pin rely on was true only at `c950fa3`.
- Evidence pointer: `corpus/instruments/r44-routed-defects.py:404-406`; `LOG.md:1965,1977,1994` (headings); `corpus/instruments/r45-routed-defects.py:314-317` (R5 pins the receipt body by sha256 "instead of a re-run" because of this); `LOG.md` round-44 attempt-3 entry (receipt cited as `cases=20 failures=0` at tip `c950fa3`).
- Commands and printed output (this seat):
  - `python3 X9/corpus/instruments/r44-routed-defects.py --root X9 --baseline X9` → `R44-D4 status=fixed … 66 seats cross-check`; `routed-defects total=8 fixed=8 unresolved=0 exit=0`.
  - `python3 X9/corpus/instruments/r44-routed-defects.py --root X9 --selftest --work W` → `selftest cases=20 failures=0`, exit 0.
  - `python3 X5/corpus/instruments/r44-routed-defects.py --root X5 --selftest --work W` → `selftest case=POSITIVE verdict=fail fixed=7 unresolved=1`, `selftest cases=20 failures=1`, exit 1.
  - `python3 X5/… --root X5 --baseline X5` → `R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping`.
  - Same at tip `6662a42`: `selftest cases=20 failures=1`, `POSITIVE verdict=fail fixed=7 unresolved=1`. At `dc5bb8c` (round base) the counter reads `fixed=7 unresolved=1 exit=1`.
- Discrimination (do-nothing control): tip tree with only `LOG.md` replaced by the `c950fa3` bytes → `selftest cases=20 failures=0`, `R44-D4 status=fixed`. The counter bytes are identical in `c950fa3` and tip (`git diff --stat c950fa3 6662a42 -- corpus/instruments/r44-routed-defects.py` empty), so the flip is caused by the LOG append alone.
- Captured-by: none. No QUALITY criterion requires a bound section to be selected by content rather than by its last heading, and no criterion re-runs a selftest at the tip before quoting its tally.
- Red-before (can fail): `python3 X5/corpus/instruments/r44-routed-defects.py --root X5 --selftest --work W | tail -1` must print `failures=0`. It printed `selftest cases=20 failures=1`.
- Fix tested in scratch only: replace the `rfind` with a scan over every `## Round 44…` section (`re.split(r"(?m)^(?=## )", log)`, keep sections that start with `## Round 44`). Patched copy on tip → `selftest cases=20 failures=0` and `R44-D4 status=fixed`. Landing this needs a new sha256 pin for `r44-routed-defects.py` in `r45-routed-defects.py` PINS (`d5438c67…`), a re-run of the R5 receipt, and a new receipt; it cannot be done by editing the tip's LOG alone.

### M45-c — C2 v1 falsified by presence, v1.1 still passes a presence-only entry (class: presence-only, R48)

- Error: the wave-1 critic showed v1 graded 7/7 on a boilerplate F27 entry (`.ufo/waves/round-45/wave1/R45CritKillC2.md:22-43`: "A boilerplate-only landing reaches 7/7 … Analysis content difference: 0 words"). v1.1 claims to close the class (`r45-c2-gate.py:29-36`), but its G2 checks headings and a 3-cell table count, G6 checks a size floor of 3000 bytes, and G5 accepts any four located quote spans. An entry made of located quotes copied from the real F27 table, with padding, passes all seven gates.
- Fixture `FX` (scratch only, built by this seat from the tip's real F27 entry): header lines 3-5 copied from the tip entry, the four `## …` sections with one filler sentence each, nine real located table rows copied verbatim, two cross-references, then 400 lines of `Padding.`. File size 7535 bytes; `grep -c '^Padding\.$'` → `400`.
- Command and output on v1.1 (the tip's counter bytes):
  ```
  $ python3 T/corpus/instruments/r45-c2-gate.py --root FX
  gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
  gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=9 xrefs=2/2
  gate G3 pass=1 read=row-S071=ok
  gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
  gate G5 pass=1 read=spans=12 located=12 failed=0 uncited=0 cores=4/4
  gate G6 pass=1 read=knowledge=64 base-names-intact=1 entry-bytes-ok=1
  gate G7 pass=1 read=census-rc=0 ok-line=1
  c2-gate fixed=7/7 exit=0
  ```
- Red-before (can fail): the same command on `FX` must print fewer than `7/7` if the class is closed. It prints `7/7 exit=0`. Discrimination: base `B` → `1/7`; real tip entry → `7/7`; `FX` → `7/7`, so the counter cannot tell a zero-analysis entry from the real one.
- Fix (not in the lane; a candidate limb to test): a limb that rejects an entry with any line repeated 20 or more times. `FX` shows `Padding.` ×400, so the check would fire. The non-author closure named in the kill rule remains the only gate that grades analysis; that must be stated in the row's captured-by.
- Captured-by: R48 (`corpus/QUALITY.md:381`) names the class and the counter's v1.1 header claims it. The only wave-1 falsifier of the boilerplate fixture (`R45CritKillC2.md:22-43`) reports v1 output. A grep of `.ufo/waves/round-45` for `boilerplate` returns only wave-1 reports and the wave-1 spec/results files; no round-45 record shows that fixture graded by v1.1 before freeze or integration (this seat's run is the first such record).

---

## Discriminated, not mined

- Scout candidate 1 (M44 rows without a criterion), candidate 2 (SKILL row for r44 tools), candidate 3 (S070 flip), candidate 4 (`final-attempt3-refiled.txt`), candidate 5 (C2 before `1/7`) were not re-derived one by one; the commands I ran above cover the parts that bear on M45-a, M45-b and M45-c. I did not re-run the scout's `corpus/SOURCES.md` or `QUALITY.md` greps.
- `corpus/source-snapshots/round-30/S046.txt` and `round-35/S052.txt` match `security-bugs|kernel.org`, but only as `git.kernel.org/stable` advisory links (`S052.txt:660`). They do not hold the security-bugs process, so the C2 before-text stands at base.
- The scout's statement that r44 reads `fixed=7` "at later trees" is correct but understates it: the base `dc5bb8c` reads 7/8 too (`R44-D4 status=unresolved`). The round-44 `8/8` exists only at `c950fa3`.

## Limitations

- The v1 counter bytes are not in the tree (digests only in the docstrings). The v1 evidence in M45-c is quoted from `R45CritKillC2.md:22-43`, not re-run.
- `FX` is a constructed fixture, not a real landing. It shows what the predicate accepts, not that a seat produced it.
- The D4 fix was tested only in a scratch copy; no lane file was edited and no pin was changed.
- No live fetch; S071/S072 captures were used as committed (pins matched: `S071.txt` `0918dcfa…`, `S072.txt` `364166c4…`).
- Tools installed: none. No git mutation, no commit, no write outside this report. Scratch under `$HYAKU_SCRATCH/kasegi-r45/R45W2CritLessonMining/` removed before yield.
