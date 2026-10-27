# RevScanOwnership — I6/I11 ownership and F1–F8 replay

## Result

No F1–F8 escape survived the integrated suite at `ad7147532cb702b0d541d40499874552183d9132`. With an isolated, empty scratch root, the suite emitted:

```
I6 payload=strays=0,read=ok,scanned=0 closed=1
I11 payload=escapes=8,red=8,F1=red F2=red F3=red F4=red F5=red F6=red F7=red F8=red,pending=0,read=ok closed=1
selftest case=I6 mutants=5/5 positive=pass payload-match=1 verdict=pass
selftest case=I11 mutants=1/1 positive=pass payload-match=1 verdict=pass
```

The I11 aggregate is exact evidence for all eight fixture states, but the current output does not expose a separate per-F payload line. The committed fixture specifications name these expected red payloads: F1 `strays=1,read=ok`; F2 `strays=2,read=ok` (or at least one stray); F3 `strays=1,read=ok`; F4 `strays=3,read=ok`; F5 `strays=1,read=ok`; F6 `strays=0,read=fail`; F7 `pending>=1`; F8 dirty-state detection for skip-worktree, assume-unchanged, and ignored-file cases. Their controls are specified in `wave1/ExecI11KillRule.fixtures.txt` lines 26–206.

## Ownership review

`wave1/ExecSuiteCore.r41-closure.sh` defines its own `scan_scratch` at lines 630–667. F1–F6 in its I11 probes (lines 1415–1463) directly call that function; they do not invoke the standalone `wave1/ExecI6Scan.sh` module. F7 checks pending-marker spellings and F8 checks git working-tree cleanliness (lines 1465–1503), not scratch scanning. The I6 suite limb separately invokes the in-core scan implementation. Thus I11 is a separate *fixture/call-site* defense, but not an independent scanner implementation: scanner logic is duplicated in the closure suite and the standalone I6 module. This is concrete drift risk, not a demonstrated surviving escape. The design report `wave1/MutDesign.md` lines 127–133 describes intended dual ownership; its wording should not imply that F7/F8 overlap I6.

The clean-root run and I11 selftest show the I11 fixture set closes all eight committed states; I6's own clean-root selftest passes all five cases. I did not successfully execute a byte-mutated suite with I6 disabled, so I cannot claim an end-to-end disable-I6 attack was reproduced. In particular, the I11 payload proves the I11 aggregate in the unmutated run, not that disabling the I6 limb still yields a passing suite. No unowned F1–F8 survivor was observed; the disable-I6 independence claim remains unverified by this seat.

## Reproduction context / caveat

The initial full run accidentally put a family-named `kasegi-r41` entry beneath its configured scratch root. That intentionally/accidentally contaminated run reported `I6 payload=strays=1,read=ok,scanned=1 closed=0` and `I11 ... red=8 ... closed=1`; its I6 selftest positive failed because the fixture root was not clean. I corrected the root and reran the normal suite at the same integrated ref. The corrected run had I6 green and I11 green, but still returned exit 1 because the commit has no final receipt yet: `I2 ... closed=0`, final `closed=11/12 exit=1`. This is pre-final falsify evidence, not a claim about Y.

The first run's selftest was likewise contaminated and is not represented as a valid selftest result. It did show `selftest case=I11 mutants=1/1 positive=pass payload-match=1 verdict=pass`; corrected normal run did not include a selftest rerun. No final-Y verification is claimed.

No actionable F1–F8 fixture survivor was found. Residual risk is duplicated scan logic and the unexecuted disable-I6 mutation. No unowned survivor identified.
