# CritDigestSelftest — round 41 falsify

## Counterexample / evidence

Ran the committed `corpus/instruments/r41-closure.sh` against integrated ref `ad7147532cb702b0d541d40499874552183d9132`, in isolated work/scratch under `/fast/scratch/hyaku/kasegi-r41/CritDigestSelftest` (removed after runs). No final Y verification performed.

The requested I2 digest/selftest transcript mutations are present in committed selftest case I2 (`selftest_case_i2`, lines 1717–1747): a payload contradiction is changed, and the fixture moves lines 18 and 19 to reverse selftest case order. Their reproduced detail outcomes were:

```text
selftest detail=I2 mutant=recorded-payload-contradicts rejected=1 limb=payload-match=10/11
selftest detail=I2 mutant=selftest-lines-reordered rejected=1 limb=cmp=0
```

This demonstrates the targeted value-recomputation and order-byte-comparison limbs reject those fixtures. However, requested digest-after-run and duplicate-case mutations are not exercised by this committed I2 case: its five mutations are future timestamp, recorded payload contradiction, summary-only body, foreign ref, and line reorder. No digest mutation or duplicate-line fixture appears in the I2 test body. Thus the requested attack coverage is incomplete; do not treat this run as proving either behavior.

Exact run transcript (`--export-ref ... --work ... --scratch-root ...`):

```text
all-gates v1
export-ref=ad7147532cb702b0d541d40499874552183d9132
suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
time-basis=ref-commit
run-utc=2026-10-27T11:35:28Z
I1 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0 closed=1
I2 payload=receipt=0,sentinel=0,ref=,digest=0,time-basis=0,run-utc=0,not-future=0,header-lines=0,run-lines=0,selftest-lines=0,selftest-verdicts=0,summary=0,closed-line=0,payload-match=0/11,ancestor=0,diff-clean=0,diff-read=ok,i8-match=0,cmp=0,i2-line=0 closed=0
I3 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0 closed=1
I4 payload=records=3,fenced=0,eof=closed,erratum=1,gate=1,tally=1,census=1 closed=1
I5 payload=declared=132,valid=132,tail=132,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok,file=present closed=1
I6 payload=strays=0,read=fail,scanned=0 closed=0
I7 payload=mentions=1,rows=1,well-formed=1,table=1,cells=10,broken=0,r40-table=1 closed=1
I8 payload=control=missed/missed,payload-contradicting=rejected,future-dated=rejected,foreign-ref=rejected,nonexistent-ref=rejected,summary-only=rejected,tampered-payload-line=rejected closed=1
I9 payload=cases=12,isolated=12 closed=1
I10 payload=suite=1,base=3/12,base-exit=1,r40=3/12,r40-exit=1,probe=3/3 closed=1
I11 payload=escapes=8,red=8,F1=red F2=red F3=red F4=red F5=red F6=red F7=red F8=red,pending=0,read=ok closed=1
I12 payload=declared=132,valid=132,tail=132,pure=1,skill-del=0,province-del=0,density=1,deleted=0,census=1,ref-not-found=1,markers=0,neg-red=1 closed=1
selftest case=I1 mutants=1/2 positive=fail payload-match=0 verdict=fail
selftest case=I2 mutants=5/5 positive=fail payload-match=0 verdict=fail
selftest case=I3 mutants=0/1 positive=fail payload-match=0 verdict=fail
selftest case=I4 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=I5 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I6 mutants=4/5 positive=fail payload-match=0 verdict=fail
selftest case=I7 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=I8 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I9 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I10 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I11 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I12 mutants=3/3 positive=pass payload-match=1 verdict=pass
selftest cases=12 failures=7
closed=10/12 exit=1
```

The selftest run (exit 1) was separately captured. It reports the two requested I2 mutations red, but also shows broad independent positive/control failures, including I2 positive `verdict=fail`, I1 and I3 positives failing, I6 positive failing, and `selftest cases=12 failures=6`. Thus I2/I3 are not green at this integrated ref; the suite as a whole is red. The selftest receipt evidence specifically:

```text
selftest detail=I2 positive=fail rc=1 payload=receipt=1,sentinel=1,ref=ad7147532cb702b0d541d40499874552183d9132,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=12,selftest-lines=12,selftest-verdicts=9,summary=1,closed-line=1,payload-match=11/11,ancestor=1,diff-clean=1,diff-read=ok,i8-match=1,cmp=1,i2-line=0
selftest detail=I2 mutant=recorded-payload-contradicts rejected=1 limb=payload-match=10/11
selftest detail=I2 mutant=selftest-lines-reordered rejected=1 limb=cmp=0
selftest case=I2 mutants=5/5 positive=fail payload-match=0 verdict=fail
selftest cases=12 failures=6
```

## Axes and correction

- **depth:verifiability (C1):** targeted order and payload-contradiction attacks are rejected, but I2 graded positive and overall suite are red on this reference; requested digest-after-run and duplicate-case attacks remain untested. No green defect reproduced.
- **coverage (C2):** no direct C2 behavior attacked in this seat; no conclusion on its coverage predicate.

Smallest safe correction: extend I2 selftest with independent fixtures that alter `suite-sha256` after forming an otherwise honest receipt and insert a duplicate graded case line; assert each is individually rejected with its own identified limb. Then rerun in a clean scratch environment and resolve/understand the observed unrelated positive failures before claiming C1 closure.

Verification performed: the two suite invocations above only. No tools installed.