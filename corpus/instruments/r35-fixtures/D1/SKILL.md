# SKILL.md — round-35 fixture payload (not the lane skill)

Committed test fixture for the C1 closure checks (`corpus/instruments/r35-fixtures/README.md`).
Reproduces the `Gates & probes registry` table shape of the live `SKILL.md`; bytes are pinned.

## Gates & probes registry (fixture excerpt)

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r-defect-closure.sh | gate | cd <lane> && bash corpus/instruments/r35-defect-closure.sh [--root DIR] | exit 0 iff `closed=7/7`; 1 while any round-34 verifier defect D1-D7 is open | cd <lane> && bash corpus/instruments/r35-defect-closure.sh --selftest -> `selftest cases=7 failures=0` | `.ufo/waves/round-35/wave1/R35Closure.md` | all inputs read-only + its own receipt dir | kasegi |
| kill-rule-check.py | probe | cd <lane> && python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH] | exit 0 iff a `--fake` instrument is rejected; 1 when the fake passes | python3 corpus/instruments/kill-rule-check.py --selftest | `.ufo/waves/round-34/wave1/ExecKillRuleCheck.json` | all inputs read-only + its own receipt dir | kasegi |
