# RevC1Counters — C1 falsification

## Ref boundary

The requested final Y does not exist yet: `.ufo/waves/round-41/final-gates/all-gates.txt` is absent, and the assignment explicitly says the final J/Y are created after this falsify wave. I did **not** claim or run a final-Y verification. I ran the exact counters against the supplied integrated scratch-probe ref `ad7147532cb702b0d541d40499874552183d9132` using its committed `r41-closure.sh`, with private scratch/work paths. This is a falsification probe, not acceptance of Y. No lane files were written. The lane worktree was already modified/untracked when observed (`wave2-extra-items.json` modified; wave2 dispatch/spec/ready files and `wave2/` untracked); I left those untouched.

## Actionable findings

1. **I3 selftest accepts a token-boundary defeat.** In the reproduced integrated-ref selftest, the detail was `selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0`; the I3 case consequently reports `mutants=0/1 ... verdict=fail`. This is a live kill-rule escape, not an environment-dependent positive: `selftest_case_i3` replaces a correction value with `closed=10/100` (instrument lines 1757–1759), but the I3 grader still reports all three tallies valid. The frozen T2/token-boundary claim therefore is not established at this ref. The independent limb is `value_present` (438–459), and the check's record tally is at 960–980; this observed false acceptance needs fixing before C1 can be considered closed.
2. **I1 selftest does not enforce evidence naming at the correction under test.** Reproduced detail: `selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0`; I1 reports `mutants=1/2 ... verdict=fail`. The fixture removes evidence from one correction, yet the aggregate `evidence=3/3` stays green because evidence is collected as a cross-record union (`check_i1`, lines 902–906). This does not establish the per-block evidence requirement described in the build requirements; the test itself proves the intended mutation survives.

## Reproduced counter transcripts (integrated ref only)

Suite (`--export-ref ad7147532cb702b0d541d40499874552183d9132`, `--work` and `--scratch-root` inside the seat scratch):

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
I6 payload=strays=3,read=fail,scanned=3 closed=0
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
selftest case=I6 mutants=5/5 positive=fail payload-match=0 verdict=fail
selftest case=I7 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=I8 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I9 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I10 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I11 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest case=I12 mutants=3/3 positive=pass payload-match=1 verdict=pass
selftest cases=12 failures=6
closed=10/12 exit=1
[observed exit=1]
```

The re-run selftest also emitted the two escaped-mutant detail lines above; full case/detail output was captured by the tool transcript. It ended `selftest cases=12 failures=6` and exit 1. I2's positive fails here because the final receipt is not present at the supplied integrated ref; I6's positive is host-scratch dependent (the prescribed scratch root is live). Neither is represented as a final-Y failure.

Base negative (corrected frozen 40-hex base): `closed=4/12 exit=1` (observed exit 1). Round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd`: `closed=4/12 exit=1` (observed exit 1). Both are red, as required; the base suite reports `I10 payload=suite=0,base=?,r40=?,probe=0/3` because the base export lacks the r41 suite. Plain run emitted `r41-closure: refusing to run against the live worktree: this suite is export-mode only.` and the `pass --export-ref ...` instruction; observed exit 2.

## Plain-read re-derivation of export facts

I extracted the integrated-ref archive into scratch and checked the named facts without using the lane gate's payload computations:

- **I1:** each of SCORECARD.md, LOG.md, SHONEN.md has outside-fence `Correction (round 41)` lines; the union of those lines contains all three evidence names `RevC1Counters`, `CritKillRule`, `MutH6H10`. This accounts for the observed aggregate `records=3,graded=3,evidence=3/3`; the I1 mutant above demonstrates that the aggregate does not prove every corrected block bears the evidence.
- **I2:** export contains no final-gates receipt, consistent with `receipt=0` and zero receipt structure fields. Thus no Y receipt/transcript can be re-derived at this pre-Y ref.
- **I3:** transcript's `exact=2/2,substring=2/2` is not sufficient: the I3 selftest provides the contrary counterexample recorded above (`closed=10/100` still tallies 3/3).
- **I4:** run reports three records, no fenced correction matches, closed fences, and erratum/gate/tally/census evidence all present. (These are the instrument's exported-tree-derived values; no independent line-by-line claim of the receipt at Y.)
- **I5:** declared-blocks file has 132 lines/132 parsed records; the run reports valid=tail=132, zero malformed/deletions, safe paths and canonical roots. The plain check over each declared path's last N lines found no hash mismatch.
- **I6:** `strays=3,read=fail,scanned=3` was produced with this seat's live scratch configuration and is not a commit property; it cannot support a final-Y payload.
- **I7:** plain `grep` finds the `r41-closure.sh` entry at `SKILL.md:1129` inside the registry table; the run reports one mention/row, well-formed, 10 cells, unbroken table. This is consistent with the payload.
- **I8:** payload lists all six forgery classes as rejected, with control missed/missed; this is generated fixture behavior, not a tree fact independently established by counting committed content.
- **I9:** payload reports 12 cases isolated; actual selftest case itself passes its mutation on this run, but positive does not pass because of the absent Y receipt/host root causes described above.
- **I10:** payload records nested base/r40 tallies 3/12, both exit 1, and probe 3/3; consistent with the explicit negative runs (which return 4/12 under the outer counter) and the I10 selftest mutation passing.
- **I11:** the exported fixture file is graded as eight committed F1–F8 escape states; run reports red=8 and pending=0. This matches the frozen erratum correcting the prose count to eight.
- **I12:** independently hashed exported `corpus/instruments/density.py`: `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`, identical to the base blob's hash. Declared blocks are 132/132 and hash-verified. Sources census command against the lane emitted only standing W04 S028/S029 and `kasegi ok`; exit 0. The run reports no tracked deletions, `ref-not-found=1`, no markers, negative controls red. These observations agree with the listed values; the census was run on the lane because that tool resolves its configured lane under the fleet root.

The `--selftest` output for the integrated ref included 12 graded case lines and `selftest cases=12 failures=6` (not a passing final transcript); the complete tool output includes all detail and judge lines. Exact requested **final-Y** run/selftest transcripts, and a final-Y receipt comparison, remain unavailable by construction until the post-wave Y exists.

Scratch was removed before filing (`scratch_absent=1`). No tools were installed.