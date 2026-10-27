# I7 registry parser mutation probe

Probe ref: `ad7147532cb702b0d541d40499874552183d9132`. Scratch: `/fast/scratch/hyaku/kasegi-r41/MutSkillTablePipes` (removed by EXIT trap). Mutated only the exported `SKILL.md` copy, one variant at a time, and called the suite's own `registry_row_state SKILL.md r41-closure.sh` function. A mutation is killed when the target row no longer yields `ok=1`.

## Outcomes

| Mutation | Actual parser output | Verdict |
|---|---|---|
| pristine | `rows=1,cells=10,broken=0,ok=1` | reference |
| blank line directly before suite row | `rows=1,cells=10,broken=1,ok=0` | killed |
| bare pipe appended inside an entry command | `rows=1,cells=11,broken=0,ok=1` | survived; coverage finding |
| leading whitespace in first cell (`|  r41-closure.sh |`) | `rows=1,cells=10,broken=0,ok=1` | survived; coverage finding |
| suite row moved outside contiguous registry table to EOF | `rows=1,cells=10,broken=1,ok=0` | killed |

The two survivors are accepted because the parser splits on every `|` without validating escaped/embedded pipes or exact row cell structure, and trims whitespace before comparing the first cell. This mutation probe does not change the registry contract.

## Bounded detector baseline

Ran `bash corpus/instruments/r41-closure.sh --export-ref ad7147532cb702b0d541d40499874552183d9132 --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work "$S/work" --scratch-root "$S/root"` with `TMPDIR="$S"`. Captured output: exit 1, `I7 payload=mentions=1,rows=1,well-formed=1,table=1,cells=10,broken=0,r40-table=1 closed=1`; overall `closed=10/12 exit=1`. Selftest: `I7 mutants=2/2 positive=pass payload-match=1 verdict=pass`, `selftest cases=12 failures=7`. This is an inconclusive baseline for the whole detector (I2 and I6 positives fail in this host/scratch setup), not evidence of a killed full-suite mutant. The four isolated parser outcomes above are the reproduced I7 behavior.

No package/tool install. No lane tracked files modified. Scratch removed.