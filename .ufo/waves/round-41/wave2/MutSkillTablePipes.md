# MutSkillTablePipes — I7 registry parser

Probe ref: `ad7147532cb702b0d541d40499874552183d9132`. The full outcomes, exact parser outputs and detector transcript are in [MutSkillTablePipes.findings.md](MutSkillTablePipes.findings.md).

| Probe | Result |
|---|---|
| Blank line before suite row | Killed: `ok=0`, `broken=1` |
| Bare pipe within entry command | Survived: `ok=1`, `cells=11` |
| Leading whitespace in first cell | Survived: `ok=1` |
| Row moved outside contiguous table | Killed: `ok=0`, `broken=1` |

The parser therefore fails to enforce exact row-cell structure and first-cell whitespace strictness. The full detector baseline was inconclusive overall: exit 1, `closed=10/12`; its I7 check passed and I7 selftest was `2/2`, while unrelated I2/I6 positives failed. These results report the isolated I7 parser probes, not final Y verification.

Scratch directory was removed. No tools installed.