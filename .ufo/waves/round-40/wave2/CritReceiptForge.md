# CritReceiptForge — round 40, wave 2 (critic seat)

Seat: `CritReceiptForge`. Item: attack the r40 receipt — produce forged receipt variants against the committed
suite at Y and verify each is rejected. Milestone: round-40 falsify wave 2 (attack C1 suite/counters).
Axes: **depth:verifiability** (primary), **coverage** (the four required forgery classes are all exercised).

## What is attacked

The C1 closure promise: the committed instrument `corpus/instruments/r40-closure.sh` (sha256
`bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`, H1–H10) must reject forged receipts. The frozen
predicate H5/H7 and the R1/G2 class require rejection of: (a) a recorded payload contradicting the export,
(b) a future-dated `run-utc`, (c) a receipt assembled from a different ref's run, (d) a summary-only receipt
with no per-check lines. Any forged variant that passes (`closed=10/10 exit=0`, or a selftest acceptance) is a
defect and keeps the R1/G2 class open.

## Method

Y = lane tip J (`3074c7679d6f527ec3930d7748ccce1dbae4a58a`, the round-40 judged head J5) + the receipt
`.ufo/waves/round-40/final-gates/all-gates.txt` only (claims `judged_head_rule`; the receipt is untracked at J,
so Y is reconstructed as a fixture repo F = J + committed receipt; `git diff --name-only J F` = the receipt
only, verified). Each suite run:

```
bash <lane>/corpus/instruments/r40-closure.sh --export-ref <F> --lane <F> \
  --work <isolated-scratch-root>/kasegi-r40-forge/work --scratch-root <isolated-scratch-root>
```

Each run gets its own isolated scratch root whose only `kasegi-r39*/r40*` family entry contains the run's
`--work` (`H6 payload=strays=0,read=ok` on every run), so every red limb is attributable to the receipt forgery,
not to host scratch state. Nested H8 negative runs (base `a7af2ce6…`, r39 head `8371e7ac…`) run against the
same fixture lane.

Control runs: the original receipt (F) → `closed=10/10 exit=0`; `--selftest` at F → `selftest cases=10
failures=0` exit=0 with all six forged selftest report shapes rejected.

Disk guard green before the heavy pass (616 G free on /fast/scratch/hyaku). Tooling: none installed or upgraded
(bash 5.3.20, git 2.56.0 preinstalled); no pacman; no network fetches. Lane git used read-only; fixture commits
only inside scratch repos after asserting `git rev-parse --show-toplevel` == the fixture (identity
`-c user.email=r40-fixture@local -c user.name=r40-fixture`).

## Results at a glance

| variant | mutation applied to the committed receipt | fixture sha256 | suite result (exit) | verdict |
|---|---|---|---|---|
| control | none — original committed receipt | `7b8cda36…` | `closed=10/10 exit=0` (0) | accepted — reproduction |
| a | `H1 payload=` rewritten to `suite=0,digest=0,registry=0,registry-in=none` | `3c95bb70…` | `closed=8/10 exit=1` (1) | **REJECTED** |
| b | `run-utc` → `2999-01-01T00:00:00Z` | `82e9c921…` | `closed=8/10 exit=1` (1) | **REJECTED** |
| c1 | `export-ref` → r39 judged head `8371e7ac…`; coherent `run-utc=2026-10-26T20:55:17Z` | `7aa50412…` | `closed=9/10 exit=1` (1) | **REJECTED** |
| c2 | `export-ref` → `0000000000000000000000000000000000000000` (nonexistent) | `13344ea6…` | `closed=9/10 exit=1` (1) | **REJECTED** |
| d | summary-only body: 5 header lines + `closed=10/10 exit=0`, no per-check lines | `4db0606d…` | `closed=8/10 exit=1` (1) | **REJECTED** |
| h7line (bonus) | the `H7 payload=` line alone tampered to `payload=tampered` | `7a348c01…` | `closed=9/10 exit=1` (1) | **REJECTED** |

## Transcript — control

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1 closed=1
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=10/10 exit=0
```

## Transcript — var-a

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=7/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=0
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=7,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=8/10 exit=1
```

## Transcript — var-b

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=0,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=0
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=0,not-future=0,header-lines=4,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=8,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=8/10 exit=1
```

## Transcript — var-c1

```
all-gates v4
export-ref=8371e7ac9f32cae5ed72f8c28205634603f836fa
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T20:55:17Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=8371e7ac9f32cae5ed72f8c28205634603f836fa,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=0,diff-read=ok,payload-match=9,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=9/10 exit=1
```

## Transcript — var-c2

```
all-gates v4
export-ref=0000000000000000000000000000000000000000
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=unreadable
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=0000000000000000000000000000000000000000,digest=1,time-basis=1,run-utc=0,not-future=1,header-lines=4,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=0,diff-clean=0,diff-read=ok,payload-match=9,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=9/10 exit=1
```

## Transcript — var-d

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=0/8,utc=1,forged-payload=accepted,future-dated=rejected,summary-only=rejected closed=0
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=0,body-lines=1,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=0,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=8/10 exit=1
```

## Transcript — var-h7line

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=0 closed=0
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=9/10 exit=1
```

## Transcript — selftest at F (control fixture)

```
selftest export-ref=a67011b25329ae66485b03614dcd62b7295115ce suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
selftest detail=H1 positive=pass payload=suite=1,digest=1,registry=1,registry-in=skill
selftest detail=H1 mutant=suite-absent rejected=1 limb=suite=0
selftest detail=H1 mutant=registry-row-absent rejected=1 limb=registry=0
selftest detail=H1 mutant=export-bytes-differ rejected=1 limb=digest=0
selftest case=H1 positive=pass mutants=3/3 verdict=pass
selftest detail=H2 positive=pass payload=corrections=8,named=5,missing=0,fences=closed
selftest detail=H2 control=four-records-green accepted=1 payload=corrections=4,named=4,missing=0,fences=closed
selftest detail=H2 mutant=lesson-correction-absent rejected=1 limb=missing=1
selftest detail=H2 mutant=values-not-named rejected=1 limb=missing=1
selftest detail=H2 mutant=fence-open-at-eof rejected=1 limb=fences=open
selftest case=H2 positive=pass mutants=3/3 verdict=pass
selftest detail=H3 positive=pass payload=mentions=1,rows=1
selftest detail=H3 control=criterion-row-green accepted=1 payload=mentions=1,rows=1
selftest detail=H3 mutant=row-absent-at-all rejected=1 limb=mentions=0
selftest detail=H3 mutant=mention-without-criterion-row rejected=1 limb=rows=0
selftest case=H3 positive=pass mutants=2/2 verdict=pass
selftest detail=H4 positive=pass payload=s056=1,s058=1,s059=1,oversize=0
selftest detail=H4 control=three-located-quotes accepted=1 payload=s056=1,s058=1,s059=1,oversize=0
selftest detail=H4 mutant=s059-block-absent rejected=1 limb=s059=0
selftest detail=H4 mutant=quote-over-25-words rejected=1 limb=oversize=1
selftest detail=H4 mutant=url-absent rejected=1 limb=s056=0
selftest case=H4 positive=pass mutants=3/3 verdict=pass
selftest detail=H5 positive=pass payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected
selftest detail=H5 control=canonical-source-green accepted=1 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected
selftest detail=H5 mutant=recorded-payload-contradicts-export rejected=1 limb=control=7/8
selftest detail=H5 mutant=source-future-dated rejected=1 limb=utc=0
selftest case=H5 positive=pass mutants=2/2 verdict=pass
selftest detail=H6 control=own-work-dir accepted=1 payload=strays=0,read=ok
selftest detail=H6 mutant=empty-sibling-family-entry rejected=1 limb=strays=1
selftest detail=H6 mutant=r39-sibling-family rejected=1 limb=strays=1
selftest detail=H6 mutant=r40-sibling-family rejected=1 limb=strays=1
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r40-closure.sh: line 770: cd: /fast/scratch/hyaku/kasegi-r40/CritReceiptForge/root-st/kasegi-r40-forge/work/mut/H6-unreadable: Permission denied
selftest detail=H6 mutant=unreadable-scratch-root rejected=1 limb=read=fail
selftest case=H6 positive=pass mutants=4/4 verdict=pass
selftest detail=H7 positive=pass payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1
selftest detail=H7 mutant=receipt-absent rejected=1 limb=receipt=0
selftest detail=H7 mutant=future-dated-run-utc rejected=1 limb=not-future=0
selftest detail=H7 mutant=export-ref-not-ancestor rejected=1 limb=ancestor=0
selftest detail=H7 mutant=suite-digest-mismatch rejected=1 limb=digest=0
selftest detail=H7 mutant=extra-body-line rejected=1 limb=body-lines=12
selftest detail=H7 mutant=h7-line-tampered rejected=1 limb=h7-line=0
selftest case=H7 positive=pass mutants=6/6 verdict=pass
selftest detail=H8 positive=pass payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1
selftest detail=H8 mutant=base-ref-unresolvable rejected=1 limb=base-exit=2
selftest detail=H8 mutant=r39-ref-unresolvable rejected=1 limb=r39-exit=2
selftest case=H8 positive=pass mutants=2/2 verdict=pass
selftest detail=H9 positive=pass payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok
selftest detail=H9 control=declared-whole-tail-green accepted=1 payload=declared=2,valid=2,tail=2,pure=1,paths=1,diff-read=ok
selftest detail=H9 mutant=declared-short-of-added rejected=1 limb=valid=0
selftest detail=H9 mutant=tail-sha-mismatch rejected=1 limb=valid=0
selftest detail=H9 mutant=declared-path-with-deletions rejected=1 limb=pure=0
selftest detail=H9 mutant=declaration-path-escape rejected=1 limb=paths=0
selftest detail=H9 mutant=declaration-absent-path rejected=1 limb=paths=0
selftest case=H9 positive=pass mutants=5/5 verdict=pass
selftest detail=H10 positive=pass payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok
selftest detail=H10 control=append-only-green accepted=1 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok
selftest detail=H10 mutant=density-instrument-changed rejected=1 limb=density=0
selftest detail=H10 mutant=skill-line-deleted rejected=1 limb=skill-del=1
selftest detail=H10 mutant=tracked-path-deleted rejected=1 limb=deleted=1
selftest case=H10 positive=pass mutants=3/3 verdict=pass
selftest cases=10 failures=0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-9-cases rejected=1
selftest judge=forged-no-verdict rejected=1
```

## Which limb reds (discrimination, from the transcripts)

| variant | red checks | reopened limbs |
|---|---|---|
| a | H5, H7 | H5 `control=7/8`; H7 `payload-match=7,h7-line=0` |
| b | H5, H7 | H5 `utc=0`; H7 `run-utc=0,not-future=0,header-lines=4,h7-line=0` |
| c1 | H7 only | H7 `diff-clean=0,h7-line=0` (H5 green: `control=8/8,utc=1`) |
| c2 | H7 only | H7 `ancestor=0,diff-clean=0,run-utc=0,header-lines=4` (H5 green) |
| d | H5, H7 | H5 `control=0/8,forged-payload=accepted,summary-only=rejected`; H7 `run-lines=0,body-lines=1,payload-match=0` |
| h7line | H7 only | H7 `h7-line=0` |

## Findings

1. **No forged variant reached `closed=10/10 exit=0`.** All four required classes — (a) payload contradiction,
   (b) future-dated `run-utc`, (c) receipt from a different ref, (d) summary-only body — are rejected with
   `closed<10/10 exit=1`. The R1/G2 class is **CLOSED**. Green re-run evidence is recorded too (control 10/10;
   selftest 10/10 failures=0, six forged selftest reports rejected).
2. **Observation (not a defect):** on the summary-only source (d), H5's `forged-payload` field reads
   `accepted` because there are no payload lines to drop below its own `control=0`; H5 still reds via
   `control=0/8` and `summary-only=rejected`, and H7 catches `run-lines=0`. The check fails correctly even where
   one sub-field reads misleadingly.
3. **Observation:** receipt provenance (ref binding) is enforced only by H7 (`ancestor`/`diff-clean`/
   `payload-match`); H5 legitimately covers content-level forgery. Variant c1 shows the coherent foreign-ref
   forgery (every content line truthful, timestamps consistent with the claimed ref) is caught solely by H7's
   `diff-clean=0` — the ancestry/diff binding is the load-bearing provenance guard. c2 confirms a nonexistent
   ref also reds (`ancestor=0`).
4. **Determinism confirmed:** the control run's printed transcript is byte-identical to the committed receipt
   (same sha256 `7b8cda36…`), matching the H7 `cmp` contract.

## Byte-exact artifacts delivered beside this receipt

`CritReceiptForge.control-original.txt`, `.variant-a-forged-payload.txt`, `.variant-b-future-utc.txt`,
`.variant-c1-foreign-ref-r39.txt`, `.variant-c2-nonexistent-ref.txt`, `.variant-d-summary-only.txt`,
`.variant-h7line-tampered.txt` (the exact bytes fed to the suite), plus `.transcript-*.txt` (verbatim
stdout+stderr of every run, including the selftest).

## Conduct

- Writes: only this receipt and the listed fixtures in `wave2/`; scratch `S=/fast/scratch/hyaku/kasegi-r40/CritReceiptForge` removed before yield.
- Lane git read-only (`rev-parse`, `log`, `status`); no mutating git/jj on the lane; no writes to fleet root or `/home/vgpnk/Projects/shokuknow`.
- No network fetches; no tools installed/upgraded; pacman untouched.
