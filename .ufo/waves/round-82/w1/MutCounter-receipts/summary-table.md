# r82 counter mutants — summary (seat MutCounter, round 82 attempt 1)

Mutants of `.ufo/waves/round-82/c1/mutbat.py` (sha256 a7d4db43…). Detectors: **P9** = counter
`--selftest`; **P4** = frozen `controls/c1-forgeries-r82.py`, r82 counter path pointed at the
mutant (F6/F7 r82 rc; 1 = forgery rejected); **P3** = frozen candidate + frozen 63-row table,
`--expect-cases 24` (rc; `ok` = summary line ends with the frozen P3 suffix
`… neutral_ok=3/3 decoy=ok decoy_hidden=59/60`). `p3-line` = rc 0 but the printed line differs.

| id | change | selftest rc | F6 r82 | F7 r82 | P3 rc | hidden | verdict |
|---|---|---|---|---|---|---|---|
| MC00 | (pristine base) | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC01 | drop-D2-exec | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC02 | drop-D1-exec | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC03 | return-d1-twice | 0 | 1 | 1 | 0 | 39/60 | killed:p3-line |
| MC04 | hidden-ge-0 | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC05 | decoy-term-forced-True | 1 | 0 | 0 | 0 | 59/60 | killed:selftest+forgery |
| MC06 | run_decoy-returns-True | 1 | 0 | 0 | 0 | 59/60 | killed:selftest+forgery |
| MC07 | rename-args-guard-inverted | 1 | 1 | 1 | 1 | - | killed:selftest+p3-rc |
| MC08 | rename-includes-module-names | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC09 | rename-includes-keywords | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC10 | rename-skips-except-as | 0 | 1 | 1 | 1 | 59/60 | killed:p3-rc |
| MC11 | hidden-counts-neutral | 1 | 1 | 1 | 0 | 61/60 | killed:selftest+p3-line |
| MC12 | hidden-threshold-2 | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC13 | hidden-from-D1-only | 0 | 1 | 1 | 0 | 39/60 | killed:p3-line |
| MC14 | decoy-accumulator-or | 1 | 0 | 0 | 0 | 59/60 | killed:selftest+forgery |
| MC15 | D2-not-renamed | 0 | 1 | 1 | 0 | 39/60 | killed:p3-line |
| MC16 | parse-failure-as-ok | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC17 | clean-pass-drops-traceback | 0 | 1 | 1 | 0 | 59/60 | SURVIVED |
| MC18 | rename-skips-args-clean | 0 | 1 | 1 | 0 | 57/60 | killed:p3-line |
