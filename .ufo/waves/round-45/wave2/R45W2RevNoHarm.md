VERDICT: BROKEN

# R45W2RevNoHarm — no-harm review of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 against round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd

Method: both trees were exported with `git archive <ref> | tar -x` into scratch (base = do-nothing control, tip = attacked tree). Every instrument named in the seat spec was run on the base export and on the tip export with identical arguments, and the outputs were compared. Nothing was committed, nothing in the lane was edited, and scratch is removed on exit.

## 1. Full file-level diff (excluding `.ufo/waves`)

`git diff --name-status dc5bb8c6 6662a427 -- . ':!.ufo/waves'` prints 16 entries:

```
M PROVINCE.md                      M corpus/instruments/knowledge-expected.txt
M SKILL.md                         M corpus/instruments/r44-frontier-count.py
M corpus/QUALITY.md                A corpus/instruments/r45-c2-gate.py
M corpus/README.md                 A corpus/instruments/r45-routed-defects.py
M corpus/SOURCES.md                A corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
M corpus/instruments/README.md     M corpus/lessons/round-44.md
A corpus/instruments/freeze-check.py
A corpus/source-snapshots/round-45/{S071.txt,S072.txt,manifest.json}
```

`--numstat`: 2187 insertions, 39 deletions. **All 39 deletions are in `corpus/instruments/r44-frontier-count.py`** (deliberate replacement; see §3). Every other touched file is insertion-only.

`git diff --name-only ... -- SCORECARD.md LOG.md MANIFEST.json .ufo/state | wc -l` → `0`. SCORECARD.md, LOG.md, MANIFEST.json and `.ufo/state` are untouched. Outside `.ufo/waves` there are no `.ufo` changes. 99 files under `.ufo/waves` changed; those were excluded as instructed.

## 2. Hunk classification (production files)

`git diff -U0 dc5bb8c6 6662a427 -- <file> | grep '^@@'`, with base EOF/line counts checked by `wc -l` on the base export:

| file | hunk | base file length | class |
|---|---|---|---|
| SKILL.md | `@@ -1144,0 +1145,11` | 1144 | pure append at EOF (new "Round-45 Gates & probes registry addition" table, 6 rows) |
| PROVINCE.md | `@@ -167,0 +168,2` | 167 | pure append at EOF (r45 Frontier amendment line) |
| corpus/QUALITY.md | `@@ -372,0 +373,10` | 372 | pure append at EOF (R47-R49 block) |
| corpus/README.md | `@@ -632,0 +633,21` | 632 | pure append at EOF (Round-45 admission block; F27 row; 27/27 amendment) |
| corpus/SOURCES.md | `@@ -76,0 +77,2` | 154 | row insertion: S071, S072 directly after S070, inside the table, before the blank line |
| corpus/instruments/README.md | `@@ -993,0 +994,4` | 993 | pure append at EOF (4 registry rows, table tail) |
| corpus/instruments/knowledge-expected.txt | `@@ -36,0 +37` | 65 | sorted row insertion (`linux-kernel-…` between `japanese-severity-…` and `mission-control.md`); count 63→64 |
| corpus/lessons/round-44.md | `@@ -203,0 +204,2` | 203 | pure append at EOF (Correction (round 45)) |
| corpus/instruments/r44-frontier-count.py | 13 hunks, 39 deletions | 96 | replacement (see §3) |

**Lines REMOVED or CHANGED in the production text files:** none, apart from the r44-frontier-count.py replacement. The SOURCES.md, knowledge-expected.txt, SKILL.md, README.md, PROVINCE.md, QUALITY.md, instruments/README.md and lessons/round-44.md hunks have zero `-` lines. The new files (freeze-check.py, r45-*.py, the knowledge entry, the S071/S072 captures and manifest) are additions only.

## 3. r44-frontier-count.py replacement: byte-for-byte behaviour

Base and tip scripts were each run on the base export and on the tip export, with the same argument sets. Each pair of stdout+exit files was compared with `cmp`.

Base README (`base/corpus/README.md`), old vs new:

```
args=[]                 old: frontier rows=26 admitted=26 rc=0          new: same, rc=0   cmp IDENTICAL
args=--expect 26        old: frontier rows=26 admitted=26 rc=0          new: same, rc=0   cmp IDENTICAL
args=--expect 27        old: frontier rows=26 admitted=26 frontier expected=27 admitted=26 verdict=SHORT exit=1 rc=1   new: same   cmp IDENTICAL
args=--expect 25        old: ... expected=25 admitted=26 verdict=SHORT exit=1 rc=1      new: same   cmp IDENTICAL
args=--ids              old: frontier-ids=F01,...,F26 frontier rows=26 admitted=26 rc=0  new: same   cmp IDENTICAL
args=--ids --expect 26  old: ... rc=0                                                  new: same   cmp IDENTICAL
args=--ids --expect 27  old: ... verdict=SHORT exit=1 rc=1                             new: same   cmp IDENTICAL
```

Tip README (`tip/corpus/README.md`): old and new are byte-identical for all 7 arg sets. Output is `rows=27 admitted=27`, and `--expect 26` gives SHORT rc=1.

Edge cases, old vs new (stdout and stderr compared):

```
--root missing        old rc=2 "error: the following arguments are required: --root"   new rc=2 same message; usage line now also lists [--selftest] [--work WORK]  -> stderr DIFFERS (usage text only)
--root nonexistent    rc=2 "root ... is not a directory"                              identical
--root is a file      rc=2 "root ... is not a directory"                              identical
--root no README      rc=0 "frontier rows=0 admitted=0" + stderr "cannot read ...README.md"   identical
```

Mechanism: `count_lines` is a line-for-line reproduction of the base loop (same `ROW_RX`, same `strip().strip("|").split("|")`, same `cells[2]=="admitted"`). `evaluate` prints ids, then the duplicate-id DEFECT, then `rows/admitted`, then SHORT, in the same order as the base `main`. The only observable change is the usage text on a missing `--root`; exit code and error message stay the same.

Note (pre-existing, unchanged by the replacement and not introduced by this lane): with no `--expect`, a missing or empty README exits 0 with `rows=0 admitted=0`. Only `--expect` makes it fail.

Selftest of the new counter (`--selftest --work <scratch>`): `case ...: ok` for all cases, `mutants=10 rejected=10`, `selftest cases=43 failures=0`, rc=0.

## 4. Instrument runs, base (do-nothing control) vs tip

Instruments that are byte-identical between base and tip: anchorcheck.py, recheck-audit.py, frontier-recheck-count.py, capture-binding-check.py, density.py (`diff -q` silent). The results below therefore come from the data, not from the code.

**4a. density.py SKILL.md (depth:density).** `density.py base/SKILL.md --label base` → `mean dens 237.4`, 31 blocks. `density.py tip/SKILL.md` → `mean dens 248.4`, 32 blocks. The only changed block rows are block 31 (lines 9→10, dens unchanged at 333.3) and the new block 32 "Round-45 Gates & probes registry addition" with `dens 588.9`. 32×248.4 − 31×237.4 = 589.4, so the rise of +11.0 comes entirely from the appended registry block. The new block ranks 3rd of 32 by dens (712.5, 662.5, 588.9). That is an inflation of the density number by a dense registry table, not added depth. No harm to the axis, but the +11.0 should not be credited as depth.

**4b. anchorcheck.py SKILL.md (depth:verifiability).** `diff a-base.txt a-tip.txt` → only line 2 differs, the path label. Both print `16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, rc=0. Harm: none. Limitation: the new SKILL.md rows carry no line-range anchors, so anchorcheck does not score them.

**4c. recheck-audit.py (depth:verifiability).** Run as `cd <root> && recheck-audit.py --root $PWD --cdroot <root>`:
- Without `--cdroot` on the scratch copy: `strict pass=1/63 cdroot_fail=62` (base) and `strict pass=1/64 cdroot_fail=63` (tip). This is an export artefact: the recheck lines hard-code `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- With `--cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin`: base `strict pass=63/63 cdroot_fail=0 instrument_fail=0 own_fail=0`, `lines=63 total=63 pass=63 fail-closed=24`, `expect=present expected=63 missing=0 unexpected=0 exit=0`, rc=0. Tip `strict pass=64/64`, `lines=64 total=64 pass=64 fail-closed=24`, `expect=present expected=64 missing=0 unexpected=0 exit=0`, rc=0.
- The new entry `linux-kernel-security-bugs-reporting-process.md` line runs `source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071`: lane_exit 0, foreign_exit 0, digests equal.

Harm: none. Caveat: the audit executes each recheck line. The `cd <lane>` lines therefore run against the LIVE lane checkout, not the export. Those runs were read-only (source-recheck.py writes only in `--selftest`, `grep` of the file), and the lane's `git status --porcelain` showed 4 entries during the run, which is L1 activity.

**4d. frontier-recheck-count.py (coverage).** `FRONTIER-CENSUS rows=26 admitted=26 closed=26 problem-rows=0 registry=70` (base) → `rows=27 admitted=27 closed=27 problem-rows=0 registry=72` (tip). Diff adds `FRONTIER-PASS F27 ids=S071`. Entries 29→30, pass 29→30, exit 0 both. Coverage harm: none. This is the intended F27 admission.

**4e. capture-binding-check.py --root (depth:verifiability). HARM.**
- Base: `MANIFEST round-44 records=1 ...`; `AUDIT records=58 with_url=58 ...`; `records=58 bound=58 unbound=0`; **rc=0**.
- Tip: `MANIFEST round-45 records=2 url_bound=1 fetched=2 archival=0`; `AUDIT records=60 ...`; `FAIL rule=rejected-row-anchor record=S072 row=S072 dir=round-45`; `records=60 bound=59 unbound=1`; **rc=1**.
- Cause: `corpus/SOURCES.md` S072 row, status cell (column 8) is `rejected` (`REJECTED: the body is readable through the article API … supersedes S070`). Rule B3 in the instrument says "a row whose status cell is `rejected` cannot anchor a record". The round-45 manifest record for S072 binds to that row.
- Discrimination (one-cell mutant): copy of tip `corpus/` with only the S072 status cell changed `rejected`→`mined`. Result: `MANIFEST round-45 records=2 url_bound=2 fetched=2`, `records=60 bound=60 unbound=0`, **rc=0**. The status cell is the sole cause.
- `capture-binding-check.py --selftest --scratch <dir>`: base `selftest cases=33 failures=0 rc=0`; tip `selftest cases=33 failures=0 rc=0`. The selftest fixtures do not read the live registry, so the selftest is blind to this regression.

**4f. Frozen round-42 closure suite, J6 F-BIND (depth:verifiability). HARM.** `bash <tree>/corpus/instruments/r42-closure.sh --export-ref <ref> --lane <lane> --work … --scratch-root … --receipt-out …`
- Base (`dc5bb8c6`): `J6 payload=instrument=present,base=1,missing-path=1,url-mutated=1,digest-mutated=1,rule=reject,… closed=1`; `closed=12/13 exit=1` (J8 open at base too, `closed=0`).
- Tip (`6662a427`): `J6 payload=instrument=present,base=0,missing-path=1,url-mutated=1,digest-mutated=1,rule=reject,replay=MutBindingExistence.md=accepted closed=0`; `closed=11/13 exit=1`.
- The only closed-flag difference between base and tip is J6 (`J6 closed=1` → `J6 closed=0`). Its `base=` value is the real-tree result of the capture-binding check, which is the 4e regression.
- J8 (receipt payload-match against the committed round-42 receipt) is open in both. Its count moves from `payload-match=9/12` (base) to `8/12` (tip). I did not trace which payload moved; J3 (rows 75→81) and J7 (rows 26→27) also moved, and those movements are expected from new rows. [INFERENCE]

**4g. Other frozen gates run in the seat.** `freeze-check.py --selftest` → `selftest cases=20 failures=0`, rc=0.

## 5. Findings, by severity

1. **HARM, depth:verifiability — capture-binding-check.py goes red on the integrated tree (base rc=0, tip rc=1).** Cause: S072 row status `rejected` anchors the round-45 S072 manifest record (rule B3). Reproduced by the one-cell mutant in 4e. The frozen round-42 closure J6 limb flips closed=1→0 for the same reason (4f). The integrated tree therefore loses one closed frozen-gate limb and makes the audit red. The lane has to decide the S072 status (for example `mined`, with the "not an operative rule source" verdict moved into `teaches`), or give B3 a documented exception. This report does not choose the fix.
2. **GAP, depth:verifiability — the round-45 counter self-tests are named but not present in the corpus.** `SKILL.md:1154-1155` and `corpus/instruments/README.md:996-997` say to run `corpus/instruments/r45-counters-selftest-c1.py` and `…-c2.py` with `--selftest`. Neither file exists in the tip tree (`ls corpus/instruments | grep r45` shows only `r45-c2-gate.py`, `r45-routed-defects.py`). Copies exist only as drafts at `.ufo/waves/round-45/wave1/R45ExecSelftestC{1,2}.draft/`. Direct `--selftest` on `r45-routed-defects.py` and `r45-c2-gate.py` gives rc=2 (argparse error: required `--root`/`--baseline`). The documented self-test entry points cannot be run from the landed corpus.
3. **Note, density:** the +11.0 density gain (237.4→248.4) comes wholly from the new appended registry block (588.9). It is not depth.
4. **Note, cosmetic:** the F27 row in `corpus/README.md` writes its knowledge path as `` `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` ``. F01–F26 write it as `knowledge/…` relative to `corpus/`. Only a convention mismatch; the path resolves from the root.
5. **Clean:** SCORECARD.md, LOG.md, MANIFEST.json, `.ufo/state` untouched. All production-file hunks are appends/row insertions, except the deliberate r44-frontier-count.py replacement, which is behaviour-identical on the real README (§3). anchorcheck and freeze-check are unchanged. The frontier count moves 26→27 as intended (4d).

## 6. Limitations

- Scope: production text files and the named instruments only. The round-45 counters C1 (r45-routed-defects.py) and C2 (r45-c2-gate.py) were not graded for correctness here; other seats own those. Only the self-test entry-point absence (finding 2) and the registry claim were checked.
- recheck-audit and frontier-recheck-count run recheck lines. Lines that `cd` into the lane run against the live lane checkout, not the export (§4c). The read-only property rests on reading source-recheck.py. The lane's `git status` was not sampled before my runs, so I cannot rule out interleaving with L1 writes.
- The `--cdroot` override in §4c is my choice, to get past the export artefact. The unmodified run (cdroot_fail) is also recorded.
- The r42 closure run took >300 s. It was run in the background and read from its transcript. Only J6 and J8 were compared in detail.
- J8's move 9/12→8/12 is not traced to a payload (labelled [INFERENCE] in 4f).
- The mutant in 4e changes only the registry status cell. It shows the status cell is sufficient to flip the instrument, not that it is the only possible fix.
- Installed tools: none. Nothing was installed or upgraded.
- Scratch `$HYAKU_SCRATCH/kasegi-r45/R45W2RevNoHarm/` is removed on exit.
