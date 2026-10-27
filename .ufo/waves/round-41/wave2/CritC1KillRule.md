# CritC1KillRule — round-41 falsify receipt

Axes: depth:verifiability (primary), coverage. Attack run used the integrated instrument copied from `wave1/ExecSuiteCore.r41-closure.sh`, export ref `ad7147532cb702b0d541d40499874552183d9132`, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, scratch `/fast/scratch/hyaku/kasegi-r41/CritC1KillRule` (removed by shell trap). No installs or network. No lane writes beyond this receipt; no git mutation.

## Reproduced counterexample

Command:

```sh
bash ./suite.sh --selftest --export-ref ad7147532cb702b0d541d40499874552183d9132 --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work "$S/work" --scratch-root "$S"
```

Transcript (complete selftest output was captured in scratch; relevant lines):

```text
selftest export-ref=ad7147532cb702b0d541d40499874552183d9132 suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
selftest detail=I1 positive=pass payload=records=3,lines=14,graded=3,evidence=3/3,missing=0
selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0
selftest detail=I3 positive=pass payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
selftest case=I1 mutants=1/2 positive=fail payload-match=0 verdict=fail
selftest case=I3 mutants=0/1 positive=fail payload-match=0 verdict=fail
selftest cases=12 failures=6
```

This is a live defect: the I1 fixture removing the named evidence is *not rejected* (`rc=0`, same green payload); the I3 mangled-value-token defeat likewise is not rejected (`rc=0`, same green payload). I1/I3 selftests detect their own inadequate defeat fixtures, so the overall selftest appropriately exits 1, but the committed checks themselves accept the defect state. This directly violates C1's kill rule (a committed fixture/check pair can green while the named defect is present) and makes the instrument's positive coverage claim unreliable. Smallest safe correction: make the I1 evidence limb require every specific named source identifier and make its negative fixture mutate/remove those exact names; correct I3's mutant to use the actual token boundary form and require a changed canonical payload plus red verdict. Then rerun the complete selftest.

## Other attack classes / limits

The same selftest reported the round-40 scoped classes working for T4 fenced row (`I4 ... rejected=1`), T7 declared path escape (`I5 ... rejected=1`), T13 mention-only registry row (`I7 ... rejected=1`), H1-H5 count-relative forgery (`I8 ... rejected=1`), H6/H10 leaf-capped base (`I10 ... rejected=1`), and all eight CritKillRule escape probes (`I11 ... escapes=8,red=8`). I6 positive failed in this invocation because the scratch-root scan observed `strays=3,read=fail,scanned=11`; this is not a valid green baseline and I do not claim the T14 attack as a clean pass/fail falsification. I did not separately mutate and execute T2/T14 against isolated copies, nor complete three new independently validated constructions; the suite's own I3 mutant was a reproduced survivor, not a substitute for those unexecuted runs. Therefore the full requested attack matrix remains incomplete.

The principal defect is in depth:verifiability; coverage is impacted because the green I1/I3 fixtures do not demonstrate the claimed defect detection. No final J/Y verification is claimed. Tool installs: none.