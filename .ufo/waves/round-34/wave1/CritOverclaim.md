# CritOverclaim — overclaim audit of C1/C2 after-values (round 34)

Seat: critic, leaf of the round-34 L2 wave. Write scope used: this receipt only. No lane
file edited, no git/jj mutation, no subagent, no `agent://all`, nothing written outside the
lane; scratch under `/fast/scratch/hyaku/kasegi-r34/CritOverclaim/` (removed before yield).

Mandate: every C1/C2 after-value must have a measured command output; no universal clause
beyond what the counting command enumerates; no "verifies" claim without a receipt; the
report/lesson must not overstate mutant kills or closure counts. Evidence = my own runs
against the working copy at HEAD `206e5108f1190e61b3e2622d21cab8a5d921650c` plus the
wave-1 receipts named below.

## Report

### 1. Pinned measurement batch (digests identical before and after the batch)

```
$ sha256sum corpus/instruments/{kill-rule-check.py,r-defect-closure.sh,capture-binding-check.py}
7a20e724659ffa35ccce2f5072232c409e7b79d2e33fda878b5589c989d697f1  kill-rule-check.py
0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1  r-defect-closure.sh
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  capture-binding-check.py
PRE == POST  -> STABLE True
```

| command | measured output (tail) | exit |
|---|---|---|
| `python3 corpus/instruments/kill-rule-check.py` | `mutants=3 killed=3 survivors=0 invalid=0` / `gates=6 failed=0` / `survivors=0` | 0 |
| `bash corpus/instruments/r-defect-closure.sh` | nine `R1..R9 … open=0` lines / `closed=9/9 exit=0` | 0 |
| `bash corpus/instruments/r-defect-closure.sh --selftest` | nine `selftest case=R* live=pass fixture=rejected verdict=pass` / `selftest cases=9 failures=0` | 0 |
| `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=23 failures=0` (23 verdict lines, all `verdict=pass`) | 0 |
| `python3 corpus/instruments/capture-binding-check.py` | `records=41 bound=41 unbound=0`; `AUDIT records=41 … multi_row_url=2 orphans=1 orphan=S040-live.txt` | 0 |

Base-tree direction (git-archive of the lane base `014ee2d`, no worktree added):

```
$ git archive 014ee2d | tar -x -C $S/base          # 6815 files
$ bash corpus/instruments/r-defect-closure.sh --root $S/base
R1 … lane-hash-markers=2 open=1 … R9 … open=1
closed=0/9 exit=1                                   # exit=1
$ python3 $S/base/corpus/instruments/capture-binding-check.py --selftest
selftest cases=11 failures=0                        # exit=0  (claim's before-value)
```

C2 counters and gates, measured at the same state:

```
grep -cE '^\| F[0-9]+ \|' corpus/README.md                                  -> 17
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 51
grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md              -> 1   (tier A | status mined | opened 2026-10-26 | recheck 90d)
grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l                     -> 1
ls corpus/knowledge/*.md | wc -l                                            -> 46
python3 corpus/instruments/frontier-recheck-count.py                        -> entries=20 pass=20 exit=0
  PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051   exit=0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
  S051:sha256 OK ; Q1..Q18 OK ; Q9 occurrences=2 anchor=77-ok ; Q17 occurrences=2 anchor=96-ok
  exit=0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … kasegi
  W04 S028 … / W04 S029 … / kasegi ok …                exit=0
grep -c '<LANE_HASH>' SCORECARD.md                                          -> 0
```

Cross-checks that hold: round-32 manifest both `fetched_utc` strict `…Z`
(`S049 2026-10-26T04:16:06Z`, `S050 2026-10-26T04:16:16Z`); round-26 manifest carries
`orphans[0] = S040-live.txt` with `sha256 b7f7b55f…e286c` **equal to the file on disk** and
`fetched_utc 2026-10-25T12:34:27Z`; S041 record sha `e18acbf9…ab47` equal to the file;
round-34 record sha `4fd8ed98…25a5` equal to `S051.txt`; `QUALITY.md:220-222` (R20 note),
`:226` (R22), `:227` (R23), `:228` (R24); `lessons/round-33.md:140` (R7 erratum) and `:215`
(R4 erratum), both after the anchor `:136`; `SCORECARD.md:1116-1119` correction naming
`7963976e60b2…` and `014ee2d7aa8c…`.

### 2. Findings — overclaims / unmeasured values

**F1 (C2, high) — the junk-twin rejection limb is false as frozen; the twin passes its own
recheck at tip.** `claims.json:58` kill rule: "junk twin passes source-recheck or is
admitted" kills C2; `:84` after: "junk twin rejected: source-recheck exit != 0 and
non-author reviewer REFUSE on record". Measured:

```
$ CMD=$(grep '^recheck:' .ufo/waves/round-34/c2-controls/junk-f17.md | sed 's/^recheck: //')
$ bash -c "$CMD"; echo exit=$?          -> junk_recheck_exit=0
$ (same extraction on corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md)
                                        -> real_recheck_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-34/c2-controls/junk-f17.md --source S051
manifest UNAVAILABLE reason=unreadable-or-invalid    exit=2
$ grep -c 'five severity levels for smart-contract exploits' corpus/source-snapshots/round-34/S051.txt
0   grep_exit=1
```

The twin's `recheck:` line is byte-identical to the real entry's, so at tip **both exit 0**;
`source-recheck` never accepts a markdown file, so `exit != 0` on the twin is an artefact of
handing it a non-manifest (any file yields exit 2 — non-discriminating), and the `:75` before
value "source-recheck on it fails (exit 2)" proves nothing. No reviewer REFUSE for
`junk-f17.md` exists in `wave1/` at read time (`grep -rn 'REFUSE' .ufo/waves/round-34/wave1/`
→ only `ExecHarnessAfter.md:204` and `RevC2BeforeAfter.md:130,132`, both `PENDING-AFTER-BATTERY`
prose). Two peer receipts already say so: `wave1/ExecHarnessAfter.md:188-206` ("the rejection
lives in the reviewer, not in this counter") and `wave1/ScoutDatawalk.md:45` ("junk-twin
rejection has no executable form as phrased"). Smallest safe correction: appended erratum
re-specifying the limb to what is measured — (i) `grep -c '<fabricated quote>' S051.txt` = 0,
(ii) `grep -c 'junk-f17' corpus/README.md` = 0 (no row admits it) — and withdrawing the
`source-recheck` clause; the harness limb must not be presented as a body-content gate.

**F1b (C2, high) — the junk twin is a mixed control: one of its two "fabricated" quotes is
true, so no single rejection cause can be attributed to it.** Measured:

```
$ grep -c 'Direct theft of any user funds' corpus/source-snapshots/round-34/S051.txt   -> 1
$ sed -n '75p' corpus/source-snapshots/round-34/S051.txt
- Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield
$ grep -c 'five severity levels' corpus/source-snapshots/round-34/S051.txt             -> 0
$ sed -n '15,17p' .ufo/waves/round-34/c2-controls/junk-f17.md
Immunefi's VSCS v2.2 defines five severity levels for smart-contract exploits;
Critical includes "Direct theft of any user funds".
[FABRICATED — no capture holds this quote; the admission gate must reject this entry]
```

`c2-controls/junk-f17.md:16` is a true substring of the capture, yet `:17` labels the block
"[FABRICATED — no capture holds this quote]": the twin's own label is false for one of its two
sentences and its sha is pinned as the control (`2752a994…4026`). Only `:15` is absent from
the capture. So (i) both rejection limbs in `claims.json:58,84` are under-specified — they do
not say *which* string is fabricated — and (ii) a reviewer limb implemented as "grep each
quoted string" passes `:16` and rejects only `:15`, i.e. the recorded rejection would not
establish what the claim says it establishes. Smallest safe correction: the erratum names the
absent string (`five severity levels for smart-contract exploits`, grep 0) as the rejection
target and records that the twin's `:16`/`:17` pair is internally inconsistent (fix the
control's label or drop that line before citing it as a control again). Independently
observed by `wave1/ScoutDatawalk.md:46`, which does not change the measurement above.

**F2 (C2, medium) — universal clause "every assertion occurrences=1" is false.**
`claims.json:57` (predicate), `:65` (counting command "all occurrences=1"), `:81` (after
"every assertion occurrences=1"). Measured: 16 assertions print `occurrences=1`; **Q9 prints
`occurrences=2 anchor=77-ok`** and **Q17 prints `occurrences=2 anchor=96-ok`**. The receipts
are already honest (`wave1/RevC2BeforeAfter.md:95` "except Q9 and Q17 which print
`occurrences=2`"; `wave1/ScribeEntryF17.md:66`), so the defect is confined to the frozen
claim text. Correction: erratum wording "each assertion `OK`, sha256 OK, exit 0; 16×
`occurrences=1`, Q9/Q17 anchor-verified `occurrences=2`" — do not let the lesson or report
repeat "every assertion occurrences=1".

**F3 (C1, medium) — the headline is time-unstable; a 9/9 quote without a digest pin is not
reproducible.** At 2026-10-26T05:38Z the same tree printed:

```
bash corpus/instruments/r-defect-closure.sh            -> closed=8/9 exit=1
   R4 check=tightened kill rule (cases>=11, one 'selftest case=' line per case) not recorded open=1
bash corpus/instruments/r-defect-closure.sh --selftest -> selftest cases=9 failures=1
   selftest case=R4 live=open fixture=rejected verdict=fail
```

and at 05:40Z it printed `closed=9/9 exit=0` / `cases=9 failures=0 exit=0`. Cause: the R4
closure depends on the prose row `QUALITY.md:228` (R24) landing, which happened between the
two runs. `kill-rule-check.py` also changed digest mid-wave (`e33a300f…` at 05:38Z →
`7a20e724…` at 05:44Z). Consequence for the L1: the integration commit must re-run all three
C1 commands **after quiescence** and quote them with the digests in §1; any 9/9 written from
a mid-wave read is unfalsifiable. (My §1 batch is pinned and stable, which is the form the
receipt should take.)

**F4 (C1/C2, medium) — the after-state is unlanded at HEAD, and an unattributed stray file
sits at the lane root.** `git show HEAD:…` counters are the *before* state: `corpus/README.md` F-rows 16,
`corpus/SOURCES.md` registry rows 50, `SCORECARD.md` `<LANE_HASH>` 2; `git ls-tree HEAD
corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py` → empty;
`git ls-tree HEAD corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` → empty.
`git status --porcelain` shows both C1 instruments untracked (`??`) and the C2 surfaces
modified. C1's predicate says "the **committed** instrument-soundness closure suite"; if the
integration commit omits either instrument (or the F17 row/entry/manifest), C1 and C2 are
unlanded no matter what these commands print in the worktree. Also `selftest-baseline.txt`
(24 lines, sha256 `ca3759d1…3a51`, untracked, lane root) is **attributed to no seat**
(`wave1/RevC2BeforeAfter.md:302` and `wave1/ScribeAssimilationGate.md:365,367` *observe* it
and say "not this seat's file" / "left unattributed"), and would be committed by a bare
`git add -A`: delete it or move it under a receipt's scratch.

**F5 (C1, medium) — the mutant population is 3 while round 33's matrix was 4; "all mutants
killed" would repeat M34-1.** `kill-rule-check.py` `MUTANTS` = `skip-selftest-summary`,
`accept-record-without-url`, `per-file-binding-removal`; measured `mutants=3 killed=3
survivors=0`. Round 33's matrix (`.ufo/waves/round-33/wave1/ExecCaptureBinding/mutants.txt`)
was four rows: `M1-accept-record-without-url`, `M2-accept-url-not-in-registry`,
`M3-skip-fetched-requirement`, `M4-skip-selftest`. **M2 and M3 are not re-run.** Compensation
measured on scratch mutants of the landed instrument (`3d9e5e0d…`): dropping the url-compare
limb → `selftest case=url-mismatch exit=0 want=1 verdict=fail`, `m2_selftest_exit=1`; dropping
the round-32 provenance limb → `selftest case=round-32-record-without-fetched_utc exit=0
want=1 verdict=fail`, `m3_selftest_exit=1`; both are therefore killed by the `selftest-shape`
probe — but that is my scratch measurement, not a matrix row. The lesson/report must write
`mutants=3 killed=3 survivors=0` and name the two un-run round-33 rows; it must not write
"all mutants killed". Related under-listing: `claims.json:41` "(skip-selftest and
accept-record-without-url mutants killed)" names 2 of the 3 killed rows.

**F6 (C1, low) — R8's fix substitutes a different measurement into `fetched_utc`.** Round-32
now reads `2026-10-26T04:16:06Z` / `…:16Z`, which are *re-open* instants measured in
`.ufo/waves/round-33/wave1/ScoutLiveDrift.md:8,10` (HTTP 200, byte-equal), not capture
instants; the capture instant is the commit author time `2026-10-25T23:14:00-03:00` = 02:14Z.
The manifest `purpose` discloses this (`wave1/ExecManifestR32Normalize.md:54`), so it is not
false provenance — but no round-34 text may present these as the time the bytes were fetched,
and the round-32 record no longer states its own capture instant. Field semantics drift, not
a numeric overclaim.

**F7 (C1, low) — the frozen counting literal `records=40` is now `41`.** `claims.json:24`;
erratum `claims-erratum-1.md` already rules on it and `corpus/instruments/README.md:753`
says "Read the pair, not the literal 40". Recorded so the lesson quotes `records=41
bound=41 unbound=0` as the after-state and `records=41 bound=40 unbound=1` (`FAIL rule=no-row
record=S051`) as the in-flight pair, not 40.

**F8 (C2, low) — R23 landed weaker than its own draft.** Draft
`wave1/ScribeQualityDraft-block.txt:17` requires the lesson to *state the proposal's
disposition* ("mined into a named path, declined, or unchanged with the reason … a proposal
left `open` through consecutive lessons with no disposition line is a cadence failure");
landed `QUALITY.md:227` requires only "citing the considerthese file and date". As landed the
criterion is satisfiable by a citation with no disposition, i.e. a silent narrowing of the
criterion the round-34 lesson will be scored against. Smallest correction: restore the draft's
disposition limb, or record the narrowing as deliberate.

**F9 (accuracy, low) — stale "11-case" descriptors of a live instrument.**
`SCORECARD.md:1101` (capability row, "run an 11-case `--selftest` (the six contract-named
cases plus five)") and `:1084` describe the round-33 state; the live instrument prints
`selftest cases=23 failures=0` and `corpus/instruments/README.md:757` already names
`selftest cases=23` as the re-verify target. Round-33 rows are history and should stay; no
round-34 sentence and no round-34 SCORECARD row may carry "11-case". Same shape for the
`SCORECARD.md:1107` round-33 move-log `records=40` / `selftest cases=11`.

**F10 (C1, low) — `--selftest` conflates closure with sensitivity, so the frozen kill-rule
clause fires on a live-tree regression.** `run_selftest` requires `live=pass` per case as well
as `fixture=rejected`; that is why F3's 05:38Z run printed `cases=9 failures=1` while the
suite's rejection power was intact. The claim's kill clause "suite --selftest prints … any
failure" therefore also fires when the corpus briefly regresses, which is the frozen text's
choice, not a defect — but the lesson should say which of the two it is testing, or a future
reader will read a live-open failure as a lost fixture.

### 2b. Clause-by-clause verdict (frozen after-values vs my measurement)

| clause (claims.json) | after-value | measured | verdict |
|---|---|---|---|
| C1 `:39` suite exists, `closed=9/9`, `--selftest cases=9 failures=0` | 9/9, 0 fail | `closed=9/9 exit=0`; `cases=9 failures=0` (pinned batch) | holds, digest-pinned (F3) |
| C1 `:40` `capture-binding --selftest` N>=19 + 9 named cases | N>=19 | `cases=23 failures=0`; all 9 names present | holds |
| C1 `:41` `kill-rule-check` survivors=0 | 0 | `mutants=3 killed=3 survivors=0` | holds; population limited (F5) |
| C1 `:42` `<LANE_HASH>` 0 + correction naming hashes | 0 | `grep -c` 0; block at `SCORECARD.md:1116-1119` | holds |
| C1 `:43` erratum 2 + pre-freeze step | present | suite R2 `open=0`; `QUALITY.md:226` (R22) | holds |
| C1 `:44` R20 per-id note | present | `QUALITY.md:220-222` | holds |
| C1 `:45` lesson R7 erratum | present | `lessons/round-33.md:140-147` | holds |
| C1 `:46` round-32 manifest strict-UTC only | 2/2 `Z` | both `…Z` | holds (semantics: F6) |
| C1 `:47` S040 record-or-orphan + purpose | present | `orphans[0]` sha == file; `orphans=1` exit 0 | holds |
| C1 `:48` rule A bidirectional | both ways | suite R9 `mirror=0 reverse=1 open=0` | holds (suite-measured) |
| C1 `:49` junk twin committed and **rejected** | rejected | committed at `29f606d`; rejection limbs unmeasured/false | **fails** (F1, F1b) |
| C2 `:78-79` frontier 17 / rows 51 / S051 1 / citing 1 | 17 / 51 / 1 / 1 | same | holds |
| C2 `:80` harness 20/20 incl. `PASS F17 … ids=S051` | 20/20 | `entries=20 pass=20 exit=0` | holds |
| C2 `:81` source-recheck exit 0 | 0 | exit 0, 18 assertions | holds |
| C2 `:81` "**every** assertion occurrences=1" | all =1 | Q9, Q17 = 2 | **fails as worded** (F2) |
| C2 `:82` census exit 0 (W04 S028/S029) | 0 | exit 0, those two W lines only | holds |
| C2 `:83` knowledge entries 46 | 46 | 46 | holds |
| C2 `:84` junk twin "source-recheck exit != 0 **and** reviewer REFUSE on record" | both | twin recheck exit 0; no REFUSE receipt | **fails** (F1, F1b) |

### 3. Scope notes (no action)

- `grep -rl '<LANE_HASH>'` repo-wide hits `corpus/lessons/round-33.md`,
  `round-33-verifier-spotcheck.md` and round-31/32/33 wave artifacts, i.e. documents that
  *quote* the token. C1's clause is correctly scoped to `SCORECARD.md` (0); a repo-wide
  "0 markers" sentence would be false.
- `corpus/instruments/__pycache__/` is covered by `.gitignore:2`.
- S051 provenance is sound: file sha `4fd8ed98…25a5` == manifest pin, `fetched_utc
  2026-10-26T05:31:10Z` == `S051.txt` mtime (`02:31:10 -0300`).
- No tools installed or upgraded this seat (only stock bash/python3/git read-only).

### 4. Scratch

`/fast/scratch/hyaku/kasegi-r34/CritOverclaim/` — base-tree archive extraction, pinned
batch output, `mut/m2.py`, `mut/m3.py`. Removed with `rm -rf` before this receipt was
finalized (`ls` after removal: absent).
