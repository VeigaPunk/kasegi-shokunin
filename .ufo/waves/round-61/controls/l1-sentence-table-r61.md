# L1 sentence table — post-count safety net, NOT EntryClaims seat output

The EntryClaims seat returned no report in the settled handoff. L1 read the full S094 capture. This table is a late safety net under R76, not a retroactive pre-count table. Source filename is corpus/source-snapshots/round-61/S094.txt.

| entry assertion | capture lines | verdict |
|---|---|---|
| Dated 2024-Nov-01, credited to Big Sleep team | 13–15 | GROUNDED |
| Naptime evolved into Big Sleep, Project Zero/DeepMind collaboration | 17 | GROUNDED |
| Team reports exploitable SQLite stack buffer underflow | 18 | GROUNDED, attributed, not independently reproduced |
| Reported early October and fixed same day | 18 | GROUNDED |
| Before official release, users not impacted | 18 / Q1 | GROUNDED |
| Recent commits, trivial/documentation changes manually removed | 25 / Q2 | GROUNDED |
| Agent receives commit message/diff, reviews current HEAD for related issues | 25 / Q3 | GROUNDED |
| Team calls variant analysis a better fit than open-ended problem | 24 | GROUNDED as attribution, not a new lane method |
| Case supplies no agent-wide success-rate denominator | bounded 1–125 read | GROUNDED bounded absence, not absence from project elsewhere |
| OSS-Fuzz harness lacked generate_series | 112 / Q4 | GROUNDED |
| Alternative fuzzingshell.c had older unaffected seriesBestIndex | 112 | GROUNDED |
| Team used CLI AFL target, checked generate_series/rowid corpus keywords | 113 | GROUNDED |
| Issue undiscovered after 150 CPU-hours | 113 / Q5 | GROUNDED, not wall-clock hours |
| Results highly experimental | 118 / Q6 | GROUNDED |
| Team says target-specific fuzzer likely at least as effective | 118 / Q7 | GROUNDED |
| Inference of universal agent superiority/fuzzing impossibility rejected | 118 | AGREE with reject; explicit source caveat |
| Source is not permission, program policy or intake route | bounded capture read | Curation scope limitation, not source-authored policy |
| F04/F40/F41 retain principles/tracker/later V8 comparison | corresponding held entries and README rows | Curation boundary; new entry adds dated SQLite case only |

All seven pinned quotes occur once; whitespace word counts 17,17,14,12,9,5,15 (89 total), maximum17. Live second-open byte-identical conversion in controls/l1-source-second-open-r61.txt. Independent source reopening remains owed to non-author closure because ScoutSource delivered no evidence.
