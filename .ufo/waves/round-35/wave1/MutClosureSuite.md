# MutClosureSuite — mutation test of `corpus/instruments/r35-defect-closure.sh`

Seat: MutClosureSuite (kasegi-shokunin round 35, item 40, mutation-tester; judged on
depth:verifiability, coverage). Object under test: the C1 closure suite's seven checks D1–D7.
**Verdict: 14/14 mutants killed (7 vacuous + 7 delete, one pair per check), both controls
rejected, no survivor.** No check can be made vacuous without `--selftest` failing, and no
check can be deleted without the plain run dropping below `closed=7/7`. Machine records:
`out/battery-rooted.json` and `out/live-probe.json` under my scratch root (deleted before
yield; every figure below is quoted from them or from the terminal transcript).

## Report

### 1. Object under test and settlement

The instrument was re-cut repeatedly mid-wave by its author seat (ExecClosureSuite, item 4)
while reviewers filed findings. Digests observed in order (sha256 prefix, lines, mtime where
captured):

| # | sha256 | lines | note |
|---|---|---|---|
| 1 | `bed8f654…4179c67e70` | 643 | first read this seat |
| 2 | `c748dd70…44f7a02a0` | 735 | fixture-missing/control logic appearing (mtime 03:36:57) |
| 3 | `8340f96f…149e7cd0a` | 754 | (mtime 03:37:43) |
| 4 | `5fb0da5e…ee87cdf6e731f` | 771 | fixtures landing |
| 5 | `d7ad8438…5149e7cd0a`→ see note | 773 | author's first "final" announcement; my first battery ran here |
| 6 | `8b8c2420…bc7e0db083` | — | transient, seen only in my watcher log |
| 7 | `d799c591…d47c784e7e9` | 815 | cascade-mutant re-cut |
| 8 | `a4f80067…49e7cd0a` | 834 | author's second announcement; rooted battery v1 ran here |
| 9 | `0ae4b484…fec09ae27f` | 834 | **author's FINAL announcement — the bytes tested below** |

Note: row 5's full value is `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304`.
Row 9 differs from row 8 by **one word in a header comment** (`sixteen`→`seventeen` clause-mutant
count; my own `diff` of the two trees shows exactly that one hunk at line 35), so the row-8
battery results transfer to row 9 — and the final battery below was re-run on row 9 bytes anyway.

Final object under test (author announcement: "FINAL baseline … Frozen unless a new defect is
filed"):

```
$ sha256sum corpus/instruments/r35-defect-closure.sh; wc -l corpus/instruments/r35-defect-closure.sh; bash -n corpus/instruments/r35-defect-closure.sh && echo parse-ok
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh
834 corpus/instruments/r35-defect-closure.sh
parse-ok
```

Fixtures (ExecSelftestFixtures' bytes, final; digests match the author's receipt §1):
`corpus/instruments/r35-fixtures/README.md`
`9bcb39cb5315abe0cd20f39599e03519542f4ae9936f01b4b0e0e80140b272d2`,
`corpus/instruments/r35-fixtures/fixtures.json`
`b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113`.
Do-nothing controls: `.ufo/waves/round-35/c1-controls/fake-suite.sh`
`292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121`, `before.txt`
`352d3da210283dc2d328b22ba27d9abd39eacc2f99ebcff2d4101532d582dd61`.

### 2. Mid-wave tree state and the baseline adaptation (author-endorsed)

The tasking's literal protocol ("`--selftest` must then fail", "the plain run must print
closed<7/7") presumes the claims' end state: baseline plain `closed=7/7 exit=0` and selftest
`cases=7 failures=0`. At battery time the **live lane legitimately reads**:

```
$ bash corpus/instruments/r35-defect-closure.sh; printf 'rc=%d\n' "$?"
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
rc=1
```

(D4 untracked pending the L1 commit — `git status --porcelain` shows
`?? .ufo/waves/round-34/wave1-results.json`; D6/D7 content pending sibling seats. The author's
receipt §11.1 measures the same `closed=4/7` / `failures=3` state.) A failing baseline makes a
mutant's failure unattributable — per the mutation-tester contract that is *inconclusive*, not a
kill — so the battery runs against the suite's own all-closed baseline tree instead: the
materialized `r35-fixtures/clean` fixture via the suite's **own `--root` flag**, which the suite
has honoured for both the plain run and `--selftest` since `a4f80067` and which the author froze
as the green baseline ("Green baseline via the frozen CLI (no patch):
`--root <materialized r35-fixtures/clean> --selftest` → `selftest cases=7 failures=0` …
`--root <clean>` plain → `closed=7/7 exit=0`"). **No byte of the instrument is patched**: the
pristine bytes are the object under test, unmodified. Live-lane runs are recorded as context (§7),
not as the baseline.

Baseline-tree construction (scratch only, mirroring the suite's own `materialize`):

```
$ S=/fast/scratch/hyaku/kasegi-r35/MutClosureSuite
$ for f in clean D1 D2 D3 D4 D5 D6 D7; do mkdir -p "$S/fixroots/$f"
    cp -a "$S/instruments/r35-fixtures/$f/." "$S/fixroots/$f/"
    git init -q "$S/fixroots/$f" && git -C "$S/fixroots/$f" add -A; done
$ cp -a "$S/fixroots/clean" "$S/closed-tree"
$ mkdir -p "$S/closed-tree/.ufo/waves/round-35"
$ cp -a "$S/c1-controls" "$S/closed-tree/.ufo/waves/round-35/c1-controls"
```

(`git init`/`git add -A` run strictly inside my scratch trees — the same construction the suite's
own `materialize` and D4 clause mutants use; no git/jj command touches the lane repository.)

### 3. Baseline on the pristine bytes — all green

```
$ bash $S/instruments/r35-defect-closure.sh --root $S/closed-tree ; echo rc=$?
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
rc=0
```

```
$ bash $S/instruments/r35-defect-closure.sh --root $S/closed-tree --selftest ; echo rc=$?
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
rc=0
```

Per-defect fixture roots each break exactly their own limb (baseline plain runs against them):
`D1 → placeholders=1,…,correction-c1c6a5f=0 open=1`, `D2 → erratum-row=0,erratum-mean=0,row-bytes=1 open=1`,
`D3 → registry-r-defect-closure=0,registry-kill-rule=0 open=1`, `D4 → tracked=0,provenance=0 open=1`,
`D5 → erratum-file=present,discriminating-invocation=2,per-id-occurrences=0 open=1`,
`D6 → dead-seat-sentence=1,correction-round-35=0 open=1`,
`D7 → supersedes-R22=0,supersedes-R23=0 open=1` — each `closed=6/7 exit=1`, rc=1.

### 4. Mutants and kill rules

Structural mutations built from the pristine bytes (never the lane file):

- **V\<i\> (vacuous)**: inside `check_d<i>`, the single verdict `exit 1` → `exit 0` (each check
  block contains exactly one `exit 1`; asserted, not assumed). The check then always exits 0.
- **X\<i\> (delete)**: the whole `check_d<i() { … }` definition removed (span: opening line to the
  first column-0 `}`).
- **NOOP (control)**: comment-only line inserted after the shebang — no semantic change; must trip
  nothing.
- **NC (control)**: stray `fi` inserted after `set -uo pipefail` — bash syntax error; rejected as
  an invalid mutant, never counted as a kill.

Detectors: `plain_closed` = `bash WORK --root closed-tree` (pristine: `closed=7/7 exit=0`);
`plain_fix<i>` = `bash WORK --root fixroots/D<i>` (pristine: `D<i> … open=1`, `closed=6/7`);
`selftest_green` = `bash WORK --root closed-tree --selftest` (pristine: `cases=7 failures=0`).
Kill rules: V\<i\> KILLED iff `selftest_green` exits non-zero with `selftest case=D<i> …
verdict=fail`; X\<i\> KILLED iff `plain_closed` prints `closed<7/7`.

### 5. Per-check outcomes — 14/14 KILLED

| check | clauses (mutants) | V\<i\> vacuous | X\<i\> delete |
|---|---|---|---|
| D1 | 3 | KILLED | KILLED |
| D2 | 3 | KILLED | KILLED |
| D3 | 2 | KILLED | KILLED |
| D4 | 2 | KILLED | KILLED |
| D5 | 3 | KILLED | KILLED |
| D6 | 2 | KILLED | KILLED |
| D7 | 2 | KILLED | KILLED |

Every V\<i\>: `selftest_green` rc=1 with `selftest case=D<i> live=pass fixture=pass mutants=0/N
others=6/6 verdict=fail` and summary `selftest cases=7 failures=1` — the check no longer fails on
its own broken fixture (`selftest detail=D<i> fixture reason=<payload> verdict=unexpected rc=0`),
which is precisely C1's kill-rule limb "any single D-closure check exits 0 on a tree that still
carries its defect". Secondary: `plain_fix<i>` flips `D<i>` from `open=1` (pristine) to `open=0`
(vacuous accepts the broken fixture; summary `closed=7/7 exit=0`). Every X\<i\>: `plain_closed`
rc=1 printing `D<i> check=undescribed open=1` and `closed=6/7 exit=1` (the deleted check's slot
falls open; the other six stay closed). Secondary: `selftest_green` fails on case D<i>
(`live=fail` — the deleted function is `command not found`, rc 127).

Exemplar evidence, V5 (D5, 3 clause mutants incl. the author's new `cascade` probe):

```
$ bash $S/instruments/r35-defect-closure.sh --root $S/closed-tree --selftest ; echo rc=$?
selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0 verdict=unexpected rc=0
selftest case=D5 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail
selftest cases=7 failures=1 control-failures=0
selftest problem=self-report status=1
rc=1
```

Exemplar evidence, X5 (D5):

```
$ bash $S/instruments/r35-defect-closure.sh --root $S/closed-tree ; echo rc=$?
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=undescribed open=1
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
rc=1
```

V1/V2 footnote: their selftest summaries read `selftest cases=7 failures=1 control-failures=1` —
the `two-defect/D1D2` control additionally breaks when D1 or D2 goes vacuous (it can no longer
fail), which is the suite's control layer catching the same defect one more way. V3–V7 read
`control-failures=0` (the two-defect control does not involve those checks).

Mutant digests (mutated bytes; each restored to pristine after its runs, verified below):

| mutant | sha256 | verdict | restored |
|---|---|---|---|
| V1 | `18b07abcf1fdfce561172b9ac340269febf55f58a18d36548a535010f4dc13ef` | KILLED | yes |
| X1 | `f81bb66b2ad3875fbe7d49ccd0d80be23dd643671f1faa763e5927b656485dd2` | KILLED | yes |
| V2 | `5d1cc90ba64a7cd40306e33dab67051c30cb8abfa9682f31fc22afb798bc0553` | KILLED | yes |
| X2 | `9c5098f0ace523df23c58f3cb73bd702d8bdb645d0333fefad25df806499c3db` | KILLED | yes |
| V3 | `1a84b8aaee11d930fc585e7eb104cb8d4295036608a5586483ca19dbbdf1fca4` | KILLED | yes |
| X3 | `650915d7a433b2e447a20876953bbb63095e3ea9c5bba7d255b754010eaae22e` | KILLED | yes |
| V4 | `6d214d4373b71da24b311dac238278ad7a5528914d18030982bbec60741230d4` | KILLED | yes |
| X4 | `94494e1709ce7743c809a65e078797941e483d46e4455739100e0e9fa8ab2afc` | KILLED | yes |
| V5 | `6268585e6b1a40b3338097f080ded64cf3b4f72df0bfa33ff36331ecf3b8aab4` | KILLED | yes |
| X5 | `bf1449361bb6ef5bf6676f7e07d27bf18b6ecbeb99bd56255818125d51b442b8` | KILLED | yes |
| V6 | `dc08506e9bd40b7c79fc30db46c07498f2d2ccbf6f06fe3734321f87bfaa9b40` | KILLED | yes |
| X6 | `a716876f7856d1574b6778821ea62547f0dd3f14b9dd6be841c9a795027308af` | KILLED | yes |
| V7 | `0721a9ba9e2f19468f52d7ba981d6753ab5cea235cab98b97a7cc402defd3976` | KILLED | yes |
| X7 | `9cba9b2ffaa00cdba9743e503c0301184d428a8d24d179241872fb16a31e4fa8` | KILLED | yes |
| NOOP | `746530b7ebabf247cc3114bacb5d3b335c86e25e5e165caa56496a2b00a89f74` | REJECTED-AS-MUTANT | yes |
| NC | `3b3d2887945c5d399dc4f6a597a280b37480428b1b814093de1eaf6cdaebcbb2` | REJECTED-AS-MUTANT | yes |

### 6. Controls — both rejected

- **NOOP** (comment-only): `plain_closed` rc=0 `closed=7/7 exit=0`; `selftest_green` rc=0
  `selftest cases=7 failures=0`. Neither detector fires — no false positive. REJECTED-AS-MUTANT.
- **NC** (stray `fi`): `bash -n` rc=2, stderr `…line 108: syntax error near unexpected token \`fi'`;
  plain run rc=2 with empty stdout (no `closed=` line — no report to misread). REJECTED-AS-MUTANT
  (invalid mutant; never counted as a kill).

### 7. Live-lane supplementary probe (context, mid-wave tree)

The same 14 mutants run against the live lane root (the instrument's own hardcoded `LANE_ROOT`,
no `--root`), where the per-check line flip is the signal. In the current tree D1/D2/D3/D5 read
closed and D4/D6/D7 read open, so exactly half the mutant-check pairs can signal:

| mutant | live plain result | signal |
|---|---|---|
| X1 | `closed=3/7 exit=1`, `D1 check=undescribed open=1` (was open=0) | SIGNAL |
| X2 | `closed=3/7 exit=1`, `D2 check=undescribed open=1` | SIGNAL |
| X3 | `closed=3/7 exit=1`, `D3 check=undescribed open=1` | SIGNAL |
| X5 | `closed=3/7 exit=1`, `D5 check=undescribed open=1` | SIGNAL |
| X4/X6/X7 | `closed=4/7 exit=1` (check already open; deletion invisible to the count) | no-signal-possible |
| V4 | `closed=5/7 exit=1`, `D4 check=tracked=0,provenance=1 open=0` (was open=1) | SIGNAL |
| V6 | `closed=5/7 exit=1`, `D6 check=dead-seat-sentence=1,correction-round-35=0 open=0` | SIGNAL |
| V7 | `closed=5/7 exit=1`, `D7 check=supersedes-R22=0,supersedes-R23=0 open=0` | SIGNAL |
| V1/V2/V3/V5 | `closed=4/7 exit=1` (check already closed; vacuity invisible to the count) | no-signal-possible |

Note the vacuous checks on open limbs **lie in their own payload**: `D4
check=tracked=0,provenance=1 open=0` — the payload still shows the open clause while `open=0`
claims it closed. That is why the kill rule needs the selftest (fixture limb), not just the plain
count. The seven no-signal pairs are structurally incapable of a live-root signal in this tree
state and are fully covered by the rooted battery (§5).

### 8. Restoration and integrity

- After **every** mutant run the working copy was rewritten with the pristine bytes and its
  sha256 re-verified: `restored=True` for all 16 entries (§5 table).
- Lane instrument sha256 before the battery == after:
  `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` — the lane file was never
  written by this seat (all mutants lived in scratch copies).
- Input digests at seat start vs at receipt time (drift is sibling landing activity, none of it
  mine): `SCORECARD.md` `51337bf1…` unchanged; `SKILL.md` `0cc95638…` → `daeff71b…` (D3 content
  landed mid-wave); `.ufo/waves/round-34/wave1-results.json` `3afa3581…` unchanged (still
  untracked); `…provenance.md` `e1c44301…` unchanged; `claims-erratum-d5.md` absent → `2f4fae0a…`
  → `eee0bb57…` (D5 content landed and iterated); `L1Integration.md` `5472f60a…` unchanged (D6
  still open); `corpus/QUALITY.md` `807cc714…` unchanged (D7 still open).
- The battery is internally consistent despite that drift: its baseline and all mutant runs
  executed with `lane_instr_unchanged_during_battery=True`, and the rooted detectors read the
  frozen baseline tree, not the moving lane.

### 9. Findings for the L1

1. **Detection power confirmed at the check level.** The suite's seven checks are neither vacuous
   nor deletable: every vacuous mutant is caught by `--selftest` (fixture limb + `report_ok`'s
   `fixture=rejected` case-line demand), every deletion by the plain run (`closed=6/7 exit=1`).
   This complements the suite's own clause-level selftest (17 clause mutants, incl. the D5
   `cascade` probe) — my mutants attack the check functions themselves, one layer above.
2. **Version churn is a coordination hazard, resolved.** The instrument moved through 9 digests
   during this seat; the author's receipt §1 named `d7ad8438…` (773 lines) which was twice
   superseded before their FINAL announcement `0ae4b484…`; `RevClosureSuite`'s review is pinned to
   `d7ad8438…` and is stale by the same token. My battery verdicts were identical on `d7ad8438…`,
   `a4f80067…` and `0ae4b484…` (the last two differ by one comment word), so the finding is robust
   across the churn — but the reviewer/author digest tables should be re-pinned to `0ae4b484…`.
3. **The faithful green live-lane pass remains gated, correctly.** `closed=7/7` on the live lane
   requires the L1 to stage/commit `.ufo/waves/round-34/wave1-results.json` (D4's counting command
   is index-based — staging suffices, per the author's receipt §11.2) and the D6/D7 content
   appends. My rooted battery covers the detection logic without waiting; ExecRegressionC1's
   quiescent-tip run covers the literal claims-verbatim protocol.
4. **No tool installed or upgraded** (pacman/uv/npm untouched; none needed), no subagents, no
   `agent://all`, no git/jj mutations against the lane (the only git invocations were
   `git init`/`git add -A`/`git ls-files` strictly inside scratch trees, mirroring the suite's own
   `materialize` semantics, plus read-only `git log`/`git status`/`git show`/`git cat-file`).

### 10. Scratch cleanup

Scratch root `/fast/scratch/hyaku/kasegi-r35/MutClosureSuite/` (instruments copy, pristine
reference, fixture roots, closed tree, out/ JSONs, driver scripts, watcher) is deleted after this
receipt was written:

```
$ S=/fast/scratch/hyaku/kasegi-r35/MutClosureSuite && rm -rf -- "$S" && ls -d "$S" 2>/dev/null; printf 'scratch-ls-rc=%d\n' "$?"
scratch-ls-rc=2
$ ls -d /tmp/r35-closure.* 2>/dev/null; printf 'tmp-check-rc=%d\n' "$?"
tmp-check-rc=2
```

`ls` exit 2 = absent; no `/tmp/r35-closure.*` residue (the suite's own selftest scratch went under
my `KASEGI_SCRATCH` and was trap-removed by the suite itself). No work tree of mine is left on
disk.
