
## Round 39 result

| axis | before | after | evidence |
|---|---|---|---|
| depth:verifiability | 4 | 4 held | `corpus/instruments/r39-closure.sh` export suite, receipt `.ufo/waves/round-39/final-gates/all-gates.txt` |

judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt

The base export is red: `bash corpus/instruments/r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a -> closed=2/8 exit=1` (transcript `.ufo/waves/round-39/final-gates/reds.txt`).

Correction (round 39): the round-38 section's 8/8 quote (`f06148c6` tip run) is report-only — the
committed receipt records `closed=7/8 exit=1` at that judged head, and the 8/8 run and selftest ran
over run-ref `7dd2fcd6`, not over J.
