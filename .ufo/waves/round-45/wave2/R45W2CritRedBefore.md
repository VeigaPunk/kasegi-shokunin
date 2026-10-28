VERDICT: BROKEN

Seat: R45W2CritRedBefore (red-before critic, QUALITY R42/R47). Tree attacked: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4; do-nothing control: export of base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd. Both exported with `git archive | tar -x` into scratch; the lane working tree was not read. Only read-only git was used (`archive`, `cat-file`, `rev-parse`). Nothing was committed or mutated.

Method: for each repair I (a) ran the same command at base, (b) built "tip minus that one repair" (copy of the tip export with only that repair's bytes reverted to base or removed) and re-ran the same command, and (c) recorded whether the command's named reason flips and nothing else does. A repair with a committed pair (red at base or minus-one, green at tip) is listed as "covered". Everything below was re-run by me in this seat.

## 1. Covered: C1 counter, reverse-one per repair (`r45-routed-defects.py --root V --baseline base`)

Base control (do-nothing):
```
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=r44-frontier-count-not-the-pinned-bytes
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1
```
Tip: `routed-defects total=5 fixed=5 unresolved=0 exit=0`.

Reverse-one (only the named repair reverted; all other limbs stay fixed=1):
- S070 correction removed from `corpus/lessons/round-44.md`: `limb R1 fixed=0 read=lesson-correction-absent-or-quotes-no-located-S072-span`; total fixed=4.
- S072 row removed from `corpus/SOURCES.md`: `limb R1 fixed=0 read=row-S072=absent`; total fixed=4.
- S072 snapshot removed: `limb R1 fixed=0 read=recheck-rc=2-quotes=0`; total fixed=4.
- QUALITY.md at base: `limb R2 fixed=0 read=quality-not-append-only-or-unchanged`; total fixed=4.
- r44-frontier-count.py at base bytes: `limb R3 fixed=0 read=r44-frontier-count-not-the-pinned-bytes`; total fixed=4.
- freeze-check.py removed: `limb R4 fixed=0 read=freeze-check-absent` AND `limb R2 fixed=0 read=R47-enforced-by-not-a-file-corpus/instruments/freeze-check.py`; total fixed=3. COUPLING: R2 is not independent of R4 (see 3.6).
- final-attempt3-refiled.txt removed: `limb R5 fixed=0 read=refiled-absent`; total fixed=4.

So each limb has a same-tree red-before with its named reason, except the coupling noted. The S070 correction's own falsity has no red-before (see 2.1).

## 2. Repairs WITHOUT a committed red-before (or whose red-before is not the same command)

2.1 S070 correction (round-44.md Correction, S070 reject reason). No committed red for the claim that the S070 reject reason was wrong. Base has no S070 capture: the only S070 evidence is row text, `corpus/SOURCES.md:76` ("the page's accessible body is a JavaScript shell") and `corpus/lessons/round-44.md:131` (same). Nothing in `.ufo/waves/round-44/source-recon/` is for S070 (only S069). The S072 capture is the article API for the same URL, and its size token is consistent: `S072.json` body = 10029 chars; `corpus/source-snapshots/round-45/S072.txt` = body + "\n" (10032 bytes, 10030 chars) (checked by Python). That supports the replacement, not the falsity of the S070 reason. Live re-fetch of S070 was refused by the seat rules, so the plain-page reading cannot be re-run.
Worse, the repair violates its own rule R49 (QUALITY.md:382): R49 says a contradicted reject reason "is corrected in the registry row and in the lesson that recorded it, not left standing". At tip the S070 row still reads `REJECTED: the page's accessible body is a JavaScript shell` (SOURCES.md:76) and lesson line 131 is unchanged with only an appended correction. The counter enforces this: `limb_r1` returns `S070-row-changed-or-baseline-absent` if the S070 row changes, so the rule-mandated correction is blocked by the predicate.
Receipt that would supply a red-before: a pinned, sha256-bound plain fetch of `https://bughunters.google.com/about/rules/about-this-section` (the shell or not), plus a counter predicate that allows the S070 row to be corrected.

2.2 r44-frontier-count.py selftest. Red at base is real but for the wrong reason to be a selftest red. Base, with the flag (`--root base --selftest`):
```
r44-frontier-count.py: error: unrecognized arguments: --selftest
[exit=2]
```
Bare `--selftest` gives `error: the following arguments are required: --root` (exit 2). Tip: `selftest cases=43 failures=0`, `mutants=10 rejected=10`, exit 0. The diff is not a selftest-only delta: it also adds `--ids`, a `count_lines` seam and an `evaluate()` split (base `count_frontier` body moved). The "fix as only delta" condition therefore fails; a receipt with the selftest-only change is missing.

2.3 freeze-check.py. The tool file is absent at base, so its own red is `exit 2`-type noise. The committed-bytes red for the motivating defect is not a file: I replayed the round-44 frozen grep verbatim through freeze-check against base:
```
grep at base: 0
claim C2 base_read=0 verdict=FAIL
finding C2 FC-NO-MATCH no output line equals expect_before '25'; rc=1
freeze-check claims=1 base_ok=0 exit=1
```
This is a valid red, but I could not find it as a committed receipt; `round-44/claims.json` is schema v1 with no counter_cmd (replay gives FC-SCHEMA/FC-MISSING-FIELD, not the grep). Also the selftest's real-README case depends on the host, not on the export: `freeze-check.py` line 47 `PURE_DEFAULT = "/fast/scratch/hyaku/kasegi-r45/L1/pure"` (another lane's scratch) and a git lookup. With PURE_DEFAULT pointed at a missing path (run on a copy in scratch) the same selftest prints `case 2-round44-frozen-grep-real-readme FAIL real base README not found` and `selftest cases=20 failures=1`. So the R4 green (selftest cases=20 failures=0) depends on an out-of-repo path. Round-45 claims replay at base is genuinely red→ok: `claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok`, `claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok`, `freeze-check claims=2 base_ok=2 exit=0`.
Receipt needed: a v2 claims file carrying the verbatim round-44 counter, replayed and committed under controls, plus a selftest case that does not read outside the export.

2.4 R47-R49 (QUALITY.md rows 380-382). The R2 limb gives a red at base and a green at tip, but it is presence-level, not content-level. Falsifier: I appended to base QUALITY.md a `## Round-45 additions` heading and three rows R47/R48/R49 made only of the keywords (`do-nothing before data presence-only capture method reject.` repeated to 479 chars), with `enforced-by: \`corpus/instruments/README.md\`` and ground `corpus/lessons/round-44.md:16`. Result:
```
limb R2 fixed=1 read=criteria=3
```
Also R49's enforcer is `corpus/instruments/source-recheck.py` (QUALITY.md:382). That file has no capture-method or reject-reason rule (grep for "capture method"/"capture-method" across corpus/instruments matches only r45-routed-defects.py). The counter checks only that the enforced-by path is a file. So R49 has a red→green pair that does not test R49.
Receipt needed: a committed fixture where the named enforcer exists but lacks the rule, expected to print a red R2 for that row.

2.5 C2 census gate G7 (`sources-census.sh validate`). No red-before. At base it is already green: `gate G7 pass=1 read=census-rc=0 ok-line=1` and `.ufo/waves/round-45/controls/sources-census-before.txt` ends `exit=0`. The frozen before value `c2-gate fixed=1/7` counts G7. G7 also stays green on each C2 reversal (section 3.2). G7 runs the fleet-root script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`r45-c2-gate.py:56`), which is not in the export.
Receipt needed: a census run on a fixture SOURCES.md with a malformed S071 row that must exit non-zero at base-plus-S071, or G7 dropped from the 7/7 denominator.

2.6 PROVINCE.md r45 line and corpus/README.md "Round-45 admission" block ("27/27 admitted"). No grader reads them. Their only committed evidence is the base absence (`grep` for F27 finds nothing), which is presence-only and forbidden by QUALITY R48.
Receipt needed: a consistency check that reads the README F27 row and the PROVINCE amendment's count, red at base and green at tip.

2.7 The counter selftests are referenced but not landed. SKILL.md round-45 rows (r45-routed-defects.py, r45-c2-gate.py) and corpus/instruments/README.md cite `corpus/instruments/r45-counters-selftest-c1.py` and `-c2.py`. `find tip -name 'r45-counters-selftest*'` finds only `.ufo/waves/round-45/wave1/R45ExecSelftestC{1,2}.draft/`. I ran the wave-1 drafts against the v1.1 counters (HYAKU_SCRATCH redirected into my scratch):
- C2 draft: `selftest cases=51 failures=4`. The unmutated control reads `FAIL control C0 unmutated tree: fixed=5/7 gates=1011101` (G2 `sections=0/4`, G6 `base-names-intact=0`); C1 and C2 controls fail the same way; M13 fails. The do-nothing control gives `selftest cases=51 failures=48`. So the draft is stale against v1.1 and has no passing positive control.
- C1 draft: `case control-good-tree total_fixed=1 verdict=FAIL expect fixed=5 R1=0 R2=0 R3=0 R4=0 R5=1`. Its GOOD tree reads R2 `R47-criterion-too-short`, R3 `r44-frontier-count-not-the-pinned-bytes`, R4 `freeze-check-not-the-pinned-bytes` (the draft uses its own minimal freeze-check, which the pinned sha forbids). The draft cannot produce a green control.
Receipt needed: landed r45-counters-selftest-c{1,2}.py that pass their positive control on v1.1 and whose do-nothing control fails the mutants, committed under controls.

## 3. Covered with caveats

3.1 r45-c2-gate.py, reverse-one per C2 piece (tip minus piece):
- README at base: G1,G2,G3(`bad=used-by`),G5,G6 red; fixed=2/7.
- SOURCES at base: G3 red (`row-S071=absent-or-malformed`); fixed=6/7.
- knowledge entry removed: G1,G2,G5 red (`F27-entry-not-a-regular-file`), G6, G7 red; fixed=1/7.
- manifest removed: G4 red (`manifest-absent`); fixed=6/7.
- S071.txt removed: G3,G4,G5 red; fixed=4/7.
Base do-nothing: `c2-gate fixed=1/7 exit=1` (G7 only). Tip: `c2-gate fixed=7/7 exit=0`.

3.2 (see 2.5) G7 does not respond to SOURCES, README, manifest or snapshot reversal; it only responds to the knowledge entry.

3.3 r44-frontier-count "--expect 27" secondary at base reads `frontier rows=26 admitted=26` and exit 0 at `--expect 26`. Tip `--root tip --expect 27 --ids` reads `frontier rows=27 admitted=27`, exit 0. Consistent with the claims' before value.

3.4 R5 refiled receipt. The red-before is real: the original `final-attempt3.txt` line after the bare call is `exit=0` while the command exits 2. I re-ran at the round-44 tip `c950fa3` (archive into scratch): `r44-routed-defects.py --selftest` with no --root exits 2 (argparse), and `--root c950 --selftest --work W` prints 21 lines that equal the refiled body byte-for-byte (diff empty; body sha256 `03fe3af5…226c0`, matching the PIN). So the R5 pin is a genuine run, at c950fa3.
But the SAME command at the round-45 tree is red, at base and at tip alike:
```
selftest case=POSITIVE verdict=fail fixed=7 unresolved=1
selftest cases=20 failures=1
exit=1
```
So R5 has no same-tree red→green pair: its green is a pinned transcript of another tree, and the counter (`limb_r5`) cannot detect that. SKILL.md's r44-routed-defects row discloses the drift, but R5 still reads `fixed=1`.
Receipt needed: a same-tree rerun at the graded tree; if it is red, R5 must stay unresolved and the receipt must say so.

3.5 Pins. All five PIN digests in `r45-routed-defects.py` match the committed bytes (S072.txt, freeze-check.py, r44-frontier-count.py, r44-routed-defects.py, claims.json).

3.6 Coupling. R2 depends on R4's artifact (QUALITY R47 `enforced-by` is `freeze-check.py`). Removing only R4 also flips R2 (section 1), so the 5 limbs are not independent and the total is not a sum of 5 independent repairs.

## 4. Other observations (outside the assigned repairs, recorded for the L1)

- `git archive` of the lane commit contains changed copies of instruments under `.ufo/waves/round-31/wave1/ExecCensusDry/validate/*/corpus/instruments/` (README.md, knowledge-expected.txt, r44-frontier-count.py, plus new freeze-check.py, r45-*.py). A closed round's wave artifacts were modified or added by the integration commit (`diff -rq base tip`).
- The r44-routed-defects selftest is red at both base and tip (`POSITIVE verdict=fail`, `failures=1`), so "selftest passes" claims that cite it are historical (c950fa3) only.

## 5. Limitations

- Live fetches (S070, S072, docs.kernel.org) were refused by the seat rules; S070's falsity cannot be re-tested here.
- G7 and the census depend on the fleet-root script, outside the export; I ran them on the host as the counters do.
- freeze-check selftest case 2 read `/fast/scratch/hyaku/kasegi-r45/L1/pure` (another lane's scratch, present on this host). I only read it.
- The C1 and C2 selftest drafts were run as read-only probes with HYAKU_SCRATCH redirected into my scratch; no lane file was written.
- I did not run the freeze controls (`freeze-controls-v1.1.txt`) on new trees; I read the recorded output only.
- Scratch was removed on exit.

Ask of the L1 (concise): (1) land counter selftests or drop the references; (2) correct S070 row and lesson line 131 per R49 and let the counter accept that; (3) add same-tree red for R5 or mark R5 unresolved; (4) make R2 content-level or stop claiming R47-R49 are graded; (5) give G7 a red fixture or remove it from 7/7; (6) make freeze-check selftest case 2 read only committed bytes.
