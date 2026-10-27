# MutFrontierParser — frontier row-counting probe

## Mutant and detector

Scratch-only mutation appended this formatted README row (no admitted knowledge entry exists):

`| F999 | Forged decoy | admitted | corpus/knowledge/not-real.md |`

Detector: `python3 corpus/instruments/frontier-recheck-count.py --root <scratch>/lane` against the integrated tree copied into isolated scratch. This specifically probes the C2 frozen F-row counting predicate (`grep -cE '^\\| F[0-9]+ \\|' corpus/README.md`) and its relationship to the admitted-entry harness; it does not establish the other C2 predicates.

## Output and verdict

Pristine detector output ended `entries=27 pass=27 exit=0` (24 distinct frontier IDs include two entries each under F09/F10/F11, hence 27 rows to evaluate). Mutated output added `FAIL F999 corpus/knowledge/not-real.md ... problems=missing-entry` and ended `entries=28 pass=27 exit=1`.

Verdict: **killed by the integrated harness**, which does not accept the decoy as a passing admitted entry. The simple frozen README regex count itself is nevertheless syntactically vulnerable to counting any matching decoy line; the task's specific counter was the frontier-recheck harness, and its observed behavior is fail-closed. No conclusion about whether an independent census or final C2 claim uses that regex safely.

Observed README pristine hash `557103682e7b040ee1ba521063c674cbab5673a91cfa1080fe21972b1fc512db`; mutated hash was not successfully recorded before the interrupted command (the checksum sidecar contains the pristine hash only). Restored exact README bytes by copying the source lane README back into the disposable scratch clone; final detector rerun returned the pristine ending `entries=27 pass=27 exit=0`. Scratch removed. No tools installed.
