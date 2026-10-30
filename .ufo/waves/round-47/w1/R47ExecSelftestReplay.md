# R47ExecSelftestReplay

## Result
- Fresh base export from `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; selftest reproduced `selftest cases=43 failures=0 exit=0` (selftest process exit 0). The committed control at `.ufo/waves/round-47/controls/selftest-receipt.txt:44-45` reports the same result.
- `r47-mutbat.py --counter both --list` exited 0 and emitted 56 listed mutation triples (35 c1, 21 c2); this is listing only, not a battery execution or evidence that survivors are caught. Independent anchor check reported `anchors total=56 bad=0`, every old substring occurs exactly once in its counter. `r47-mutbat.py` documents that mutation application asserts exact-once (`corpus/instruments/r47-mutbat.py:16-21`); the independent check is recorded in the anchor log.
- Do-nothing control: unmutated fresh base was used for the green selftest cases; receipt lines 1 and 21 show c1 and c2 clean-target outputs. No claim that counter mutations were tested for detection here.

## Evidence files
- `R47ExecSelftestReplay-selftest.txt` — full reproduction output.
- `R47ExecSelftestReplay-mutbat.txt` — complete mutation listing.
- `R47ExecSelftestReplay-anchors.txt` — all 56 exact-once anchor counts.

Commands: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 | tar -x -C <fresh scratch>/base`; then `python3 .../r47-counters-selftest.py --base <base> --work <scratch>/st --counter both` and `python3 .../r47-mutbat.py --base <base> --work <scratch>/mb --counter both --list`. Scratch was removed after copying logs. No installs, mutations, builds, linters or tests beyond this assigned selftest were run.

## Limitation
The `--list` invocation is not the full mutation battery; known pre-freeze receipt remains 35/19/16 for c1 and 21/3/18 for c2 (35/21 mutants, caught/uncaught), with 34 known survivors. No assertion of uncaught=0 is made.