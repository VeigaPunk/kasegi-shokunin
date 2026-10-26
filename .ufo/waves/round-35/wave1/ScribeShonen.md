# ScribeShonen — round-35 wave-1 receipt (SHONEN promotion checklist)

- Seat: `ScribeShonen` (scribe, L2 leaf; L1 = `KasegiR35`). Lane `kasegi-shokunin`, round 35, wave 1.
- Write scope used: `SHONEN.md` and this receipt only. No product file, judge, claim, SCORECARD,
  QUALITY, lesson, PROVINCE, fleet-root, sibling-lane, bounties or shokuknow write. No commit/stage/jj
  mutation. No tool installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r35/ScribeShonen/`
  created, used and removed (removal verified at every run; final `ls -d` exit 2).
- Read at: lane HEAD `5a25337` (later `bb2dc8c` landed while this receipt was being written);
  integration commits `aa6ad99` (C1 D4/D6/D7), `0aee0ef` (integration: lesson, SCORECARD stub, SHONEN,
  LOG, receipts), `8ce6fb4` (D1 wording), `5a25337` (wave leftovers). Base `3266c993…`, freeze
  `617496b9…`.

## Report

### 1. Deliverable — `SHONEN.md`

The four boxes were refreshed to round-35 evidence; every box stays `[~]` (a wave seat is the lane and
cannot write a checked box). The round-34 paragraphs are retained as history and a header line now says
which paragraphs are current.

```
$ git diff --numstat 3266c99 -- SHONEN.md
77      0       SHONEN.md
$ grep -c '\[x\]' SHONEN.md            -> 0
$ grep -c '^\- \[~\]' SHONEN.md        -> 8   (4 round-34 history + 4 round-35 current)
$ sha256sum SHONEN.md                  -> f62435940ee8b69257ab0c5ed67708d7dd238046dfe555ab9deac36e11156c44
$ wc -l SHONEN.md                      -> 159
```

Box 1 (decision tables / no-harm): `SKILL.md:1097` (`r-defect-closure.sh`) and `:1098`
(`kill-rule-check.py`) registry rows; `git diff --numstat 3266c99 -- SKILL.md` = `13 0`, digest
`daeff71b…`, 1104 lines. No-harm: `ExecNoHarmFinal` §1–§2 — base blob 201.2 / 25 blocks / 711 cites,
landed 220.9 / 26 blocks / 742 cites, `anchorcheck.py SKILL.md` exit 0 with `LOST-RECORDED=306
PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`; `RevNoHarm` §A–§C independently reproduces both
limbs. The box records that the SCORECARD integration stub (`:1269`) still says “no-harm guard mean
≈ 201.2” while the receipt-grounded guard row (`:1314`) binds base 201.2 and landed 220.9 and discloses
the stub cell as contradicted.

Box 2 (end-to-end domain task): **no new end-to-end domain task ran.** `LOG.md` has the committed
`## Round 35` heading at `:1651` but logs instruments and an admission, not a hunt-to-claim task; the
KEV capture/recheck is a measurement (`ExecC2Capture` §2/§5: `status=200`, 1,479,694 bytes / 27,870
lines, sha256 `d69349e8…`, source-recheck Q1–Q5 `occurrences=1`, exit 0; §6 CSV measured then
discarded).

Box 3 (instructions executable without oral context): F18 entry is the 47th knowledge entry
(`e9de994d…`, 91 lines) with `knowledge-expected.txt` synced (`d2e99ca6…`, 49 lines);
`recheck-audit.py` → `strict pass=47/47 …`, `expect=present expected=47 missing=0 unexpected=0 exit=0`;
`r35-defect-closure.sh` plain `closed=7/7 exit=0`, `--selftest cases=7 failures=0` exit 0.

Box 4 (no cross-domain bleed): `PROVINCE.md` 75 lines, `b4bb5fee…`, `git diff --numstat 3266c99 --
PROVINCE.md` empty; `RevNoHarm` §A PASS; `ScoutSiblingSweep` / `ConnSibling-ruling-draft` rule F18/S052
uncontested across 20 sibling lanes. The F18 frontier amendment is **owed and not applied** at this
read (`grep -c 'F18' PROVINCE.md` = 0; appended list stops at F17, `PROVINCE.md:75`).

### 2. Commands and outputs (verbatim, exit codes)

Suite plain run, this seat, tip `5a25337` (SCORECARD uncommitted at that moment):

```
$ KASEGI_SCRATCH=$S/scratch bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=4 open=0
D2 check=erratum-row=1,erratum-mean=6,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
plain_exit=0                         # output sha256 6ab64da0eef6af1fd691c52e130da1834f884a3725cffb718bc164e4a3714133
```

Suite `--selftest`, this seat, after the D1 wording fix:

```
$ KASEGI_SCRATCH=$S/scratch bash corpus/instruments/r35-defect-closure.sh --selftest
selftest case=D1..D7 live=pass fixture=rejected ... verdict=pass      # 7 such case lines (grep -c -> 7)
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
selftest_exit=0                      # output sha256 490297254ae563e75c0a021e89727b7cc8c9956bafc226270037ea49632fcdd9
```

Counter commands:

```
$ python3 corpus/instruments/recheck-audit.py ; echo exit=$?
strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=47 missing=0 unexpected=0 exit=0
exit=0                               # output sha256 4685c5e67c845a14758cd72e52dbff553028323426303672715cba12c0fe4ff0

$ python3 corpus/instruments/frontier-recheck-count.py ; echo exit=$?
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
exit=0                               # output sha256 d96f6a7b315a1efc0da6e9987ca451a8f2c20a326b5537f0aa10b0803aef3cee

$ grep -c 'filled by the L1' SCORECARD.md                       -> 0
$ grep -c 'c1c6a5f' SCORECARD.md                                -> 4
$ grep -c '201\.2' SCORECARD.md                                 -> 6
$ grep -c '220\.9' SCORECARD.md                                 -> 2
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                    -> 18
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md -> 1
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l       -> 1
$ grep -c '^## Round 35' LOG.md                                 -> 1  (heading at :1651; 1659 lines)
$ grep -c 'F18' PROVINCE.md                                     -> 0
$ git diff --numstat 3266c99 -- SKILL.md PROVINCE.md corpus/QUALITY.md SCORECARD.md
13      0       SKILL.md
54      15      SCORECARD.md
21      0       corpus/QUALITY.md
                                    # PROVINCE.md absent = empty diff
```

### 3. Findings for the L1

- **F1 — live D1 regression inside round 35, reported and repaired (no credit to this seat).** The
  round-35 SCORECARD append carried by `0aee0ef` reintroduced the D1 placeholder literal at
  `SCORECARD.md:1271` (“…final lane commit filled by the L1 in the closing commit.”). On those bytes
  `grep -c 'filled by the L1' SCORECARD.md` = 1 and this seat's suite run read
  `D1 check=placeholders=1,…, open=1` → `closed=6/7 exit=1`, i.e. the committed integration broke the
  frozen C1 marker clause. This seat messaged `ExecD1Markers`; the line was reworded in `8ce6fb4` and
  the post-fix runs above are `closed=7/7 exit=0` and `cases=7 failures=0`. `ExecD1Markers`’ returned
  task result confirms it did not write the repair (its edit was rejected on changed bytes) and
  independently escalated the density cell.
- **F2 — stale density cell in the integration stub, disclosed not deleted.** `SCORECARD.md:1269`
  still reads “no-harm guard mean ≈ 201.2” against the landed `SKILL.md` (measured 220.9 by
  `ExecNoHarmFinal`). The receipt-grounded section at `:1286ff` restates it in the guard row (`:1314`:
  base 201.2 / landed 220.9) and explicitly calls the stub cell contradicted; the closing commit is the
  reconciliation point. Not a suite kill (D2 reads erratum presence), but the stub is the sort of
  stale-prose row D2 was filed for.
- **F3 — stale “final lane commit” label.** The same stub line labels `0aee0ef…` as the final lane
  commit although later commits exist (`8ce6fb4`, `5a25337`, `bb2dc8c`). It is now worded
  “`0aee0ef…` (recorded in the closing commit)”, which is still ambiguous; the L1 should make the
  closing commit name the true tip.
- **F4 — box 2 stays open by fact.** No new end-to-end domain task ran this round; the KEV capture is
  a measurement (see §1). Nothing in this seat’s work changes that.
- **F5 — required artifacts were untracked mid-wave and are now tracked.** At ~06:50Z this seat’s
  `git status` showed `corpus/source-snapshots/round-35/S052.txt`,
  `.ufo/waves/round-35/c1-controls/fake-suite.sh` and `c2-controls/junk-f18.md` untracked and
  `SKILL.md` modified (registry append). `5a25337` committed them; verified with
  `git ls-files corpus/source-snapshots/round-35/S052.txt .ufo/waves/round-35/c1-controls/fake-suite.sh
  .ufo/waves/round-35/c2-controls/junk-f18.md` → all three listed, exit 0. No action outstanding.

### 4. Limits

- The tree moved under this seat (SCORECARD changed once mid-measurement: `085cffd6…`/1282 lines →
  `5ea6f459…`/1404 lines). Every count above is bound to the named bytes/time; later peer writes are
  not measured here.
- This receipt does not judge the round, does not re-run the wave, and makes no score claim. It reports
  observed state for the L1’s integration decision.
- No subagent, wave dispatch or broadcast was used; only `ExecD1Markers` was messaged (the D1 finding).

### 5. Digests read at this seat’s measurement

```
f62435940ee8b69257ab0c5ed67708d7dd238046dfe555ab9deac36e11156c44  SHONEN.md (159 lines)
5ea6f4593ee909be06944d8cbfb58a91220ca5edf6ec0c265ed652630e8293a9  SCORECARD.md (1404 lines)
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md (1104 lines)
a576d58c347300b7d4517515397ae7bb541d87fbc837139b22b8612280885200  LOG.md (1659 lines)
b4bb5fee0a37cb2a81e351ee837a3e23fc64fbe002dfb25e4688d0ed4782ff91  PROVINCE.md (75 lines)
d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69  corpus/QUALITY.md (250 lines)
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md (396 lines)
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md (112 lines)
e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761  corpus/knowledge/cisa-kev-catalog.md (91 lines)
d2e99ca60bc5acf109a60a26452379bc8d428ea0cb382f1e513696a7873347a8  corpus/instruments/knowledge-expected.txt (49 lines)
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh (834 lines)
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt (1479694 B, 27870 lines)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json (5631 B)
```

### 6. Addendum — post-receipt commit movements

- `SHONEN.md` as refreshed by this seat was committed by the L1 in `48e6053` (“round-35: scorecard +
  SHONEN late seat appends”; the commit’s `SHONEN.md` blob is `f6243594…`, 159 lines). One post-commit
  correction rebinds the measurement-state digest to the SCORECARD blob that commit actually carries:
  working `SHONEN.md` is now `90385026eda9d4495ca6fe046b03c462c41c6a502ba26661d3d4bf11eab0a98b`
  (160 lines; `git diff --numstat HEAD -- SHONEN.md` = `3 2`), pending the L1’s next commit.
- SCORECARD committed blob at `48e6053`: `ed6e931f…`, 1404 lines; the `:1269` stub cell and the
  `:1314` guard row are unchanged by that commit. `grep -c 'filled by the L1' SCORECARD.md` = 0 on the
  committed tree.
- `PROVINCE.md` remains unamended (`grep -c 'F18' PROVINCE.md` = 0) and undiffed vs base at this read;
  the F18 frontier append is still owed (box 4 in §1 above).
- Receipt digest: `8289f790c46eee48087b9ab623c9a2799fbd7570c284d047eff8cc9e07434bdd` (177 lines,
  before this addendum); the file is untracked at this read and the L1 commits it.

Report: .ufo/waves/round-35/wave1/ScribeShonen.md
