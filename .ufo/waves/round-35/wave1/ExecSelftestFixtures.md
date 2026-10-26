# ExecSelftestFixtures — round-35 broken-fixture set for the C1 closure suite

Seat: executor `ExecSelftestFixtures` (leaf of the round-35 wave). Lane `kasegi-shokunin`, lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Written at lane `HEAD` `da2d3c687f82a9814ee71c91c930cb733050d37c` (jj working copy `8dae5bf3…`),
2026-10-26T06:42Z. The L1 commits; this seat ran no `git add`/`commit`/`push` and no jj mutation.

Item: create the broken-fixture set the C1 closure suite consumes in `--selftest`, one tree per
round-34 verifier-routed defect D1–D7, each isolating exactly one limb.

## Report

### 0. What landed

| path | files | bytes | sha256 |
|---|---|---|---|
| `corpus/instruments/r35-fixtures/` (whole set) | 65 (54 `.md`) | 77 514 | per-file list: `.ufo/waves/round-35/wave1/ExecSelftestFixtures-digests.txt` (`18dec376…`) |
| `corpus/instruments/r35-fixtures/README.md` | 86 lines | — | `6d99ba915272f9424f3d9fb9cc56fbfd6b2fb34c3c3c60c3037d991ef6562563` |
| `corpus/instruments/r35-fixtures/fixtures.json` | 113 lines | — | `b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113` |
| `corpus/instruments/r35-defect-closure.sh` (consumed, not written here) | 834 lines | — | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` |

`git status --porcelain corpus/instruments/r35-fixtures` → `?? corpus/instruments/r35-fixtures/`
(untracked at write; the L1 commits it with the round).

### 1. Inventory — one complete minimal root per case

Each tree is a full root laid out like the lane, because the suite's checks resolve `SCORECARD.md`,
`SKILL.md`, `.ufo/waves/…` and `corpus/QUALITY.md` relative to the root it is given:

```
SCORECARD.md                                          limbs D1, D2
SKILL.md                                              limb  D3
.ufo/waves/round-34/wave1-results.json                limb  D4 (index state)
.ufo/waves/round-34/wave1-results.json.provenance.md  limb  D4 (provenance)
.ufo/waves/round-35/claims-erratum-d5.md              limb  D5
.ufo/waves/round-34/wave1/L1Integration.md            limb  D6
corpus/QUALITY.md                                     limb  D7
```

`D<i>/` breaks limb D<i> and carries fixed content for the other six. `clean/` breaks none.
`two-defect/D1D2/` breaks D1 and D2 (nested one level down, so a `D?`/`D[1-7]` glob cannot mistake it
for a case; the suite reads it by its explicit path).

| tree | limb broken | how the break is written | measured payload (suite output, §2) |
|---|---|---|---|
| `D1/` | D1 | `SCORECARD.md` keeps the round-34 placeholder sentence `**Round-34 final lane commit: filled by the L1 in the closing commit.**`; no `c1c6a5f`, no `<LANE_HASH>` marker | `placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0` |
| `D2/` | D2 | stale row carried verbatim (`grep -E '^\| depth:density \| 9 \| mean \*\*201\.7\*\*'`, pinned from the live file at build time) and the appended erratum omitted, so no `round-34 depth:density row`, no `201.2` | `erratum-row=0,erratum-mean=0,row-bytes=1` |
| `D3/` | D3 | registry table lists `recheck-audit.py` and `anchorcheck.py` only; neither `r-defect-closure` nor `kill-rule-check` appears | `registry-r-defect-closure=0,registry-kill-rule=0` |
| `D4/` | D4 | results file present, `.gitignore` names `/.ufo/waves/round-34/wave1-results.json` so `git add -A` leaves it untracked, and no provenance note | `tracked=0,provenance=0` |
| `D5/` | D5 | erratum present, §1 keeps `discriminating invocation`; §2 states the Q9/Q17 fact without the `per-id occurrences` literal | `erratum-file=present,discriminating-invocation=2,per-id-occurrences=0` |
| `D6/` | D6 | stale sentence `- The round-33 summary \`ExecRegressionC1\` did not file a receipt (dead seat, 1 of 65); the` kept; no `Correction (round 35)` | `dead-seat-sentence=1,correction-round-35=0` |
| `D7/` | D7 | R22 (grounded in M34-2) and R23 (grounded in `considerthese/2026-10-25.md:76`) present with their original grounding; no supersession row | `supersedes-R22=0,supersedes-R23=0` |

Why the D4 break is a `.gitignore` and not a nested repository: this lane is jj/git-colocated, so a
nested `.git` inside `corpus/` would be committed as a gitlink — a worse defect than the one under
test. `D4/.gitignore` gives the same observable state under the loader the suite uses (`materialize`:
`cp -a` → `git init -q` → `git add -A`): the copy indexes everything except the results path.

### 2. Per-tree verification — every case isolates its own limb

Command (harness kept in scratch, output sidecar
`.ufo/waves/round-35/wave1/ExecSelftestFixtures-per-tree.txt`, sha256 `4e198dfc…`):

```
bash verify-fixtures.sh <work> corpus/instruments/r35-fixtures corpus/instruments/r35-defect-closure.sh
# per tree: cp -a <tree>/. <dest>/ && (cd <dest> && git init -q && git add -A)
# then:    bash corpus/instruments/r35-defect-closure.sh --root <dest>
```

| tree | suite prints | exit | open check |
|---|---|---|---|
| `clean` | `closed=7/7 exit=0` | 0 | — |
| `D1` | `closed=6/7 exit=1` | 1 | D1 only |
| `D2` | `closed=6/7 exit=1` | 1 | D2 only |
| `D3` | `closed=6/7 exit=1` | 1 | D3 only |
| `D4` | `closed=6/7 exit=1` | 1 | D4 only |
| `D5` | `closed=6/7 exit=1` | 1 | D5 only |
| `D6` | `closed=6/7 exit=1` | 1 | D6 only |
| `D7` | `closed=6/7 exit=1` | 1 | D7 only |
| `two-defect/D1D2` | `closed=5/7 exit=1` | 1 | **D1 and D2 only** |

The per-tree runs above were taken at suite digest `d7ad8438…`; the same isolation is re-proved by
§3 at the final digest `0ae4b484…`, where every case line prints `others=6/6` (the six non-target
checks closed on that fixture's own tree).

Isolation is therefore two-sided: the `clean` control proves each fixture's six non-target limbs are
read as closed (all seven checks exit 0 on one tree), and each `D<i>` proves its own limb is read as
open and no other. Measured index state per materialized tree (the D4 clause's own reading):

```
tree-clean               tracked=1 provenance=1
tree-D1 … D3, D5 … D7    tracked=1 provenance=1
tree-D4                  tracked=0 provenance=0
tree-two-defect-d1d2     tracked=1 provenance=1
```

### 3. The suite's own `--selftest` over the set — green, first with the frozen CLI

#### 3a. Frozen CLI, no instrument change (primary)

The final suite honours `--root` in `--selftest`, so the fixture/suite pair is proved with the
committed bytes exactly as they are:

```
cp -a corpus/instruments/r35-fixtures/clean <scratch>/clean-lane
( cd <scratch>/clean-lane && git init -q && git add -A )
KASEGI_SCRATCH=<scratch>/tmp bash corpus/instruments/r35-defect-closure.sh \
  --root <scratch>/clean-lane --selftest
```

Observed (`.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-frozen-cli.txt`, sha256
`1e1f2af4…`), `EXIT=0` at suite digest `0ae4b484…`:

```
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
selftest judge=complete-report accepted=1
```

#### 3b. The same green path on an earlier cut that hardcoded `LANE_ROOT` (kept for the record)

Earlier suite bytes ran the live limb against a hardcoded `LANE_ROOT`, so a lane whose own D-limbs
were still in flight could not print a green summary. Those runs used a **scratch copy of the suite
with one line changed** — `LANE_ROOT=<materialized clean tree>` — and the committed fixtures beside it:

```
cp corpus/instruments/r35-defect-closure.sh sut4/            # sha256 of the copy after the sed: d24f4e53…
sed -i 's|^LANE_ROOT=.*|LANE_ROOT=<fixed-lane>|' sut4/r35-defect-closure.sh
cp -a corpus/instruments/r35-fixtures sut4/r35-fixtures
cp -a corpus/instruments/r35-fixtures/clean fixed-lane && (cd fixed-lane && git init -q && git add -A)
KASEGI_SCRATCH=<scratch>/tmp bash sut4/r35-defect-closure.sh --selftest
```

`diff` of the copy against the lane file with `LANE_ROOT` normalized on both sides → identical
(`identical_after_lane_root_normalization`), so the only difference is the root under test.

Observed (full output `.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-fixed-lane.txt`,
sha256 `e2fe74bb…`; byte-identical to §3a's report and across the `a4f80067` → `0ae4b484` re-cuts),
`EXIT=0`, at suite digest `0ae4b484…` — excerpt: the per-mutant detail lines of D1–D4, D6 and D7 are
elided, the full 40-line report is in the sidecar:

```
selftest detail=D1 fixture reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D2 fixture reason=erratum-row=0,erratum-mean=0,row-bytes=1
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D3 fixture reason=registry-r-defect-closure=0,registry-kill-rule=0
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D4 fixture reason=tracked=0,provenance=0
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0
selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 cascade=1
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D6 fixture reason=dead-seat-sentence=1,correction-round-35=0
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D7 fixture reason=supersedes-R22=0,supersedes-R23=0
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite absent=1
selftest judge=complete-report accepted=1
```

`selftest cases=7 failures=0` with `judge=complete-report accepted=1` and exit 0 — the claim's
`--selftest` spelling, over this fixture set.

### 4. The same command on the live lane at this seat's read — 4/7 live, all fixtures rejected

Full output `.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-live-lane.txt`
(sha256 `37dc456e…`, at suite digest `0ae4b484…`; byte-identical across the last three suite re-cuts), `EXIT=1`:

```
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=fail fixture=rejected mutants=2/2 others=6/6 verdict=fail
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D6 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest case=D7 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest problem=self-report status=1
```

The fixture half is green on the live lane too (`fixture=rejected` for all seven, both controls pass,
`control-failures=0`). The three live failures are other seats' open work, not fixture state:
D4's live `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` is 0 until the L1 commits the
file (`ExecD4ResultsTrack` landed the file and the provenance note; both are untracked at this read),
and the D6/D7 corrections had not landed yet, which also collapses their scratch mutants (`mutants=0/2`
— the mutant builder filters a clause that is already absent). This is reported, not worked around:
the fixtures do not carry live-lane content, so no fixture edit can close those three.

### 5. Defect found in the consuming suite (reported, and fixed by its owner)

At suite digest `c748dd70979920d48a4f4ac2b38e38cca74bcc72685bf71aa1d256b44f7a02a0` the run printed
`selftest cases=7 failures=0`, both controls `verdict=pass`, then exited 1 with
`selftest problem=self-report cases=7 expected=7`. Cause: `report_ok` tested each fixture detail line
with an anchored pattern, `"^selftest detail=$id fixture reason=$(fix_re "$id")"` (line 485 of that
digest), while the payload only begins with its clause for D1/D2/D3/D6/D7. Measured on the report:

```
D1 anchored=1 unanchored=1     D2 anchored=1 unanchored=1     D3 anchored=1 unanchored=1
D4 anchored=0 unanchored=1     D5 anchored=0 unanchored=1     D6 anchored=1 unanchored=1
D7 anchored=1 unanchored=1
```

i.e. D4 (`reason=tracked=0,provenance=0`) and D5
(`reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0`) never matched, so the
judge rejected the suite's own green report. Reported to `ExecClosureSuite` with the one-line fix
(`reason=.*$(fix_re …)`); the author's next bytes carried it (`d7ad8438…`, line 487) and the bytes now
at `0ae4b484…` still do (line 531). §3 above is the re-run at those bytes. Recorded here because the earlier reading is what a reviewer will find in the
git history of the suite, and because the closed-loop evidence is the re-run, not the report.

### 6. No-harm measurement — the fixture markdown is inside the resolver's scan

`resolve.py` scans `SKILL.md` + `corpus/**/*.md`, so a markdown fixture set under `corpus/` enters the
lane citation census. Measured rather than assumed (script + output sidecar
`.ufo/waves/round-35/wave1/ExecSelftestFixtures-census-delta.txt`, sha256 `fd8762b2…`): two scratch
roots that differ **only** by `corpus/instruments/r35-fixtures/`, each scanned by a scratch copy of
`resolve.py` (exit 0 both times, census files written inside the scratch run dirs):

| root | lane total | SKILL |
|---|---|---|
| without fixtures | `265/2896 = 9.15 %` | `44/589 = 7.47 %` |
| with fixtures | `266/2918 = 9.12 %` | `44/589 = 7.47 %` |

Delta: **+22 distinct citations, +1 resolving** (denominator 2896 → 2918, numerator 265 → 266). The
added tokens are the fixture README's own path mentions and the registry/erratum paths the fixture
payloads must spell (`D<i>/`, `clean/`, `two-defect/D1D2/`,
`corpus/instruments/r35-defect-closure.sh --selftest`, `.ufo/waves/round-34/wave1-results.json.provenance.md`, …).
I did not reword the fixtures to shrink the proxy — the README has to name the trees it documents, and
gaming `density`/`resolve` shape is exactly what `corpus/instruments/README.md` §Known limits warns
against. The disposition (whether the fixtures should be excluded from the census in a future
`resolve.py` change) is the L1's call; the number is disclosed here so the choice is informed.

### 7. Limits and risks

- **Pinned excerpts, not full-file copies.** Each tree carries line-faithful excerpts of the lane
  file's shapes and spellings (the D2 stale row is the live row verbatim, pinned at build time), not
  the several-hundred-line lane files. Rationale: the lane files move every round, and a fixture that
  tracked them would drift into a pass. Consequence: the fixtures prove a check *can* change verdict
  on the bytes it reads; they do not prove the live files' full content is well-formed.
- **D2's "row bytes untouched" is an exact-prefix grep, not a diff.** The suite reads the filed row
  with `grep -cE '^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances'`;
  the fixture carries that row verbatim in every tree. Nothing here proves the round-34 base commit's
  row was not deleted — that remains a `git diff` reading on the lane.
- **`erratum-file=absent` has no committed fixture.** D5's clause list includes the erratum file's
  existence, but `fix_re D5` is `per-id-occurrences=0`, so `D5/` exercises the missing-literal limb,
  not the missing-file limb. The later suite bytes cover existence with a scratch mutant
  (`-erratum-file`, printed `cascade=1` because deleting the file also zeroes the two statements),
  so the clause is tested — just not by a committed fixture. Flagged for `MutFixturesLimbs` /
  `RevSelftestFixtures`.
- **D4 depends on the loader.** Run in place (no copy), `git ls-files` resolves the enclosing lane
  repository and credits the lane's index; the tracking limb is only meaningful in the copied-and-`git
  init`-ed tree the suite builds. `README.md` §How to run states this.
- **Markdown under `corpus/` moves the census** — measured in §6.
- **Suite bytes move under this seat.** The suite is another seat's file. §3a needs no override at
  all (`--root <clean> --selftest` on the committed bytes, digest `0ae4b484…`); §3b is the same green
  path on an earlier cut that hardcoded `LANE_ROOT`, where the copy digest `d24f4e53…` differs from
  the lane file only by that one `LANE_ROOT` line. Four green readings across `c748dd70…`,
  `d7ad8438…`, `a4f80067…` and `0ae4b484…` gave `cases=7 failures=0` on the same fixture bytes.

### 8. Hygiene, commands, tooling

- Scratch root `/fast/scratch/hyaku/kasegi-r35/ExecSelftestFixtures/` (build script, harness, fixed
  lane, sut copies, run outputs, scratch git trees) removed after the sidecars were copied into the
  wave dir — verified empty at yield (`test ! -e` on the path).
- No `pacman`, no installs, no tool upgrades: `bash`, `git`, `python3`, `sha256sum`, `diff`, `find`
  from the host. Nothing to record under the 2026-10-19 tooling authorization.
- Read-only over everything outside `corpus/instruments/r35-fixtures/` and this wave dir; no fleet,
  sibling-lane, bounties or shokuknow access; no subagents; no `agent://all`.
- Peer messages sent: `ExecClosureSuite` (fixture contract before landing; the `report_ok` anchor
  defect with the measured anchored/unanchored table), `RevSelftestFixtures` (D5/D4 design answers,
  the fixture `fix_re` values at quoted lines), `MutFixturesLimbs` (set final, per-tree baseline, the
  D4 `.gitignore` / D5 literal caveats), `RevC1BeforeAfter-3` (fixture set is this seat's; correction
  of the `tracked=0` / `erratum-file=absent` `fix_re` reading, which is not what the current bytes say).
- Peer message received and acted on: `RevClosureSuite` flagged the fixture README's "no fixture and no
  mutant" bullet as stale against the re-cut suite; it was right on the mutant half, so the bullet now
  reads "no fixture" only, and the digests sidecar and §0 were regenerated for the new bytes.
- Peer message received and acted on: `ExecClosureSuite` asked that the D2 stale row start exactly
  with `| depth:density | 9 | mean **201.7**, 25 blocks, 710 path-citation instances` — the fixture
  builds the row by taking the live line verbatim on that prefix, and the `clean` control's
  `row-bytes=1` is the proof it took.

### 9. Files changed by this seat

```
corpus/instruments/r35-fixtures/README.md
corpus/instruments/r35-fixtures/fixtures.json
corpus/instruments/r35-fixtures/{D1,D2,D3,D4,D5,D6,D7,clean,two-defect/D1D2}/…   (63 payload files)
.ufo/waves/round-35/wave1/ExecSelftestFixtures.md                     (this receipt)
.ufo/waves/round-35/wave1/ExecSelftestFixtures-digests.txt
.ufo/waves/round-35/wave1/ExecSelftestFixtures-per-tree.txt
.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-frozen-cli.txt
.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-fixed-lane.txt
.ufo/waves/round-35/wave1/ExecSelftestFixtures-selftest-live-lane.txt
.ufo/waves/round-35/wave1/ExecSelftestFixtures-census-delta.txt
```

Checks the L1 should run after integration: `bash corpus/instruments/r35-defect-closure.sh` →
`closed=7/7 exit=0`; `bash corpus/instruments/r35-defect-closure.sh --selftest` →
`cases=7 failures=0` (green only once D4's file is committed and the D6/D7 corrections land); and
`git ls-files corpus/instruments/r35-fixtures | wc -l` → 65. Before that commit the same command is
expected to name exactly the limbs still open — at my read D4 (`tracked=0`), D6 and D7.
