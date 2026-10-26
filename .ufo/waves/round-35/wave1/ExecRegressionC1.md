# ExecRegressionC1 — final C1 regression at quiescent tip bytes (round 35)

- seat: `ExecRegressionC1` (executor, leaf of the L2 wave; no dispatch, no subagent, no commit)
- lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (jj-colocated; no git/jj mutation run by this seat)
- lane base: `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
  `617496b9c6e92bc671e7e78b83df69a04470d0e9`
- `HEAD` at the measurement of record: `48e605332b266c59d72937deb0d85671d3944570` (`round-35: scorecard +
  SHONEN late seat appends`); round-35 wave bytes were committed by the L1 between 06:58:39Z and 07:06Z
  of this seat's run, so this receipt carries **both** the pre-integration and the final bytes
- measurement instants of record: `2026-10-26T07:05:58Z` (finalI) and `07:06:36Z` (finalJ) — the five
  counter lines are byte-identical across them (`COUNTERS_IDENTICAL`); the earlier instants are recorded
  in §0.2 as the in-flight ladder, not as the measurement of record
- **C1-input quiescence witness**: the sha256 over exactly the nine files the five commands read
  (SCORECARD.md, SOURCES.md, QUALITY.md, SKILL.md, L1Integration.md, results + provenance,
  claims-erratum-d5.md, the suite itself) is
  `c5ca9471417fa5660a461e3c7c2bc169348eb923eede183d57de5e4978fad3d4`, unchanged at `07:08:00Z` and
  `07:09:10Z` while `HEAD` advanced `48e6053 → 87f6b95` (a commit touching only
  `corpus/lessons/round-35-verifier-spotcheck.md`). Scribe prose kept landing after the wave's `complete`
  line; the C1 inputs did not move under it, and the counters did not move either.
- lane tip at the end of this seat: `87f6b95` (`round-35 verifier spot-check (integrator, hyaku): non-author
  admit/reject`); 64 of 64 seat receipt files present under `.ufo/waves/round-35/wave1/`
- corpus input digest at `07:06:36Z`: `67a280a343f4a277875f552050f4e5c1ed4a20b4be842bf47b8026880c4b8a3b`
  (`2026-10-26T07:05:58Z`, wider surface incl. the suite's non-corpus inputs:
  `b4af3080ca4b72a542c742e0a840c3825470adb9a6d53775945b5c4fca15f46f`)
- wave receipts at measurement: 62 of 64 seat files present under `.ufo/waves/round-35/wave1/`

## Report

### 0. Measurement state and quiescence

The five frozen C1 counting commands of `.ufo/waves/round-35/claims.json` → C1 `counting_commands` were
run from the lane root, verbatim, at the bytes recorded below. Two quiescence witnesses were kept: a
polling watcher over the C1 input surface (first surface `…06:49:10Z stable=120s inp=1c99fb7c…`, second
surface `…07:01:19Z…07:01:59Z inp=b10c50bd…`) and a final back-to-back re-run 38 s and again 75 s apart
whose **counter lines** diff clean.

#### 0.1 Working tree at the measurement of record

```
$ git status --porcelain=v1          # 6 paths, all scribe prose/drafts, none of them a C1 input
 M .ufo/waves/round-35/wave1/ScribeLesson.md
 M .ufo/waves/round-35/wave1/ScribeReportDraft.md
 M SHONEN.md
 M corpus/lessons/round-35.md
?? .ufo/waves/round-35/wave1/ScribeScorecard.md
?? .ufo/waves/round-35/wave1/ScribeShonen.md
$ git rev-parse HEAD
48e605332b266c59d72937deb0d85671d3944570
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l
1
```

`corpus/lessons/round-35.md` is inside the digest surface (it moved between `07:05:58Z` and `07:06:36Z`);
it is not read by any of the five commands, and the counter lines did not move with it (§1).

At the end of this seat (`07:09Z`, `HEAD 87f6b95`) the same surface carried 8 paths — the six above plus
`?? .ufo/waves/round-35/wave1/SentScopeFinal.md` and this receipt — with `git show 87f6b95:SCORECARD.md |
grep -c 'filled by the L1'` → `0`, so none of the late writes reintroduced the placeholder phrase (F2).

#### 0.2 In-flight ladder observed while the wave landed (not the measurement of record)

Every row is a real run of the same five commands; the last two rows are the record.

| instant (UTC) | HEAD | state | CMD1 | CMD2 | CMD3 | CMD4 | CMD5 |
|---|---|---|---|---|---|---|---|
| 06:49:15Z | `da2d3c6` | wave bytes, uncommitted (`inp=1c99fb7c…`) | `closed=4/7 exit=1` (D4, D6, D7 open) | `cases=7 failures=3` exit 1 | `0` | `52` | `0` |
| 06:55:53Z | `da2d3c6` | `inp=3f43cc24…`, receipts 58 | `closed=4/7 exit=1` | `cases=7 failures=3` | `0` | `52` | `0` |
| 06:57:54Z | `da2d3c6` | D6+D7 landed (`QUALITY.md` 30889→33731 B), D4 still untracked | `closed=6/7 exit=1` (D4 open) | `cases=7 failures=1` | `0` | `52` | `0` |
| 06:58:39Z | `aa6ad99` | L1 commit — `tracked=1` | — | — | — | — | `1` |
| 07:03:47Z | `5a25337` | **transient D1 reopen** (see F2) | `closed=6/7 exit=1` (`D1 …placeholders=1… open=1`) | `cases=7 failures=1` | `1` | `52` | `1` |
| 07:04:32Z | `5a25337` | settled | `closed=7/7 exit=0` | `cases=7 failures=0` | `0` | `52` | `1` |
| **07:05:58Z** | **`48e6053`** | **measurement of record** | **`closed=7/7 exit=0`** | **`cases=7 failures=0`** | **`0`** | **`52`** | **`1`** |
| **07:06:36Z** | **`48e6053`** | **re-run, counters identical** | **`closed=7/7 exit=0`** | **`cases=7 failures=0`** | **`0`** | **`52`** | **`1`** |
| 07:08:00Z | `48e6053` | C1-input sha `c5ca9471…` | `closed=7/7 exit=0` | `cases=7 failures=0` | `0` | `52` | `1` |
| 07:09:10Z | `87f6b95` | C1-input sha `c5ca9471…` (unchanged), HEAD +1 commit | `closed=7/7 exit=0` | `cases=7 failures=0` | `0` | `52` | `1` |

No receipt I read and no measured instant shows a C1 counter disagreeing with the identical command at the
same bytes; the ladder moves only on real file/commit changes. Placeholder count by commit, for the same
reason (F2): `617496b 1`, `da2d3c6 1`, `aa6ad99 1`, `0aee0ef 1`, `8ce6fb4 0`, `5a25337 0`, `bb2dc8c 0`,
`48e6053 0`, `87f6b95 0`.

#### 0.3 Digests of every file the five commands read (at the measurement of record)

```
sha256                                                            bytes   lines  path
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  35391   834    corpus/instruments/r35-defect-closure.sh
ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94  159457  1404   SCORECARD.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  65480   112    corpus/SOURCES.md
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  107906  1104   SKILL.md
d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69  33731   250    corpus/QUALITY.md
76f190a003931aee3bfbab7fec10aa657c0d64584d0cc0c7fd88b02b3679dc2d  3714    40     .ufo/waves/round-34/wave1/L1Integration.md
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  312874  397    .ufo/waves/round-34/wave1-results.json
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  5639    107    .ufo/waves/round-34/wave1-results.json.provenance.md
eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6  13086   262    .ufo/waves/round-35/claims-erratum-d5.md
```

`r35-defect-closure.sh` is `bash -n`-parseable (`bash_n_exit=0`). The round-34 instrument
`corpus/instruments/r-defect-closure.sh` is unchanged from base (`809aaf90…`, 35971 B, 832 lines) — the
round-35 suite is a separate file, as the frozen command names it.

Aggregate over exactly these nine files (`sha256sum … | sha256sum`):
`c5ca9471417fa5660a461e3c7c2bc169348eb923eede183d57de5e4978fad3d4`, re-confirmed unchanged at
`07:08:00Z` and `07:09:10Z`.

### 1. The five frozen C1 counting commands — verbatim, at the measurement of record

Run from the lane root. `CMD<n>_exit` is the command's own exit status.

```
===== [CMD1] $ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=4 open=0
D2 check=erratum-row=1,erratum-mean=6,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
CMD1_exit=0
```

```
===== [CMD2] $ bash corpus/instruments/r35-defect-closure.sh --selftest
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
CMD2_exit=0
```

(The per-defect detail lines are omitted here for length; the run printed three `selftest detail=D1/D2/D5`
lines each, two for D3/D4/D6/D7, with `mutant=<clause>` payloads that flip exactly one clause — e.g.
`selftest detail=D6 mutant=dead-seat-sentence reason=dead-seat-sentence=1,correction-round-35=1`,
`selftest detail=D7 mutant=supersedes-R22 reason=supersedes-R22=0,supersedes-R23=1`.)

```
===== [CMD3] $ grep -c 'filled by the L1' SCORECARD.md
0
CMD3_exit=1                 # grep's no-match status; the claimed quantity is the count
```

```
===== [CMD4] $ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
52
CMD4_exit=0
```

```
===== [CMD5] $ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l
1
CMD5_exit=0
```

### 2. Comparison to the frozen literals (`claims.json` → C1 `counting_commands` / `after`)

| # | frozen counting command | frozen literal | observed | verdict |
|---|---|---|---|---|
| 1 | `bash corpus/instruments/r35-defect-closure.sh` | `closed=7/7 exit=0` | `closed=7/7 exit=0`, `CMD1_exit=0`; seven `D<i> … open=0` lines | **match** |
| 2 | `bash corpus/instruments/r35-defect-closure.sh --selftest` | `cases=7 failures=0` exit 0 | `selftest cases=7 failures=0`, `complete-report accepted=1`, `CMD2_exit=0` | **match** |
| 3 | `grep -c 'filled by the L1' SCORECARD.md` | `0` | `0` (grep exit 1 = no match) | **match** |
| 4 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `52` | `52`, exit 0 | **match** |
| 5 | `git ls-files .ufo/waves/round-34/wave1-results.json \| wc -l` | `1` | `1`, exit 0 | **match** |

The predicate's parenthetical limb — "(the suite fails on the base tree, `closed=0/7`, exit 1)" — was
re-measured by extracting the lane base (`git archive 3266c993… | tar -x -C <scratch>/base`, read-only)
and copying the landed suite bytes into it:

```
$ bash corpus/instruments/r35-defect-closure.sh --root <scratch>/base
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
base_exit=1
```

All seven checks are red at base with their **own** clause payloads (not a shared failure), and all seven
are green at the tip — the suite discriminates in both directions on real bytes, not only on its fixtures.

### 3. Per-defect (D1–D7) after-item evidence, by named location

| item | frozen `after` clause | measured evidence at the record bytes | verdict |
|---|---|---|---|
| D1 | `SCORECARD.md` `filled by the L1` count 0 **with an appended correction naming `c1c6a5f`** | CMD3 = `0`; `grep -n 'c1c6a5f' SCORECARD.md` → `1130` (`…c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1)`), `1241` (`**Round-34 final lane commit: c1c6a5f…** (filled in round 35, D1)`), `1259` (the correction paragraph: "…were replaced with the round-34 final lane hash `c1c6a5f…`"), `1312` (the round-35 C1 scorecard row citing it); suite `correction-c1c6a5f=4` | **met** |
| D2 | appended round-34 `depth:density`-row erratum naming the corrected mean **201.2** | `SCORECARD.md:1246` "Erratum (round 35): the round-34 depth:density row measured 0 changed SKILL/PROVINCE lines and mean 201.7; at the tip each file had +1 appended correction line and the measured density mean is 201.2 …"; `201.2` ×6 (`1246, 1250, 1269, 1307, 1314`), `201.7` ×5, and the stale row's own opening bytes still present (`row-bytes=1`, append-only) | **met** |
| D3 | `SKILL.md` Gates & probes registry registers `r-defect-closure.sh` + `kill-rule-check.py` | `SKILL.md:1097` row `r-defect-closure.sh` + `gate\|probe` + `bash corpus/instruments/r-defect-closure.sh [--root DIR] …`, `1098` row `kill-rule-check.py` + `gate\|probe` + `cd <lane> && python3 …`; base had `grep -c 'r-defect-closure' SKILL.md` → 0 | **met** |
| D4 | `wave1-results.json` tracked **with a provenance note beside it** | `git ls-files` → `1`; `.ufo/waves/round-34/wave1-results.json.provenance.md` present (5639 B, 107 lines, `e1c44301…`), and its own text reads "**Committing this file together with this note closes D4.** … the frozen counting command that must then print `1` is `git ls-files .ufo/waves/round-34/wave1-results.json \| wc -l`". The results file is valid JSON: `seats=65`, `results=65`, keys `lane/results/round/seats/wave` | **met** (closed by the L1's commit, not by wave bytes — see F4) |
| D5 | `claims-erratum-d5.md` carries the discriminating-invocation **and** per-id occurrences statements | `.ufo/waves/round-35/claims-erratum-d5.md` present (13086 B, 262 lines, `eee0bb57…`): `:75` `## 3. Clause 1 — restated with a discriminating invocation`, `:137` `## 4. Clause 2 — why "every assertion occurrences=1" is literally false`, with the control at `:114` ("The control that makes it discriminating — the identical fixture with the quote…"); suite `discriminating-invocation=5, per-id-occurrences=5` | **met** |
| D6 | `L1Integration.md` stale dead-seat sentence corrected | `L1Integration.md` (3714 B, 40 lines, `76f190a0…`): the round-34 bullet now reads "The round-33 summary `ExecRegressionC1` filed its receipt, committed in `c1c6a5f` (round-34 closure); …" and `:34` carries "- Correction (round 35): the bullet above was corrected in place — the dead-seat claim was false; …"; suite `dead-seat-sentence=0, correction-round-35=1` | **met** (see F5 on the wording) |
| D7 | `QUALITY.md` carries appended `supersedes-R22` and `supersedes-R23` rows | `corpus/QUALITY.md:249` row `R26` = the next-score-gap criterion, whose grounded-in cell opens `supersedes R22 — R22's Grounded-in column cites M34-2, but …the correct mistake is M34-3…`; `:250` row `R27` = the reflection-cadence criterion, `supersedes R23 — R23's Grounded-in column cites considerthese/2026-10-25.md:76 … the landed grounding is the round-34 lesson's own § considerthese disposition…`; file 30889→33731 B, and the append is byte-exact: `head -c 30889` → `807cc714…` (unchanged prefix) and `tail -c 2842` → `e3aa99a1…`, the exact span/digest the draft pinned | **met** |

Non-claim frontier item in C1's neighbourhood (recorded, not scored here): `QUALITY.md` R26 is the
considerthese-proposal-2 row (`grep -cE '^\| R26 \|' corpus/QUALITY.md` → `1`), appended inside the same
2842-byte span.

### 4. Discrimination ladder — each closure proven sufficient *before* it landed

While the wave's C1 items were still open (06:34Z–06:57Z) this seat measured, on scratch copies of the
tip bytes with a throwaway `git init && git add -A` index, exactly what each missing item would do. These
runs are the reason the final 7/7 is not a surprise, and they show the checks load one defect each:

```
A. tip bytes + committed index (D6, D7 still open)                  closed=5/7 exit=1
B. A + D6 fixed (sentence rewritten in place + correction note)     closed=6/7 exit=1
C. B + the D7 draft span (2842 B, sha256 e3aa99a1…)                closed=7/7 exit=0
D. C under --selftest                                              selftest cases=7 failures=0, exit 0
E. tip bytes + committed index + an D6 **append-only** note only    D6 check=dead-seat-sentence=1,
                                                                   correction-round-35=1 open=1
                                                                   closed=5/7 exit=1
```

`C` and `D` are the exact post-commit state the L1 then landed (07:04:32Z, `bb2dc8c`/`5a25337`/`48e6053`):
the prediction and the real tree agree line for line. `E` is the measured form of finding F5.

The selftest's own fakes are also non-vacuous at the record bytes: `.ufo/waves/round-35/c1-controls/fake-suite.sh`
(361 B, `292aaac0…`) prints a claimed `cases=7 failures=0` / `closed=7/7 exit=0` while checking nothing, and
is rejected by both judges (`judge=fake-suite rejected=1`, `judge=fake-plain rejected=1`).

### 5. Cross-checks

- `RevC1BeforeAfter.md:92-93` (independent reviewer, same lane, not the author) records the same ladder:
  `closed=4/7 exit=1`, `cases=7 failures=3 control-failures=0` at 06:4xZ bytes; `:210` "`D4 check=tracked=1,
  provenance=1 open=0 ← flips exactly at commit (was tracked=0)`"; `:218` "`closed=7/7` is exactly D6 + D7
  landing plus the commit itself." No receipt I read states a C1 value that disagrees with my live runs at
  the same instant.
- `ScribeIntegrationNotes.md:47-53` predicted the same transition and warned "this entry's final C1
  sentence must quote a post-integration run"; `ScribeQualityDraft.md:15-47` is the source of the D7 span,
  with the 21-line/2842-byte/`e3aa99a1` pin that reproduces byte-exactly.
- Commit-level C1 trace: `SCORECARD.md` `filled by the L1` count by commit —
  `617496b 617…` = 1, `da2d3c6` = 1, `aa6ad99` = 1, `0aee0ef` = 1, `8ce6fb4` (`D1 closure fix — scorecard
  closing-commit wording`) = 0, `5a25337` = 0, `bb2dc8c` = 0, `48e6053` = 0.

### 6. Findings for the L1 (verdicts, not judgments of the round)

- **F1 — C1 as frozen is satisfied at the quiescent tip bytes.** All five counting commands print their
  frozen values (§2), the base-tree limb prints `closed=0/7 exit=1` (§2), `--selftest` prints
  `cases=7 failures=0` with five judge rejections, and every one of the eight `after` statements has named
  evidence (§3). The scoring decision stays with the L1; the regression result does not.
- **F2 — the D1 counter is spelling-brittle and was *transiently reopened* by a late writer.** At
  `07:03:47Z` (HEAD `5a25337`) CMD3 printed `1` and CMD1 printed `closed=6/7` with
  `D1 … placeholders=1 … open=1`, while `git show 5a25337:SCORECARD.md | grep -c 'filled by the L1'` → `0`:
  the phrase existed only in the uncommitted working copy. It was gone 45 s later. Two wave commits
  (`aa6ad99`, `0aee0ef`) also carry the placeholder phrase (count 1) and only `8ce6fb4` fixes it, i.e. the
  round-33 R1-class defect recurred *inside* the round-35 integration commits. Recommendation (not applied
  by this seat, claims are frozen): widen the D1 clause from the literal phrase to the placeholder class
  (e.g. `filled by the L1|the L1 fills this line|<LANE_HASH>`), which the suite already half-does via
  `lane-hash-markers`.
- **F3 — C1's counting list is not a complete verifier of C1's after list.** Of the eight `after` items,
  the five frozen commands exercise three (suite, selftest, placeholder) plus one C2 counter (`S`-rows =
  52, CMD4) and the D4 tracking limb (CMD5). D2, D3, D5, D6, D7 have **no independent counter** in
  `claims.json`: their only verification is the suite's own judgement. That concentration is mitigated here
  by the suite's self-report judges, the base-tree control and this seat's independent greps (§3), but the
  gap is structural (R24/R25 class: literals not jointly checked for satisfiability/coverage at freeze).
- **F4 — CMD5 and the suite's D4 `tracked` limb are index-based and therefore post-commit-only.** At every
  uncommitted instant they read `0`; they read `1` from `06:58:39Z` (`aa6ad99`). The frozen predicate's
  "quiescent tip bytes" is thus not a window in which C1 can be fully satisfied before the L1's closing
  commit — the `after` list inherits the L1's commit, not the wave's bytes. Measured supporting fact: the
  provenance note itself says so ("Committing this file together with this note closes D4"). Recommend the
  claims erratum record the measurement window ("post-commit counters") so a later verifier does not file
  this as a wave defect.
- **F5 — D6's frozen wording and D6's check agree only under the "rewritten in place **and** a note
  appended" reading.** `after` says "stale dead-seat sentence corrected by an appended note"; the check
  requires `did not file a receipt (dead seat` → 0 **and** `Correction (round 35)` ≥ 1. Measured: a pure
  append-only note leaves `dead-seat-sentence=1` → `open=1` (§4 E). The landed fix (L1Integration.md:29-35)
  is the rewrite + note, which satisfies the check. If a later re-verifier reads `after` literally as
  append-only, they will file a false defect; the erratum should state the reading.
- **F6 — D7's append is byte-reproducible and its own precondition held.** The draft pins `21 lines, 2842
  bytes, e3aa99a1…`; the landed append is exactly 2842 bytes with that sha256 after an unchanged 30889-byte
  prefix (`807cc714…`), so `QUALITY.md`'s append point was still pristine at landing time. (Caveat for a
  re-reader: extracting the draft **including** its ```markdown fences yields 25 lines/2860 B/`7981cdd8…`;
  that is a different span, not a digest mismatch. The 21-line window is lines 3–23 of the fenced region.)
- **F7 — eight paths were still uncommitted at the end of this seat** (`SHONEN.md`,
  `corpus/lessons/round-35.md`, four `wave1/*.md` drafts — 2 modified, 2 untracked — plus
  `SentScopeFinal.md` and this receipt). None of them is read by the five commands and none moved a counter
  across `07:04:32Z → 07:05:58Z → 07:06:36Z → 07:08:00Z → 07:09:10Z`, but they are the same class as the
  round-34 D4 defect ("wave writes after the `complete` line"). `HEAD 87f6b95` carries the round-35 verifier
  spot-check lesson; if the closing commit follows the remaining prose, re-run the five commands
  afterwards: `SHONEN.md`/lesson prose is inside the digest surface and a new placeholder phrase in any of
  them would reopen D1 (F2). Re-measured at `87f6b95` (§0.2, last row): all five counters unchanged.

### 7. Limits and risks (not blockers)

- **Measurement surface.** The record is the working tree at `HEAD 48e6053…` (confirmed again at `87f6b95`)
  plus the uncommitted paths of §0.1, digested in §0.3. If any digested file changes, the five commands must
  be re-run; further commits that touch only lesson/receipt prose do not change the C1 inputs
  (`c5ca9471…` unchanged across `48e6053 → 87f6b95`), and `CMD5`'s index reading must be re-checked after
  the closing commit.
- **Receipts.** 62 of 64 seat receipt files existed at the record instant and 64 of 64 at `07:09:10Z`;
  receipts are not read by any of the five commands, so their churn cannot move a C1 value.
- **Suite growth.** The round-35 suite is a new 834-line instrument; its own `--selftest` verdicts and the
  base-tree control are the only proof of non-vacuity I ran. `MutClosureSuite.md`/`RevClosureSuite.md`
  (sibling seats) cover the mutation matrix; I did not re-run their mutants.
- **Scratch instability (observed, repaired).** My scratch tree
  `/fast/scratch/hyaku/kasegi-r35/ExecRegressionC1/` was removed by another process mid-run (between
  `07:03:07Z` and `07:04Z`; the parent `kasegi-r35/` survives with three sibling seat dirs). The
  measurement of record was therefore re-taken with the command block inlined; no evidence depends on the
  deleted files, because every number in this receipt is a transcript.

### 8. Scratch and tooling

All work lived under `/fast/scratch/hyaku/kasegi-r35/ExecRegressionC1/` (watcher logs, the five-command
transcripts, the base extraction of `3266c993`, and the five discrimination trees of §4) and is removed
before this receipt is filed (`rm -rf --` of the seat dir); no lane path was written by this seat except
this receipt, and no git/jj mutation was run. No tool was installed or upgraded for this item.

Report: .ufo/waves/round-35/wave1/ExecRegressionC1.md
