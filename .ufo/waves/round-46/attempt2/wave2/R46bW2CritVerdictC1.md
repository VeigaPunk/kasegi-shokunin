VERDICT: BLOCKED

## Findings

1. **`claims.json` C1 axis/surface — label is appropriate.** C1 names `depth:verifiability` and changes the C1 selftest/mutation-grading surface, not the corpus admission surface (C2 coverage). I re-derived the integrated C1 selftest from an archive of `96379ae26ef9443097b860ddb33ef924b2cd5b5a`:
   ```
   python3 -B corpus/instruments/r46-counters-selftest-c1.py --pure <pure> --work <scratch> --jobs 8
   case TIP-7of7 ... fixed=7/7 exit=0 ... verdict=OK
   case CONTROL-do-nothing ... fixed=1/7 exit=1 ... verdict=OK
   ...
   selftest cases=83 failures=0
   ```
   This matches committed `wave1/R46bExecSelftestC1.md` (`selftest cases=83 failures=0`) and discriminates the do-nothing selftest control. It verifies the selftest after-value only, not the battery summary.

2. **`claims.json` C1 after-value / `controls/final-battery.txt` — no committed after battery receipt.** Read-only `git show -s` gives `fe0f56b...` subject `... freeze claims ... counters v1 ...`; the later `96379ae...` subject identifies the wave-1 integration (`selftests 83/147, mutbat v1.1`). `git cat-file -e <rev>:.ufo/waves/round-46/attempt2/controls/final-battery.txt` reports it absent at both revisions. At `96379`, committed `wave1/R46bExecPlain.md` leaves `F9` as `BATTERY_PLACEHOLDER`. The only local `controls/final-battery.txt` is not committed and stops at line 10, `== battery c1:`; before that it records `NameError: name 'C1_ENTRIES' is not defined` for the C2 selftest and `exit=0`. It contains no C1 battery summary. Thus I cannot confirm that the claimed `uncaught=0` after-value is what a committed receipt prints.

3. **`controls/mutbat-before.txt` / base no-op control — independently reproduced.** I archived base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` and the frozen battery from `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`, set `TMPDIR` to my scratch, and ran `python3 -B corpus/instruments/r46-mutbat.py --root <base-export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>/work/c1-base --counter c1 --jobs 8`. It printed `mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught` and the other six named uncaught mutants from the receipt, then `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0` (process exit 1). This matches the committed receipt's C1 summary and confirms the do-nothing base does **not** reach uncaught=0. The receipt SHA-256 is `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`, as claimed. The C2 half of the before receipt was not rerun in this C1 seat.

## Weakest link and correction

Weakest link is **freeze → after**: the supplied attack hash is the claims-freeze commit, while the later wave-1 integration has no committed complete C1 battery output. Pin freeze and integration as distinct revisions, then commit a complete C1 battery receipt (command, revision/tool hashes, both summary lines and process exit) from the integration tree. Do not treat the partial, untracked `final-battery.txt` as evidence; make the measurement fail closed on the recorded selftest exception.

## Limitations

The full C1 after-battery run was not completed; no after battery summary is claimed as independently reproduced. I re-derived the integrated C1 selftest (`83 failures=0`) and the full base C1 battery above. No C2/source/live-page audit was performed in this seat. Scratch was removed; no shared instrument or git/jj state was modified.