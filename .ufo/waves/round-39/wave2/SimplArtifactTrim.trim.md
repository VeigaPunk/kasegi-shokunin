# Round-39 artifact trim — redundancy, supersession, and the minimal evidence set

Seat: `SimplArtifactTrim` (simplifier, wave 2 falsify). Date: 2026-10-26, snapshot
`20:21:13Z`. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD
`5006097a84305267c9a3e8c1e1d560e60fe41d37` (Y), judged head J =
`46c66c268502abd1b2c342fc71bf88ccf721845b` (Y's `export-ref`), base `480b1a50`.

**Author declaration**: this seat wrote none of the artifacts it reviews. It has no
write outside this file and its receipt. Nothing in the lane, fleet, sibling lanes or
source trees was modified; every run below is read-only, with `--work` and the export
under `/fast/scratch/hyaku/kasegi-r39/SimplArtifactTrim/`.

Axes named: **depth:verifiability** (does each retained artifact carry evidence that a
verifier can replay, and is the authority for each fact unique?) and **coverage** (can
the seven C2 counters be rebuilt from the retained set?).

---

## 1. Inventory at HEAD

`git ls-files .ufo/waves/round-39` = **262 files, 3,670,980 B** tracked; the live
directory at snapshot = **283 files, 4,065,689 B** (wave 2 was writing while this
review ran; `wave2/` held 31 entries at 20:21Z and is not yet adjudicated here).

| area | files | bytes | state |
|---|---:|---:|---|
| round root (`claims.json`, erratum, spec/dispatch/plan/results, build scripts) | 24 | 2,282,680 | tracked |
| `wave1/` (49 seat receipts + deliverables + 5 fixture packs) | 236 | 1,597,122 | tracked |
| `c1-controls/` | 1 | 1,017 | tracked |
| `c2-controls/` | 4 | 8,298 | tracked |
| `final-gates/` | 2 | 2,366 | `all-gates.txt` tracked; `reds.txt` untracked (wave-2 output, 20:18Z) |
| `wave2/` | 31 | — | in flight |
| `__pycache__/` | 2 | 74,567 | untracked byte-code |

For scale: the discriminating gate receipt is **1,765 B**; the round directory that
carries it is **4.07 MB**, of which **2.14 MB** is `wave1|2-{spec,dispatch}.json`,
`wave1|2-plan.out` and `kasegi-r39-build-results.json`, and **1.59 MB** is `wave1/`.

## 2. What makes an artifact canonical

An artifact stays in the minimal set only if at least one holds:

1. **Cited by a landed file or read by a committed instrument.** Measured: the only
   `wave1/` paths named from outside `wave1/` are
   `.ufo/waves/round-39/final-gates/all-gates.txt` (12 citations),
   `.ufo/waves/round-39/declared-blocks.txt` (5),
   `wave1/ExecSuiteBuild.md` (1, in `corpus/instruments/r39-closure.sh:66`),
   `wave1/ExecConsiderthese.scorecard.append.md` and `wave1/ExecScoreGap.gap.txt`
   (1 each, both in `corpus/knowledge/considerthese-proposals-ledger.md:81`); `wave1/note.txt` and
   `final-gates/run.txt` are fixture paths created by the suite's selftest, not files.
2. **Carries evidence the tree at HEAD cannot regenerate**: before-states, negative
   controls, time-dependent probes.
3. **Is the unique transcript of a run whose bytes are otherwise only asserted.**

## 3. Redundant, duplicated or superseded artifacts (evidence)

### T1 — byte-identical to a landed file (6 artifacts, 177,896 B)

| wave artifact | identical to | sha256 |
|---|---|---|
| `wave1/ExecSuiteBuild.r39-closure.sh` (75,170 B) | `corpus/instruments/r39-closure.sh` | `2856a210…b4222b` |
| `wave1/ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh` (73,132 B) | `corpus/instruments/r37-closure.sh` (pin `2387dcf6`) | `0da98e37…a42434d` |
| `wave1/ExecFrontierCapture.S057.txt` (17,971 B) | `corpus/source-snapshots/round-39/S057.txt` | `11c8d6d6…64f2f` |
| `wave1/ExecFrontierCapture.manifest.json` (5,488 B) | `corpus/source-snapshots/round-39/manifest.json` | `432f2205…1ce6659` |
| `wave1/ExecJunkRecheck.junk-recheck.txt` (4,924 B) | `c2-controls/junk-f22-recheck.txt` | `7d6e7df2…fcbc` |
| `wave1/ExecJunkRecheck.manifest.json` (1,211 B) | `c2-controls/junk-manifest.json` | `9dafce36…88470a` |

Command: `sha256sum` on each pair; output identical on both sides.

### T2 — append blocks now inside landed bytes (16 artifacts, 51,562 B)

Byte-containment test (`open(wave).read() in open(landed,'rb').read()`) passes for:
`ExecCorrectionsR2.{log,scorecard,shonen,round38-lesson}.append.md` ⊂ LOG / SCORECARD /
SHONEN / `corpus/lessons/round-38.md`; `ExecQualityCriteria.quality.append.md` ⊂
`corpus/QUALITY.md`; `ExecConsidertheseLedger.ledger.append.md` ⊂ ledger;
`ExecConsiderthese.scorecard.append.md` ⊂ SCORECARD; `ScribeSearchLog.searchlog.append.md`,
`ScribeRowS057.row.md`, `ScribeRowsRejected.S056/S058/S059.row.md` ⊂ `corpus/SOURCES.md`;
`ScribeFrontierF22.readme.append.md` ⊂ `corpus/README.md`;
`ScribeProvinceF22.province.append.md` and `ExecSuiteBuild.overlay/blocks/province.append.md`
⊂ `PROVINCE.md` (the latter two are byte-identical to each other, sha `bd8dbc09…dc7d`);
`ScribeEntryF22.entry.md` ⊂ `corpus/knowledge/cisa-when-to-issue-vex.md`.

**Exception — do not drop**: `ExecConsiderthese.scorecard.append.md` is contained in
`SCORECARD.md` *and* cited by the landed ledger as the byte-exact source of the block.
It is load-bearing (rule 1) and stays.

Draft superseded by a richer landed row: `wave1/ExecConsiderthese.ledger-row.md` (1,038 B,
one table row "mined round 39 … Landed as `SCORECARD.md` § Saturation addendum") is not
contained in the landed section but is superseded by it: the landed
`## Round-39 dispositions` row 1 (`corpus/knowledge/considerthese-proposals-ledger.md:81`)
carries the same status plus the correction paragraph, the criteria bar and the
`score-gap.py` measurement.

### T3 — stale declaration block (superseded, and wrong at HEAD)

`wave1/ExecSuiteBuild.overlay/blocks/declared-blocks.txt` (f982712d, 164 B) declares
`PROVINCE.md 1 bd8dbc09…` and `corpus/README.md 15 f8f01dae…`. At HEAD:

```
$ tail -n 2 PROVINCE.md | sha256sum
fa2dd99f2791e022305fe1ee759a53ba514d7d4ef2e89a597cae8a41fe70d3d7  -
$ tail -n 1 PROVINCE.md | sha256sum
bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d  -
$ tail -n 15 corpus/README.md | sha256sum
bead673d246cf88871edf6348cb1f54e17fb4665f1f37e7492ab2449894c7466  -
$ tail -n 28 corpus/README.md | sha256sum
a59d42ccaea20fc78bc2ff2a55c5fead32ac43616df8c606c51c7ac8ebec2c8f  -
```

The operative `.ufo/waves/round-39/declared-blocks.txt` (07e63e96, 164 B) declares
`PROVINCE.md 2 fa2dd99…` and `corpus/README.md 28 a59d42cc…` — both exact. The overlay
copy is a pre-integration draft: its one-line PROVINCE tail predates the second appended
line, and its 15-line README digest matches no suffix of the file.

### T4 — two artifacts labelled `all-gates v3`, one naming commits that do not exist

`final-gates/all-gates.txt` (0d53f733, 1,765 B) is authoritative: `export-ref=46c66c2…`,
`suite-sha256=2856a210…`, `closed=8/8 exit=0`, eight graded cases. It is what G2 reads
(`corpus/instruments/r39-closure.sh:678`).

`wave1/ExecSuiteBuild.overlay/all-gates.txt` (75afed0c, 1,738 B) carries the same
`all-gates v3` header and the same suite digest but a **different** `export-ref=f918ec4f…`
and an older payload set (G1 `corrections-outside=1` vs 0, G3 `added-quotes=1` vs 0,
G6 `r39=absent` vs `present`, G7 `rows=4` vs 7). Its refs are not objects in the lane:

```
$ git cat-file -t f918ec4f8edae900f528f6d2daaab84ac425cc31
fatal: git cat-file: could not get object info
$ git cat-file -t b3a3b06b5acb1c17d584636b70c9cbdc9e8b04fc
fatal: git cat-file: could not get object info
```

The same unresolvable pair is quoted by `overlay/heads.txt`, `overlay/MANIFEST.txt`,
`overlay/run-at-J.txt`, `overlay/run-at-J-with-head.txt`, `overlay/run-at-Y.txt`,
`overlay/selftest-at-Y.txt` and `wave1/ExecSuiteBuild.md` §Runs. Those transcripts were
taken in a scratch overlay repository that no longer exists, so **no committed
transcript names a ref a verifier can reach**. Under the round's own R35
(`corpus/QUALITY.md:307`) they are neither backed by a `final-gates/` transcript nor
labelled `report-only`; the report must not quote them.

The one coherent transcript pair that survives is `overlay/run-at-base.txt` (7e0a8946)
and `overlay/run-at-r38head.txt` (359979c0): both refs exist, both runs are 2/8 red, and
`overlay/blocks/reds.txt` duplicates `run-at-base.txt` modulo one `deviation=` line
(1,330 vs 1,301 B; `diff` reports only `2d1 < deviation=non-default --lane`).

### T5 — the wave-1 index is stale in 2 of 235 rows

`wave1/ScribeWaveEvidence.index.md` (da6a7e8b, 55,327 B) re-verified row by row against
the bytes at HEAD: 233 rows match on bytes, newline count and sha256; two do not —

| row | index says | HEAD |
|---|---|---|
| `ExecNoPlaceholderScan.md` | 12,420 B, 263 lines, `08566ad1…` | 14,299 B, 293 lines, `02a022f0…` |
| `ScribeWaveEvidence.md` | 6,644 B, 114 lines, `5383c906…` | 6,959 B, 120 lines, `56d41265…` |

Row bytes total 1,541,795 against the stated 1,539,601 (Δ 2,194 B = 1,879 + 315). Both
files were finalised in the same commit that carries the index (`46c66c2`), so the index
snapshot is pre-commit. It also indexes `swarm-registry.json` (pre-wave bookkeeping) and
omits itself.

### T6 — zero-byte and duplicated bookkeeping

* `wave1-plan.err`, `wave1-run.err`, `wave2-plan.err`, `wave2-run.err` are **0 B**.
* `wave1|2-spec.json` (413,733 + 203,578 B) repeat one ~7,045 B / 4,581 B context block
  per item (49 and 37 items); `wave1|2-dispatch.json` (433,466 + 218,350 B) and
  `wave1|2-plan.out` (422,719 + 212,824 B) reproduce the same task texts and plan again;
  `kasegi-r39-build-results.json` (239,000 B) repeats the seat envelopes a third time.
  The 49/37 task prompts hash differently across files (the dispatch prefix differs), so
  this is triple duplication, not triple identity — but no evidence line depends on any
  of the three.
* Five fixture-pack base images repeat across packs by design (`01-full-tail-green` and
  `02-partial-tail-red` share `base/PROVINCE.md` `704b9c1a…` and `base/corpus/README.md`
  `9851dc92…`; `export/` equals `head/` inside each pack). These are per-scenario images,
  not staging copies: **keep**.

## 4. Measured defect in the C1 evidence chain: the counting commands need a clean checkout

The frozen counting commands carry no `--lane` (`claims.json` C1; erratum E4), i.e. they
run against the **live lane**. Today the live lane holds uncommitted wave-2 work, and the
suite's G8 limb executes the pinned r37 suite, whose E9 limb reads the live worktree
(`corpus/instruments/r39-closure.sh:185-190`: "at the real judged head the lane must be
checked out at Y with a clean tree, else G8 reds by construction"). Measured:

```
# live lane, worktree clean? no (wave-2 files untracked)
$ bash corpus/instruments/r39-closure.sh --export-ref 5006097a84305267c9a3e8c1e1d560e60fe41d37 ...
G8 payload=pin-ref=2387dcf6…,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
closed=7/8 exit=1

$ bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097a8430… ...
selftest case=G8 positive=fail mutants=3/3 verdict=fail
selftest cases=8 failures=1
exit=1

# clean clone of the same lane checked out at Y (`git clone --shared`, status 0 lines)
$ bash corpus/instruments/r39-closure.sh --export-ref 5006097a8430… --lane <clone> ...
G8 payload=…,r37-closed=1,r37-exit=0 closed=1
closed=8/8 exit=0

$ bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097a8430… --lane <clone> ...
selftest cases=8 failures=0
exit=0
```

The nested r37 suite's own payload explains the live-lane red: `E9 payload=…,status-dirty=6,
head-match=1,… closed=0` (six untracked wave-2 paths). The same precondition moves the
J-run: live lane at `46c66c2` prints **6/8** (G2 `receipt=0` *and* G8 red), while a clean
clone at `46c66c2` prints **7/8** with G2 `receipt=0` — erratum E4's number only in the
clone. Base and r38-head controls stay red either way (`closed=2/8 exit=1`).

Consequences for the report (this is a defect in the *record*, not in the instrument,
which documents the limit):

1. Three lane lines assert the result without the precondition —
   `corpus/lessons/round-39.md:15` ("`closed=8/8 exit=0` at Y; graded
   `selftest cases=8 failures=0`"), `:76` ("`--export-ref Y` prints 8/8"),
   `SCORECARD.md:1567` ("`closed=8/8 exit=0` at Y, graded `selftest cases=8 failures=0`").
   True of the export bytes at Y; not true of the command as frozen.
2. `final-gates/all-gates.txt` cannot be re-earned after the round's next commit: the
   nested E9 `head-match` limb needs lane HEAD == Y, and G2 needs the receipt's
   `export-ref` to be ancestor-or-equal of REF with a receipt-only diff — so the 8/8 is a
   snapshot of a transient window (clean tree, HEAD == Y), not a replayable predicate.
3. The receipt records no lane state (no head, no porcelain count). Any claim that "the
   counting command prints 8/8" must carry the precondition "clean checkout of the lane at
   Y" or be labelled `report-only` with the clone run attached.

The C2 counting commands, by contrast, are tree-local and reproduce exactly today
(section 5, row R12), which is why the wave-1 C2 copies in T1 can be dropped.

## 5. Minimal evidence set for the round-39 report

Fourteen artifacts. Every row is a file that still earns its bytes; nothing here depends
on the dispatch/plan JSON.

| # | artifact | B | sha256 | proves | why it cannot be dropped |
|---|---|---:|---|---|---|
| R1 | `.ufo/waves/round-39/claims.json` | 8,942 | `e427ab6a…e051c` | the frozen predicates, counting commands, kill rules | the thing under test |
| R2 | `.ufo/waves/round-39/claims-erratum-1.md` | 5,505 | `712c3a8d…9a86a` | E1 59, E2 40-char r38 head, E4 Y-ref, E5 semantics | the claim text alone is wrong on registry count and ref |
| R3 | `c1-controls/before.txt` | 1,017 | `0363c8c0…e348b` | C1 before-state: suite absent, R1–R5 open, 25 r38 mutants | not derivable from HEAD |
| R4 | `c2-controls/before.txt` | 543 | `866ac757…7af2` | C2 before-counts (21/55/50/24/45/50) | not derivable from HEAD |
| R5 | `final-gates/all-gates.txt` | 1,765 | `0d53f733…ffe025` | the only committed Y receipt: export-ref, suite digest, 8/8, 8 graded cases | sole authoritative 8/8 transcript, read by G2 |
| R6 | `wave1/ExecSuiteBuild.overlay/run-at-base.txt` | 1,301 | `7e0a8946…c98520` | base red 2/8 (kill-rule control) | resolvable ref; reproduces (measured 2/8) |
| R7 | `wave1/ExecSuiteBuild.overlay/run-at-r38head.txt` | 1,301 | `359979c0…7b9fce` | r38-head red 2/8 with the 40-char ref | resolvable ref; reproduces (measured 2/8) |
| R8 | `wave1/ExecSuiteBuild.overlay/run-at-r38head-37char.txt` | 127 | `859f8596…42b89598` | the truncated hash is refused (exit 2) | one line; documents E2's necessity |
| R9 | `c2-controls/junk-f22-recheck.txt` + `junk-manifest.json` | 4,924 + 1,211 | `7d6e7df2…`, `9dafce36…` | junk-f22 rejected, capture bound | the F22 negative control; `junk-f22.md` (8a719e6a) is the recipe |
| R10 | `wave1/ExecCaptureStability.stability.txt` | 3,689 | `87fce57e…df1ffc` | duplicate-fetch stability of the S057 capture | time-dependent; cannot be re-run after the page changes |
| R11 | `wave1/ExecSuiteBuild.md`, `wave1/ExecConsiderthese.scorecard.append.md`, `wave1/ExecScoreGap.gap.txt` | 8,467 / 4,897 / 15,130 | `08f2cfa0…`, `a8c7af52…`, `65f5e7b1…` | design provenance of the suite; byte-exact source of the SCORECARD block and the gap measurement | **cited by landed files** (instrument line 66, ledger line 81); removing them breaks a live pointer |
| R12 | the C2 tree counters, quoted not copied: `corpus/SOURCES.md` (59 rows), `corpus/knowledge/cisa-when-to-issue-vex.md` (51st entry, `source: S057`), `corpus/source-snapshots/round-39/{S057.txt,manifest.json}`, `corpus/README.md` (22 frontier rows) | — | `11c8d6d6…`, `432f2205…` | all seven C2 counters | re-measured this seat: frontier 22; registry 59; 1 entry citing S057; knowledge 51; harness `entries=25 pass=25 exit=0`; binding `records=46 bound=46 unbound=0`; audit `expected=51 missing=0 unexpected=0 exit=0` |
| R13 | `wave2/` per-seat receipts (authoritative for their own item) | — | — | wave-2 falsification record | in flight at snapshot (31 entries, 20:21Z); each seat's receipt is the evidence for its item, not the wave-1 file it re-reads |
| R14 | this file + `SimplArtifactTrim.md` | — | — | trim verdict and run record | the only place the clean-checkout precondition is measured |

**Substitutions** (same fact, one authority): `wave1/ExecSuiteBuild.r39-closure.sh` →
`corpus/instruments/r39-closure.sh` (`2856a210…`); `wave1/ExecFrontierCapture.*` →
`corpus/source-snapshots/round-39/*`; `wave1/ExecJunkRecheck.*` → `c2-controls/*`;
`wave1/ExecHarnessProbe.harness.txt` (74,637 B) → the re-runnable
`corpus/instruments/frontier-recheck-count.py`; `c1-controls/census-before.txt` (276 B) →
the C2 before line in R4; `overlay/{all-gates,heads,MANIFEST,run-at-J,run-at-J-with-head,
run-at-Y,selftest-at-Y}.{txt}` → R5 + a clean-clone rerun, since their refs do not resolve.

**Do not drop**: R5 (only Y receipt), R3/R4 (before-states), R6/R7/R8 (control
discrimination), R9 (F22 negative control), R10 (time-dependent), R11 (live citations),
R13 (the round's own falsification record).

## 6. Tradeoffs and limits

* Dropping T1/T2/T3 removes 229,458 B (≈14.5 % of `wave1/`) from the *report's* citable
  set, not from the repo: the wave-1 files are committed at J2 and the round is
  append-only, so this is a citation decision, not a deletion. A later seat may delete
  them in a cleanup round only after checking that no landed file cites them (rule 1) —
  at HEAD, three `wave1/` files are cited, and the ones in T1/T2 (except R11) are not.
* `ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh` (73,132 B, T1) is a hermetic copy
  of a tracked file: the fixture pack is reproducible only with it, and the committed
  suite bypasses it via `git show 2387dcf6`. Keeping it costs one duplicate; dropping it
  makes the standalone fixture pack unrunnable. Default: keep, cite the instrument.
* `ScribeWaveEvidence.index.md` (T5) is a derived pointer index. It is useful only if its
  two stale rows are corrected; otherwise the report should cite the wave-2
  `ScribeFinalWaveEvidence` receipt instead. This seat cannot edit it (write scope).
* The live lane's 7/8 (section 4) is an environment property, not a byte property of Y:
  the export bytes are unchanged. I did not attempt to establish whether the round's
  authors ran the receipt pass from a clean clone; the transcript does not say. What is
  measured is that the command *as frozen* no longer reproduces, and that it cannot
  reproduce after the next commit.
* Not measured here (other seats own them): the 8 graded cases' mutant adequacy
  (`CritMutantAssault`, `MutSuiteLimbs`), the C2 row/entry content (`RevF22*`), the
  wave-2 receipts themselves (still landing), and whether the report should cite Y or J
  as "the judged head" (the erratum and G2 disagree in wording; `RevC1Receipt` owns it).
* No tool was installed; no `pacman` transaction was attempted; the only git commands
  used were `log`, `diff`, `show`, `cat-file`, `ls-files`, `status`, `clone` into
  scratch, and `checkout` **inside that scratch clone** (`git -C $S/clone rev-parse
  --show-toplevel` → `$S/clone`). The scratch dir was removed before yielding.
