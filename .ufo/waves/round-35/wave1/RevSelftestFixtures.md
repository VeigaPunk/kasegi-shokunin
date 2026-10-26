# RevSelftestFixtures — round-35 wave-1 receipt (reviewer, r35-fixtures set)

- Seat: RevSelftestFixtures (reviewer, leaf of the L2 wave; no subagents dispatched)
- Scope: review `corpus/instruments/r35-fixtures/` against the seat acceptance:
  (A1) each of D1–D7 has a fixture where exactly that defect is present and the other six are fixed;
  (A2) the suite's `--selftest` over the set yields `cases=7 failures=0`;
  (A3) a fixture with two defects reintroduced fails exactly two checks;
  (A4) no fixture is vacuous (each truly changes the check's verdict).
- Reviewed at: 2026-10-26, lane worktree at HEAD `da2d3c6` ("round-35: wave-1 spec + dispatch (64 seats, v2)");
  claims freeze `617496b`, lane base `3266c99` untouched.
- Suite under review: `corpus/instruments/r35-defect-closure.sh`, sha256
  `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304` (773 lines), identical before and
  after every run below (stability checked, §8). This digest differs from the suite the executor first
  read (`c748dd70…`): the `report_ok` anchoring fix it reported to ExecClosureSuite landed mid-review;
  all runs below are against the fixed suite.

## Report

### 0. Measurement basis (materialization), and why

`check_d4` counts `git ls-files -- .ufo/waves/round-34/wave1-results.json` from the root under test.
Inside the lane worktree that pathspec resolves against the **lane's** index, never the fixture's
files, so an in-place `--root corpus/instruments/r35-fixtures/D3` run reads `D4 … tracked=0` on every
fixture regardless of fixture content. Negative control, measured:

```
$ bash corpus/instruments/r35-defect-closure.sh --root corpus/instruments/r35-fixtures/D3
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=1 open=1          <- artifact: lane index, not the fixture
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1                                raw-exit=1
```

Every run below therefore materializes each fixture tree first, exactly as the suite's own
`materialize()` does (`cp -a` → `git init -q` → `git add -A`), which is also the recipe
`corpus/instruments/r35-fixtures/README.md` ("How to run the set") prescribes. The suite's `--selftest`
materializes internally; no fixture tree is ever measured in place.

### 1. Fixture inventory (A1 structure)

`find corpus/instruments/r35-fixtures -type f | sort` → 63 files: `D1/`…`D7/` (7 files each, D4 has 6
+ `.gitignore`), `clean/` (7), `two-defect/D1D2/` (7), plus `README.md` and `fixtures.json`. No
stray files, no nested `.git` anywhere in the committed set (the executor explicitly avoided nested
repos — a gitlink inside this jj-colocated lane would be a worse defect than the one under test).

Every tree carries the same seven-file row layout (`fixtures.json` → `row_root_layout`):
`SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `.ufo/waves/round-34/wave1-results.json`,
`.ufo/waves/round-34/wave1-results.json.provenance.md` (absent in `D4/`),
`.ufo/waves/round-35/claims-erratum-d5.md`, `.ufo/waves/round-34/wave1/L1Integration.md`.

Digest groups (sha256; every file is either a shared fixed copy or a defect variant):

| role | files | sha256 |
|---|---|---|
| fixed SCORECARD (clean, D3–D7) | `cf0871072b3909e4…` | clean/D3/D4/D5/D6/D7 `SCORECARD.md` |
| D1 defect SCORECARD | `a4f21d974f5dbef5…` | `D1/SCORECARD.md` |
| D2 defect SCORECARD | `8d37f176e250ad26…` | `D2/SCORECARD.md` |
| two-defect SCORECARD | `092e3a8189156e81…` | `two-defect/D1D2/SCORECARD.md` |
| fixed SKILL | `b3e65baf8e81322e…` | all trees except `D3/` |
| D3 defect SKILL | `ace0e887f632b193…` | `D3/SKILL.md` |
| fixed QUALITY | `346d1c1ce5873355…` | all trees except `D7/` |
| D7 defect QUALITY | `0efdf7a196d1c0fc…` | `D7/corpus/QUALITY.md` |
| fixed L1Integration | `549dd352195c5b25…` | all trees except `D6/` |
| D6 defect L1Integration | `aebf5bcc285bece5…` | `D6/…/L1Integration.md` |
| fixed erratum-d5 | `ec9a82869dc115eb…` | all trees except `D5/` |
| D5 defect erratum-d5 | `2292d081a0a92a01…` | `D5/…/claims-erratum-d5.md` |
| results json (byte-identical everywhere, incl. D4) | `a27fe46892493655…` | all 9 trees |
| fixed provenance note (absent in D4) | `f2ba0bcc681a73bb…` | 8 trees |
| D4 `.gitignore` | `b0f1ac5f17972347…` | `D4/.gitignore` only |
| manifest / README | `b9a07afa1bed7b15…` / `9bcb39cb5315abe0…` | `fixtures.json` / `README.md` |

`D4/.gitignore` (verbatim):

```
# limb D4 broken: the results file is left out of the index (untracked), and no provenance note exists
/.ufo/waves/round-34/wave1-results.json
```

Clause-level grep of the pinned bytes (each fixture's own limb open, all other limbs closed —
`ph`=`filled by the L1`, `lh`=`<LANE_HASH>`, `cor`=`c1c6a5f`, `er`=`round-34 depth:density row`,
`mean`=`201.2`, `row`=stale-row prefix grep, `rdc`/`krc`=`r-defect-closure`/`kill-rule-check`,
`disc`/`occ`=`discriminating invocation`/`per-id occurrences`, `stale`/`corr`=dead-seat / `Correction (round 35)`,
`r22`/`r23`=`supersedes R22`/`supersedes R23`):

```
clean            SCORECARD: ph=0 lh=0 cor=1 er=1 mean=1 row=1   <- all D1/D2 clauses closed
D1               SCORECARD: ph=1 lh=0 cor=0 er=1 mean=1 row=1   <- only D1 open
D2               SCORECARD: ph=0 lh=0 cor=1 er=0 mean=0 row=1   <- only D2 open
two-defect/D1D2  SCORECARD: ph=1 lh=0 cor=0 er=0 mean=0 row=1   <- D1+D2 open
D3 SKILL: rdc=0 krc=0        | clean SKILL: rdc=1 krc=1
D5 erratum: disc=2 occ=0     | clean erratum: disc=2 occ=1
D6 L1Int: stale=1 corr=0     | clean L1Int: stale=0 corr=1
D7 QUALITY: r22=0 r23=0      | clean QUALITY: r22=1 r23=1
D4 tree: results-present=yes provenance-present=no; results bytes identical to clean's
```

Note: the fixture "fixed" copies carry corrections that are **not yet on the live lane** (live
`D6 corr=0`, `D7 r22=0 r23=0`, `D4 tracked=0` at review time — in-flight seats + L1 integration).
The fixtures therefore pin the intended closed bytes, which is what a fixture for a not-yet-landed
correction must do; the live half of the selftest covers the real files once they land.

### 2. A1 — per-fixture isolation: exactly one defect, other six fixed (PASS)

Suite `--root` on each materialized fixture (exit codes in tail; full outputs in my run log):

```
fixture=D1 open=[D1 ] own-line: D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1 | exit=1
fixture=D2 open=[D2 ] own-line: D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1 | exit=1
fixture=D3 open=[D3 ] own-line: D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1 | exit=1
fixture=D4 open=[D4 ] own-line: D4 check=tracked=0,provenance=0 open=1 | exit=1
fixture=D5 open=[D5 ] own-line: D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0 open=1 | exit=1
fixture=D6 open=[D6 ] own-line: D6 check=dead-seat-sentence=1,correction-round-35=0 open=1 | exit=1
fixture=D7 open=[D7 ] own-line: D7 check=supersedes-R22=0,supersedes-R23=0 open=1 | exit=1
```

Every fixture fails **exactly its own check**; the other six read `open=0` on the same tree. Each
rejection payload matches the suite's own `fix_re` for that defect (the anti-vacuous discriminator):
D1 `placeholders=[1-9]`, D2 `erratum-row=0`, D3 `registry-r-defect-closure=0`, D4 `provenance=0`,
D5 `per-id-occurrences=0`, D6 `dead-seat-sentence=[1-9]`, D7 `supersedes-R22=0`. The suite's selftest
independently asserts the same property per case (`others=6/6` in every case line, §4).

### 3. Controls (PASS)

```
tree=clean            open=[]          summary=closed=7/7 exit=0   exit=0
tree=two-defect/D1D2  open=[D1 D2 ]    summary=closed=5/7 exit=1   exit=1
```

`clean/` passes all seven checks (proves the fixture harness is not always-reject, and proves D4's
tracked limb reads `tracked=1` when no ignore rule is present — the limb the D4 fixture does not
carry). `two-defect/D1D2/` fails exactly D1 and D2.

### 4. A2 — the suite's `--selftest` over the set (PASS on every fixture-intrinsic half; live half gated on L1 integration)

Literal run at review time (`KASEGI_SCRATCH` pointed into my scratch dir; suite writes only there):

```
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=fail fixture=rejected mutants=2/2 others=6/6 verdict=fail
selftest case=D5 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D6 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest case=D7 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest problem=self-report status=1
selftest-exit=1
```

All seven **fixture halves are green** (`fixture=rejected`, mutants `n/n`, `others=6/6`), both
controls pass, and the do-nothing control is rejected by the judge. The three `verdict=fail` cases are
**not fixture defects**: their `live=fail` payloads name clauses still open on the live lane at review
time — `D4 live-reason=tracked=0,provenance=1` (results file not yet in the git index; only the L1
commits), `D6 live-reason=dead-seat-sentence=1,correction-round-35=0` and
`D7 live-reason=supersedes-R22=0,supersedes-R23=0` (corrections still landing). The D6/D7
`mutants=0/2 … verdict=unexpected` lines are the same artifact: mutants are built from **live** bytes,
and with live's correction/supersession clauses still open, `isolate_ok` correctly refuses to attribute
the failure to the reopened clause alone. No fixture is implicated in any of the three failures.

Proof that the suite+fixture set prints the claimed form once the lane root is closed — prediction
run, clearly labeled: a scratch copy of the suite with only the `LANE_ROOT=` line redirected to a
fully closed stand-in tree (my repaired-D7 tree, §6, plus `c1-controls/` copied in for judge
fidelity; `r35-fixtures` symlinked, i.e. the real committed fixtures), then `--selftest`:

```
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D5 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
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
prediction-exit=0
```

All 17 clause mutants (3+3+2+2+2+2+2) isolate correctly on a closed root — including D6/D7, whose
mutants read exactly one open clause there (`dead-seat-sentence=1,correction-round-35=1` /
`supersedes-R22=0,supersedes-R23=1` etc.). **Verdict: the `cases=7 failures=0` criterion is met by the
suite+fixture set; the literal lane run turns green exactly when the L1's integration lands
(D4 git-index + D6/D7 corrections), which is inherent ordering for this round, not a fixture gap.**

### 5. A3 — two defects reintroduced → exactly two checks fail (PASS, full 21-pair matrix)

Beyond the committed `two-defect/D1D2` control I built every pair T(i,j) = materialized fixture D*i*
with defect *j* reintroduced (defect file overlaid from fixture D*j*; for the shared-file pair D1+D2
the committed two-defect SCORECARD; for j=D4 the D4 `.gitignore` + provenance removal), materialized
the same way, and ran the suite:

```
pair=D1+D2 open=[D1 D2 ] OK exit=1     pair=D2+D6 open=[D2 D6 ] OK exit=1
pair=D1+D3 open=[D1 D3 ] OK exit=1     pair=D2+D7 open=[D2 D7 ] OK exit=1
pair=D1+D4 open=[D1 D4 ] OK exit=1     pair=D3+D4 open=[D3 D4 ] OK exit=1
pair=D1+D5 open=[D1 D5 ] OK exit=1     pair=D3+D5 open=[D3 D5 ] OK exit=1
pair=D1+D6 open=[D1 D6 ] OK exit=1     pair=D3+D6 open=[D3 D6 ] OK exit=1
pair=D1+D7 open=[D1 D7 ] OK exit=1     pair=D3+D7 open=[D3 D7 ] OK exit=1
pair=D2+D3 open=[D2 D3 ] OK exit=1     pair=D4+D5 open=[D4 D5 ] OK exit=1
pair=D2+D4 open=[D2 D4 ] OK exit=1     pair=D4+D6 open=[D4 D6 ] OK exit=1
pair=D2+D5 open=[D2 D5 ] OK exit=1     pair=D4+D7 open=[D4 D7 ] OK exit=1
                                        pair=D5+D6 open=[D5 D6 ] OK exit=1
                                        pair=D5+D7 open=[D5 D7 ] OK exit=1
                                        pair=D6+D7 open=[D6 D7 ] OK exit=1
pairs_ok=21 pairs_bad=0
```

21/21 exact: no pair leaks a third open check, no pair hides one of its two. The limbs are
genuinely independent.

### 6. A4 — no fixture is vacuous (PASS)

Repair-flip test: for each fixture, replace only its defect-carrying file(s) with the `clean/` copies
(for D4: drop `.gitignore`, restore the provenance note), re-materialize, re-run the suite:

```
repaired=D1 summary=closed=7/7 exit=0 exit=0
repaired=D2 summary=closed=7/7 exit=0 exit=0
repaired=D3 summary=closed=7/7 exit=0 exit=0
repaired=D4 summary=closed=7/7 exit=0 exit=0
repaired=D5 summary=closed=7/7 exit=0 exit=0
repaired=D6 summary=closed=7/7 exit=0 exit=0
repaired=D7 summary=closed=7/7 exit=0 exit=0
```

Each fixture's failure is owned by exactly its defect bytes: removing them flips the tree to a
fully passing one (byte-equivalent to the `clean` control). Combined with §2 (rejection names the
defect's own clause via `fix_re`) this is the strongest non-vacuousness reading: the verdict change
is caused by the defect clause alone, in both directions.

### 7. Findings

1. **[minor, suite-side — not a fixture defect] D5's `erratum-file` clause is isolated by neither
   fixture nor mutant inside `--selftest`.** `clause_specs D5` has three clauses
   (`erratum-file`, `discriminating-invocation`, `per-id-occurrences`) but `mutant_specs D5` builds
   only two mutants, and the committed `D5/` fixture keeps the file present (it must — `fix_re D5` =
   `per-id-occurrences=0`, and a file-absent fixture would read `verdict=unexpected`). The
   `mutant_specs` header comment "Every clause of every check has exactly one mutant" is therefore
   inaccurate for this one clause. The limb *is* exercised outside the selftest by the base-tree run
   (erratum file absent at base → `erratum-file=absent`, check fails), so this is a selftest-internal
   coverage note, not a claim-level hole. One-line fix if wanted: a `D5:+file` mutant
   (`copy_live` the erratum file's parent, omit the file). Reported to ExecClosureSuite.
2. **[info, documented deviation] Fixture bytes are pinned excerpts, not full-file copies.** The
   dispatch text said "a copy of SCORECARD.md"; the landed set ships line-faithful excerpts and says
   so in `r35-fixtures/README.md` §Limits ("the live SCORECARD.md, SKILL.md and corpus/QUALITY.md are
   large and move every round, and a fixture that tracked them would rot into a pass"). I judge the
   deviation sound: the checks read only the pinned clause literals, functional equivalence is proven
   by §§2–6, and the live half + base-tree run cover the real files. The README also honestly scopes
   what no fixture proves (D2's "base bytes not deleted" remains a git-diff reading on the lane).
3. **[info] The selftest's live half is integration-gated.** At review time the lane still reads
   D4 `tracked=0` (git index — only the L1 commits), D6 `corr=0`, D7 `r22=0 r23=0`; the three
   selftest failures trace entirely to those live payloads (§4). Fixture halves, mutants-on-closed-root,
   controls and judge are all green. The literal `cases=7 failures=0` on the lane becomes true at the
   L1's integration commit; the prediction run proves the suite reaches it.
4. **[info] Raw in-lane `--root` runs on fixture dirs read D4 open on every tree** (git pathspec
   resolves the enclosing lane repo) — measured negative control in §0, documented in the README's
   run recipe; the suite's selftest materializes, so the committed behavior is correct.
5. **[info] Tracking state:** `corpus/instruments/r35-defect-closure.sh` and
   `corpus/instruments/r35-fixtures/` are untracked (`??`) at review time; the L1 commits at
   integration (the suite header's "committed defect fixture" wording becomes literally true then).
   `two-defect/` is nested one level down so a `D[1-7]` glob never picks it up as a case (README).

### 8. Run integrity

- Suite sha256 identical before and after all runs:
  `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304`.
- All scratch (harness, materialized trees, pair trees, repaired trees, patched-suite prediction copy,
  suite's own `KASEGI_SCRATCH` trees) lived under `/fast/scratch/hyaku/kasegi-r35/RevSelftestFixtures/`
  and is deleted before this receipt's submission (confirmed by the post-delete check below; a
  surviving tree would be reported here as a defect — none is).
- No tools installed (none needed); no `pacman` use; no git/jj mutations anywhere — the only git
  invocations were read-only (`git ls-files`, `git status`, `git log`, `git init`/`git add -A`
  strictly inside my scratch trees, mirroring the suite's own materialize semantics).
- Peer coordination: 1 message to ExecSelftestFixtures (measurement-basis questions, answered), 1 to
  ExecClosureSuite (finding 1). No `agent://all`, no subagents.

## Verdict

**PASS on every fixture-intrinsic acceptance criterion**, with evidence above: (A1) each of D1–D7
fails exactly its own check with the other six passing on the same materialized tree, and each
rejection names its own clause per the suite's `fix_re`; (A2) the suite's `--selftest` is green on
all seven fixture halves, both committed controls, all 17 clause mutants on a closed root, and the
do-nothing judge — the literal `cases=7 failures=0` on the lane is gated only on the L1's
integration (D4 git-index, D6/D7 corrections), proven reachable by the labeled prediction run;
(A3) two reintroduced defects fail exactly two checks — verified on the full 21-pair matrix, not
just the committed D1D2 control; (A4) no fixture is vacuous — repairing each fixture's defect bytes
alone flips its tree to `closed=7/7`. One minor suite-side coverage note (D5 `erratum-file` clause:
no fixture/mutant inside `--selftest`, covered by the base-tree run) and no fixture-side defects.

## Addendum — re-verification against the superseding suite bytes (2026-10-26, same session)

ExecClosureSuite reported (and I confirmed) that the suite moved after the bytes reviewed above:
`d7ad8438…` (773 ln) → `a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad` (834 ln,
closes my Finding 1) → `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` (834 ln,
settled during re-verification; stable across a 40 s watch and identical before/after the final
battery). **The fixture set is untouched**: all 63 per-file sha256 digests re-measured identical to
the §1 table, except `README.md` (`9bcb39cb…` → `c7261c745e60812824a430574b42766a1e3f2193fea30c29e9e866e6e3547e55`,
the documented-spelling update ExecClosureSuite recorded in its receipt §10); `fixtures.json` still
`b9a07afa…`.

Full battery re-run coherently against the settled `0ae4b484…` (digest checked immediately before and
after the run — equal, so no step straddled an edit):

- **Controls**: `clean` → `closed=7/7 exit=0`; `two-defect/D1D2` → `closed=5/7 exit=1`, open exactly
  `D1 D2`. (unchanged)
- **A1 per-fixture isolation**: identical to §2 — each `D<i>` opens only its own check, payloads
  unchanged, `exit=1`. (unchanged)
- **A2 selftest, literal no-arg run**: fixture halves all green, D5's case line now reads
  `mutants=3/3` (the new cascade mutant included); the three `verdict=fail` cases remain exactly the
  live-gated ones (`D4/D6/D7 live=fail` — lane still mid-integration at re-verification time:
  `tracked=0`, `corr=0`, `r22=0 r23=0`), `cases=7 failures=3 control-failures=0`, exit 1. (unchanged shape)
- **A2 selftest, the suite's own green path — now native, no patched copy**: the suite honours
  `--root` in selftest mode, so `bash corpus/instruments/r35-defect-closure.sh --root <materialized
  r35-fixtures/clean> --selftest` prints all seven cases `live=pass fixture=rejected mutants=n/n
  others=6/6 verdict=pass` (16 clause mutants: 15 isolated + D5's `-erratum-file` cascade, detail
  line `selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,
  per-id-occurrences=0 cascade=1`), both controls pass, `selftest cases=7 failures=0`,
  `selftest judge=complete-report accepted=1`, **exit 0**. This supersedes my §4 prediction run
  (which needed a `LANE_ROOT`-patched copy; retained above as historical evidence of the same result).
  The `mutant_specs` header comment now states the cascade rule instead of over-claiming one-mutant-
  per-clause isolation.
- **A4 repair-flip**: all seven repaired trees → `closed=7/7 exit=0`. (unchanged)
- **A3 two-defect matrix**: `pairs_ok=21 pairs_bad=0`, every pair opens exactly `{Di,Dj}`. (unchanged)

**Addendum verdict: PASS, unchanged**, now evidenced against the settled suite bytes `0ae4b484…`
(834 ln) with the fixture set byte-identical to the set reviewed in §1–§7. Finding 1 is **closed** in
these bytes (D5 `erratum-file` covered inside `--selftest` by the cascade mutant; comment accurate).
Findings 2–5 stand as written; Finding 3's gating resolves at the L1's integration commit exactly as
described there. Scratch for the re-verification
(`/fast/scratch/hyaku/kasegi-r35/RevSelftestFixtures/`) deleted before this addendum's submission.
