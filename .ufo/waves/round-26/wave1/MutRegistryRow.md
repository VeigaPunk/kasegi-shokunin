# Registry row mutation probe

Axis: depth:verifiability. I read the frozen C1 counter from `.ufo/waves/round-26/claims.json` and used a scratch-only synthetic canonical row, since the counter measures a future `gate|probe` row. Pristine scratch count was `1` (exit 0). The command was `grep -cE '^\| [^|]+\| gate\|probe '`.

Results in `.ufo/waves/round-26/c1-controls/m2-registry-mutants.txt`:

| Mutant | grep stdout / exit | Detector result |
|---|---:|---|
| Omit verdict map | `1 / 0` | Survives; count still corresponds to one row |
| Change type to `gate` (omit `|probe`) | `0 / 1` | Detected; count no longer corresponds to the row |
| Spell flag `--self-test` | `1 / 0` | Survives |
| Omit pinned-value path | `1 / 0` | Survives |
| Typo instrument name (`recheck-audti.py`) | `1 / 0` | Survives |

The grep counter deterministically detects the missing `|probe` marker only. It does not establish row correctness for the other four properties. These are counter-coverage findings, not proposed changes to the frozen contract.

Real `SKILL.md` was read-only; its observed SHA-256 was `fa09d5b835451f2443fc96353432a330608baf5f3631d1b382141f7e86d64f2d`. No tool installation or production edit was made.