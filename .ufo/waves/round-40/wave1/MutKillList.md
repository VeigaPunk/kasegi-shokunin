# MutKillList — round 40 wave 1 receipt (mutation catalogue for the r40 suite)

Seat: `MutKillList` (leaf; no subagents). Item: once `ExecSuiteBuild.r40-closure.sh` existed
in the wave dir, build a mutation catalogue for the r40 suite — at least one find->replace
patch per H-limb (H1-H10) whose effect is to reopen exactly that check's defect class, each
run through the suite's `--selftest` (or the affected check directly) with a kill/no-kill
verdict; any survivor is a defect the L1 must know about. Axes touched: **depth:verifiability**
(primary), **coverage** (read-only context). No claim is authored, edited, judged or shipped
by this seat.

## Deliverable

- `MutKillList.txt` — 231 lines, 11 516 bytes, sha256
  `c25cc3f55982ca66fbb371d540457ae5dd9e93d301d51c630f4b55d53bacd40a`, landed at
  `.ufo/waves/round-40/wave1/MutKillList.txt`.
- Content: detector + baseline header; 17 find->replace patches M01-M17 (at least one per
  H-limb: H1×1, H2×2, H3×1, H4×2, H5×2, H6×2, H7×1, H8×1, H9×3, H10×2) each with the exact
  find/replace bytes, the reopened defect class, the verdict and the measured evidence; an
  observations block; a tally. **13 killed, 4 survived** (M08, M11, M12 real coverage
  findings; M14 benign-equivalent).

## Inputs read (all read-only)

- `.ufo/waves/round-40/claims.json` (frozen) — C1 predicate, kill rule, counting commands;
  the H1-H10 definitions the catalogue's patches must reopen.
- `.ufo/waves/round-40/c1-controls/before.txt` — R2/R5/R6 open, G2/G6 flaws standing.
- `.ufo/waves/round-40/wave1/ExecSuiteBuild.r40-closure.sh` — the suite under test (two
  revisions, see below).
- `.ufo/waves/round-40/wave1/CritC1AntiSuite.txt` — the T1-T11 attack menu (45 named
  mutants) used as the source of defect classes.
- `corpus/lessons/round-39-verifier-spotcheck.md` §5 — R1-R7 routed defects (what each
  H-limb must catch).
- `corpus/instruments/r39-closure.sh` — predecessor machinery (`st_pos`/`st_neg`/
  `st_verdict`, `judge_selftest_report`) used to predict the kill signal before the r40
  bytes landed.

## Method

- Detector: the suite's own graded selftest —
  `bash <suite-copy> --selftest --export-ref 5e985b74075dd3813a63d7750966bf8abf693465
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work <scratch>/work-<tag>
  --scratch-root <scratch>/sroot-<tag>`, `TMPDIR=<scratch>/tmp`, identical args for every
  run so pristine/mutated/restored outputs are comparable.
- Kill signal: the per-case `selftest case=H<n> positive=… mutants=<ok>/<n> verdict=…`
  lines. Mutant fixtures are self-contained scratch trees, so the mutant-count signal is
  independent of the export's greenness; a kill = the affected case's `mutants` count drops
  below baseline (the weakened check now accepts a fixture) or the positive limb flips.
- Baseline (pristine, revision 2): `cases=10 failures=9`, case lines H1 3/3, H2 3/3,
  H3 2/2, H4 3/3, H5 2/2 (positive=pass), H6 4/4 (positive=pass), H7 6/6, H8 0/2, H9 5/5,
  H10 3/3 (positive=pass); judge `own-report accepted=0` — expected mid-build: the export at
  5e985b7 predates the round's content, so 7 positive limbs are red (H5's source falls back
  to a self-referential assembled transcript, H6 scans the pinned clean scratch root, H10's
  no-harm holds between base and 5e985b7). H8's `mutants=0/2` is a **baseline failure** at
  this ref (the export has no `r40-closure.sh`, so `check_h8` short-circuits at `suite=0`
  and the graded needles never fire) — H8 is judged by direct probe, per the item's
  "(or the affected check directly)" allowance.
- Survivors were additionally proven by direct probes: sourcing the (mutated) suite copy in
  a scratch shell (`BASH_SOURCE` guard prevents `main`), `prepare_export` +
  `selftest_prepare` for state, then the affected check invoked directly on a crafted
  fixture (probe harness `probe.sh`, kept in scratch, removed with it).

## Revision event (integrity)

The wave-dir file changed under the campaign: revision 1 (sha256
`1da1d76d6df352618104d1ce55e3b1d51d16703c5dac8beef738db3a3a1ba6f6`, 1713 lines) was copied
at campaign start; the builder replaced it with revision 2 (sha256
`bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`, 1734 lines) at
18:44:23 -03:00 — diff 55 changed lines: `--receipt-out` red-run semantics in the header,
widened H4 location-token regex, and an H7 receipt fixed-point loop in `run_suite_report`.
**None of the 14 patch-point texts changed.** The full campaign (baseline, 17 mutants,
restored re-run, 9 probes) was re-executed against revision 2; every verdict identical to
the revision-1 run. `ExecSuiteBuild-3` confirmed FINAL at `bdbd18a3…` mid-campaign; the
wave-dir file re-hashed identical after the campaign.

## Runs (revision 2; mutant sha256 = the exact mutated bytes)

| tag | limb | mutant sha256 | affected case baseline -> mutated | verdict |
|---|---|---|---|---|
| H1-reg-gate | H1 | `ef33ae0f602850deaa155fba8cf980bc76d3158715cd74dec6343c7484bb04a9` | H1 3/3 -> 2/3 | killed |
| H2-count-gate | H2 | `ef8f2ee6aad3291d30f338a6e35902832c90968fa5a8927ddb02d7f9200e568e` | H2 3/3 -> 1/3 | killed |
| H2-fence-gate | H2 | `066ccf35ac769a168a69f1a5ec7c77d6a7e64bdced5c4e9001ba5286fdc1fab0` | H2 3/3 -> 2/3 | killed |
| H3-rows-gate | H3 | `e8febc52064690993c0759fdb9ad2f166f2e012c29441054dfde4e87e62b534e` | H3 2/2 -> 1/2 | killed |
| H4-oversize-cap | H4 | `5c5c491f432d944fb61248cfb5e180331098e040b7ed22842481ec8e4d5abe8c` | H4 3/3 -> 2/3 | killed |
| H4-url-always | H4 | `8f4f85dd316444420198a6ef1883408f69ccb88694067171e78495c7caacbfd7` | H4 3/3 -> 2/3 | killed |
| H5-utc-gate | H5 | `e611138f62a69c257bac19175be6ffd889a323e9e0fd57d94b811f5283e5f192` | H5 2/2 -> 1/2 | killed |
| H5-control-gate | H5 | `3e8a79bb2d051b2b7beeb339603c96a5686622cf9679ee811b4b6589c5ef5039` | H5 2/2 -> 2/2 | **SURVIVED** |
| H6-family-exact | H6 | `37236fa062b1874dd5def3bbec4ddc64fe0f9b5bc1c9cb5a5b9bdd76879ebd55` | H6 4/4 -> 2/4 | killed |
| H6-tolerate-all | H6 | `3cf61ffca2e1e10fbde94cd3bb7d2069beb626de7a751398d38278661b34f0b7` | H6 4/4 -> 1/4 | killed |
| H7-cmp-self | H7 | `287b3648f372e6f50d7c40fd64b935ef04facc124257a9720c648247247b165e` | H7 6/6 -> 6/6 | **SURVIVED** |
| H8-gate-le | H8 | `0c2b6654e4abf8937ca694b6d389c59d4a3946a86f4e2413621f4fa903b8423f` | H8 0/2 -> 0/2 (baseline-broken; probe-judged) | **SURVIVED** |
| H9-add-ge | H9 | `99913e27f6a9d90e4c9933563babd35bf1d025a3766bba921a4d4bf7a4e4bf0e` | H9 5/5 -> 4/5 | killed |
| H9-pure-gate | H9 | `6aa5de6df257ab432990efddbf96d82c2b069bd162a748b357cfc9f61f960f26` | H9 5/5 -> 5/5 | **SURVIVED (benign)** |
| H9c-valid-pure-gates | H9 | `4819b080d5477c3b57da9933edbddff473e3a98aea91cbadc7543665a82c2093` | H9 5/5 -> 2/5 | killed |
| H10-dens-gate | H10 | `28c64daeb487ead4bce8cb1f5a37e58e8853cf8601b6b3fa432231a2575e1404` | H10 3/3 -> 2/3 | killed |
| H10-deleted-gate | H10 | `63c98eb910f9049d376222446e92fb3a44de4d1e3d4bb97b88632ab37e6c85e0` | H10 3/3 -> 2/3 | killed |
| restored | — | `bdbd18a3239c…` (pristine) | all ten case lines identical to baseline | restoration verified |

In every mutant run only the affected case's line changed; all other case lines equalled
baseline (verified per run in the saved outputs).

## Probes (direct check invocation; revision 2 bytes)

```
PROBE h5-forged-h2 script=…/pristine/r40-closure.sh rc=1 payload=source=1,control=7/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected
PROBE h5-forged-h2 script=…/mut/H5b.sh             rc=0 payload=source=1,control=7/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected
PROBE h7-control  script=…/pristine/r40-closure.sh rc=0 payload=sentinel=1,ref=5e985b7…,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1
PROBE h7-control  script=…/mut/H7.sh               rc=0 payload=(identical to pristine)
PROBE h7-reorder  script=…/pristine/r40-closure.sh rc=1 payload=(every shape limb green — cmp is the only red)
PROBE h7-reorder  script=…/mut/H7.sh               rc=0 payload=(identical shape payload)
PROBE h8-stub-green script=…/pristine/r40-closure.sh rc=1 payload=base=10/10,base-exit=1,r39=10/10,r39-exit=1
PROBE h8-stub-green script=…/mut/H8.sh               rc=0 payload=base=10/10,base-exit=1,r39=10/10,r39-exit=1
PROBE h1-readme-only script=…/pristine/r40-closure.sh rc=0 payload=suite=1,digest=1,registry=1,registry-in=readme
```

Probe fixtures: `h5-forged-h2` = the assembled transcript with the H2 payload line replaced
by `zz-forged-h2`; `h7-control`/`h7-reorder` = the canonical receipt built the way
`run_suite_report` builds one (`assemble_transcript ''` -> `h7_inner` -> `assemble_transcript
"$h7val"`), with the reorder variant swapping the H1 and H2 payload lines; `h8-stub-green` =
a fixture tree whose `corpus/instruments/r40-closure.sh` is a stub printing
`closed=10/10 exit=0` and exiting 1; `h1-readme-only` = a tree with the registry row only in
`corpus/instruments/README.md`. The executing suite's bytes were planted into the probe
export so digest limbs bind (probe-only fixture state, under the seat scratch).

## Findings for the L1 (survivors = coverage findings, not contract changes)

1. **M08 (H5 control-count gate).** The selftest's forged fixture tampers only the H3
   payload id, so weakening `[ "$control" -eq 8 ]` is invisible to it (mutants stay 2/2)
   while the probe proves a non-H3 forgery (H2) is then ACCEPTED (pristine rc=1 -> mutant
   rc=0). Fix: add forged-payload fixtures for the other seven ids (or at least one
   non-H3 id).
2. **M11 (H7 cmp clause).** All six H7 fixtures are caught by shape limbs; none isolates
   `cmp`, so killing the byte-identity comparison is invisible to the selftest (6/6 stays)
   while the probe proves a shape-clean reordered receipt is then ACCEPTED. Fix: add a
   reorder fixture (shape-clean, byte-different).
3. **M12 (H8 gates).** H8's fixtures only exercise unresolvable-ref fail-closed
   (`base-exit=2`/`r39-exit=2`); no fixture exercises a green or tampered control, so the
   `-lt 10`/`-eq 1` clauses are ungraded at any ref (selftest inconclusive here — baseline
   0/2 because the export predates the suite). The probe proves a stub suite printing
   `closed=10/10 exit=1` for both controls is then ACCEPTED (pristine rc=1 -> mutant rc=0).
   Fix: add a stub-suite/green-tally fixture. H1's digest limb backstops a stub suite in a
   real export, but the H8 clause itself stays ungraded.
4. **M14 (H9 pure gate) — benign.** `pure=0` implies `valid<declared` by construction (a
   deleted path `continue`s before `valid++`), so the pure gate is redundant given that
   continue and the single-point mutant is equivalent on every reachable tree; the 2-point
   variant M15 (valid+pure) is killed 2/5. No action required; recorded because a
   single-point pure-gate edit is invisible to the selftest.
5. **Observation (no mutation): H1 registry breadth.** `check_h1` sets `reg=1` for a row in
   EITHER `SKILL.md` OR `corpus/instruments/README.md`; measured probe `h1-readme-only`
   shows a tree whose SKILL.md carries no `r40-closure.sh` row passes H1
   (`registry-in=readme`, rc=0). The frozen C1 predicate names "its SKILL.md Gates &
   probes registry row". Tighten the check or widen the predicate wording — L1's call.

## Restoration

- `restored` run (pristine bytes re-run after all mutants): all ten case lines + judge
  lines byte-identical to baseline; the only byte difference in the full outputs is the
  `--work` path embedded in one stderr diagnostic (the H6 unreadable-root fixture's
  `cd: Permission denied` message names `work-baseline` vs `work-restored`);
  sed-normalized `cmp` -> BYTE-IDENTICAL-MODULO-WORK-PATH.
- Wave-dir original re-hashed after the campaign: `bdbd18a3…` (unchanged; the suite under
  test was never modified — every patch landed on a scratch copy).

## Controls / hygiene

- Disk guard green before work: `bash scripts/hyaku/disk-guard.sh status` -> `/fast/scratch/hyaku`
  26%, 602.0G free (re-checked implicitly by the small per-run footprint; each selftest run
  is ~3.5 s and its work dirs live under the seat scratch).
- No tool installed or upgraded (none needed; pacman untouched — paused host-wide; no
  uv/npx/network use).
- No git/jj mutation anywhere; the only writes were the two wave1 files (deliverable +
  this receipt) and the seat scratch. The lane repo, fleet root, sibling lanes and
  `/home/vgpnk/Projects/shokuknow` untouched.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/MutKillList` removed before yield (deliverable
  and receipt copied to wave1 first). No `kasegi-r39*`/`kasegi-r40` sibling survives from
  this seat at filing.

Report: .ufo/waves/round-40/wave1/MutKillList.md
