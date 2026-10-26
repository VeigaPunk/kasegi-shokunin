# SKILL.md — round-35 fixture payload (not the lane skill)

Committed test fixture for the C1 closure checks (`corpus/instruments/r35-fixtures/README.md`).
Reproduces the `Gates & probes registry` table shape of the live `SKILL.md`; bytes are pinned.

## Gates & probes registry (fixture excerpt)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| recheck-audit.py | gate | cd <lane> && python3 corpus/instruments/recheck-audit.py | exit 0 clean; 1 failed; undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | `.ufo/waves/round-26/c1-receipt-index.txt` | corpus/ read-only + its own receipt dir | kasegi |
| anchorcheck.py | gate | cd <lane> && python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: exit 0 clean; 1 on a fail class | python3 corpus/instruments/anchorcheck.py --selftest | `.ufo/waves/round-28/c1-receipt-index.txt` | all inputs read-only + its own receipt dir | kasegi |
