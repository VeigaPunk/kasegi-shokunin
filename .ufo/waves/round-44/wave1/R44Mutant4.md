# R44Mutant4 — report-completeness mutant accepting absent planner=L1 / wave-count evidence

Item: *Design a report completeness mutant accepting absent planner=L1 or wave count evidence.* Axes: depth:verifiability, coverage. Lane HEAD at probe time `66314015122b9aa32dc40f2f1815df56624c26d1`.

## Verdict: SURVIVED (coverage finding, not a contract change)

The smallest plausible report-completeness mutant — a one-token `and`→`or` on the mandatory-content conjunction — is **killed only by a detector that does not exist in the lane**. No committed instrument, limb, or mutation-ledger row reads `.ufo/reports/**`, so the committed detector set cannot kill it. The routed defect 4 surface (`corpus/lessons/round-43-verifier-spotcheck.md` §6 item 4, "report records neither the planner=L1 mapping nor the L2-floor/residual-call line") is today **ungraded**.

## The mutant

Surface: a candidate committed gate `report-completeness-check.py` grading the two mandatory clauses of `scripts/hyaku/lane-addendum.md:233-239` — `Record the round shape, each wave's seat count, role mix and dead seats, any residual call, and the round total in the report` (233-234) and the planner-seat mapping `Record that mapping in the report` (236-239). Pristine rule:

```
planner = some line outside fences carries `planner` and `L1`
waves   = report carries `N seats` + `M dead seats` AND a parsed
          .ufo/waves/round-*/{wave*|*}-results.json has seats == N
complete = planner and waves          # MUTANT: and -> or  (one token)
```

The `or` mutant accepts whenever **either** piece of mandatory evidence is present — exactly "accepting absent planner=L1 or wave count evidence". It still rejects a report missing both, so it looks healthy under a green-path-only fixture.

## Detector matrix (same bounded detector, three byte states)

Detector = the checker run `--report <fixture> --export <dir>`; exit 0 COMPLETE / exit 1 INCOMPLETE. Export carries the real artifact `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` (`seats=73`, `results`=73). Fixtures:

| fixture | sha256 (first 16) | content |
|---|---|---|
| `complete.md` | `18f003138f2652c6` | r43 report + appended `planner=L1 …` + `round total … 73 seats` lines |
| `r43-actual.md` | `02704332cfeede3a` | the committed round-43 report verbatim (planner absent, waves present) |
| `no-waves.md` | `9230855d5f1a450e` | planner line present, every `seats` line removed |
| `neither.md` | `e33ee061f7229b15` | boundary: neither clause |

Outputs:

```
pristine sha 87a187eabb0f3fc5781593da8436346cc83cf978bce8e8b2df9127683dd7e166
P complete.md   rc=0  REPORT payload=planner=1,waves=1,seats=73,missing=-         verdict=COMPLETE
P r43-actual.md rc=1  REPORT payload=planner=0,waves=1,seats=73,missing=planner   verdict=INCOMPLETE
P no-waves.md   rc=1  REPORT payload=planner=1,waves=0,seats=-,missing=waves      verdict=INCOMPLETE
P neither.md    rc=1  REPORT payload=planner=0,waves=0,seats=-,missing=planner,waves verdict=INCOMPLETE
mutant   sha 31748b9ae4fba3d0eb86b461381c5b57cbe6cc1822965be81eda381f0d62183a
M complete.md   rc=0  payload=planner=1,waves=1,seats=73   verdict=COMPLETE   (non-equivalent: still green)
M r43-actual.md rc=0  payload=planner=0,waves=1,seats=73,missing=planner verdict=COMPLETE  <- SURVIVED
M no-waves.md   rc=0  payload=planner=1,waves=0,missing=waves    verdict=COMPLETE          <- SURVIVED
M neither.md    rc=1  payload=planner=0,waves=0,missing=planner,waves verdict=INCOMPLETE   (boundary)
```

Kill expectation per the ledger idiom: pristine `exit=1` + `verdict=INCOMPLETE` on each defect fixture (killed = exit flip or signal loss). The mutant flips both defect fixtures to `exit=0`/`COMPLETE` — yet still prints `missing=planner` in its own payload, a discriminating signature any real signal would catch.

## Restoration evidence

The mutated copy was overwritten with the exact pristine bytes (not reconstructed): sha `31748b9a…` → `87a187ea…` (= pristine), byte-equal confirmed; re-run reproduces all four pristine rows above verbatim.

## Why it survives the committed detector set

1. **No instrument reads the report surface.** `grep -rn 'ufo/reports' corpus/instruments/ --include='*.sh' --include='*.py'` → 0 hits; `r43-closure.sh` has no `report` token at all. Every limb's scan set excludes `.ufo/reports/**`: K15 reads `LOG.md` + `corpus/lessons/*.md` (`k15-wave-narrative.sh:83-85`), K16 reads `corpus/lessons/*.md` + `LOG/SCORECARD/SHONEN.md` (`k16-placeholder.sh:175-176`), K18's declared scope is `corpus/lessons/round-4[23]*.md` + `.ufo/waves/round-43/*.md` top-level (`k18-transcript.sh:13-17`).
2. **Measured blindness, not just source reading.** Two exports of lane HEAD (`git archive HEAD | tar -x`): A plain; B = A + `.ufo/reports/round-43/kasegi.md` (the actual incomplete report, `02704332…`). All six limbs byte-identical (`diff` rc=0):
   `K14 closed=1`, `K15 closed=1`, `K16 closed=1`, `K17 closed=1`, `K18 closed=0` (pre-existing `unbound=1`, identical in both), `K19 closed=1`. The defect artifact is present and nothing sees it.
3. **The mutation ledger has no report limb.** `corpus/instruments/limb-ledger.json`: 13 limbs over 3 instruments (`recheck-audit.py` ×8, `source-recheck.py` ×2, `frontier-recheck-count.py` ×2), 3 controls; zero report-gate rows (`grep -ci report` = 1, a prose word in a control note). Run at HEAD: `limbs=13 killed=13 survivors=0 controls=3 rejected=3` exit 0 — fully green while this mutant is out of reach.
4. **The detector exists as a one-row addition — proving killability.** The same mutant run through the committed harness `limb-mutation-check.py` with a single scratch ledger row (`find: "complete = planner and waves"` → `replace: "…or…"`; kill = checker on `r43-actual.md`; signal `verdict=INCOMPLETE`; live_exit 1) prints `LIMB RC-planner-or live=1/y mutant=0/n verdict=killed`, `limbs=1 killed=1`, harness exit 0. So the mutant is not equivalent/unreachable in principle; it survives only because the row (and the gate it guards) is absent.
5. **The named counter is absent.** `corpus/instruments/r44-routed-defects.py` (claims.json C1 `counter`) does not exist at HEAD (`git cat-file -e` rc=128) — do-nothing control (`controls/do-nothing.txt:7`) agrees.
6. **Scope note that widens the finding.** The graded artifact is not even in the lane repo: `.ufo/reports/round-43/kasegi.md` is committed in the **fleet root** repo (`fdf719a92d8d305d5465f8087c5af90a8900a172`, file sha `02704332…`); the lane's `.ufo/reports/` holds only `round-21`. A counter graded over a lane export literally cannot read the artifact defect 4 concerns unless its contract names fleet-root paths.

## Do-nothing discrimination

At the frozen base (`do-nothing.txt:2-7`): 8 routed defects present, no r44 correction, no r44 counter. Do-nothing cannot reach C1's after-state — and my probe shows the *attempted* fix route must add the gate too: a C1 counter composed of today's suite would print green with the defect-4 artifact sitting in the export, and a completeness gate written without the red-before fixtures would pass the live r43 report shape. The honest minimal repair is: a committed report-completeness gate + a mutation-ledger row binding it to (at least) the `absent planner` and `absent waves` fixtures, plus a contract clause naming the report path (fleet-root `.ufo/reports/round-44/kasegi.md`) as graded surface.

## Exact commands / outputs

```
git -C kasegi-shokunin rev-parse HEAD                        -> 66314015122b9aa32dc40f2f1815df56624c26d1
grep -rn 'ufo/reports' corpus/instruments/{*.sh,*.py,r43-limbs/*.sh} -> 0 hits
grep -ci planner  .ufo/reports/round-43/kasegi.md            -> 0   (wave counts present: line 4-5 "73 seats … 0 dead seats … Role mix")
grep -ciE 'residual|L2 floor' .ufo/reports/round-43/kasegi.md -> 0
sed -n '233,239p' scripts/hyaku/lane-addendum.md             -> mandatory clauses cited above
git cat-file -e HEAD:corpus/instruments/r44-routed-defects.py -> rc=128 (absent)
# mutation matrix: see table above (run via python3 report-completeness-check.py --report fixtures/<f>.md --export export)
# committed limbs on export-A vs export-B (B adds the report):
bash run-limbs.sh export-A  == bash run-limbs.sh export-B    -> diff rc=0 (payloads byte-identical)
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json --root kasegi-shokunin
   -> limbs=13 killed=13 survivors=0 controls=3 rejected=3, exit 0
python3 corpus/instruments/limb-mutation-check.py --ledger <scratch>/candidate-ledger.json --root kasegi-shokunin
   -> LIMB RC-planner-or live=1/y mutant=0/n verdict=killed; limbs=1 killed=1; exit 0
sha256: pristine 87a187ea…  mutant 31748b9a…  restored 87a187ea… (byte-equal)
```

## Limitations

- The candidate gate is a scratch artifact; the landed gate's exact mandatory-field split is unfrozen. The survival mechanism (weakened conjunction or dropped required field) generalizes to any conjunction over the addendum's required content; a gate keyed on a different split could shift which fixtures discriminate, not whether they exist.
- K18 is `closed=0` at HEAD for a pre-existing `unbound=1` quote — identical in both exports, unrelated to this probe.
- I did not mutate any committed file: the mutant lives only in scratch (`git status` untouched by me beyond this report); the lane's `M corpus/SOURCES.md` and untracked wave files predate/wedging this seat are sibling work, not mine.
- No tools installed; `HYAKU_SCRATCH` unset → scratch at `<lane>/.ufo/scratch/kasegi-r44/R44Mutant4`, deleted on exit.

## Report trailer

- seat: R44Mutant4 (mutation-tester, leaf)
- mutant: `and`→`or` on `complete = planner and waves` (candidate gate, scratch)
- expected detector: committed completeness gate + ledger row keyed on `verdict=INCOMPLETE` — **absent**
- output: defect fixtures `exit=0 verdict=COMPLETE` under mutant (see matrix)
- verdict: **survived** — coverage finding: report-completeness (planner=L1, wave counts/residual) ungraded by all committed gates; no committed detector kills the mutant
- restoration: exact pristine bytes restored over the mutant path, sha `87a187ea…`, re-run byte-identical
- scratch: `<lane>/.ufo/scratch/kasegi-r44/R44Mutant4` — removed on exit
