# ExecSelftest — R71 W1: single-limb isolation audit of the ten new selftest cases

Seat: ExecSelftest (executor). Round 71, wave 1. Scope: V70-1 follow-through — do the ten
r71 selftest cases each kill a minimal one-limb mutant of their pinned rule limb?
Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Base rev `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`.
Frozen claims commit `0e260a54b0a670cee2915237ac403d37164c749d` (claims.json + pins-r71.txt read first; no
pin in pins-r71.txt constrains the gate selftest beyond the sha below).

## Environment and pristine baseline (measured)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60 | tar -x -C /fast/scratch/hyaku/kasegi-r71/ExecSelftest/base
$ sha256sum base/corpus/instruments/figure-audit.py
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  base/corpus/instruments/figure-audit.py   # == frozen C1 gate sha
$ python3 --version
Python 3.14.8
$ cd <scratch>/work && HYAKU_SCRATCH=<scratch>/tmp python3 -B corpus/instruments/figure-audit.py --selftest
selftest cases=106 failures=0        # exit 0
```

Mutant method: each mutant restores the pristine gate into a full lane-tree copy at
`<scratch>/work/corpus/instruments/figure-audit.py`, applies ONE exact limb-removal edit
(old string asserted unique), reruns the selftest (same command as above), records exit +
`verdict=fail` case ids. Killed := exit != 0 or failures > 0. EXPECTED_CASES=106 held in
all 15 runs (no run shows the pin line; every tail reads `selftest cases=106`).
Scratch: /fast/scratch/hyaku/kasegi-r71/ExecSelftest (receipts/ has full stdout per run;
removed after this report was written).

## (1) The ten new cases (gate lines 777–796 at 4e33119e)

| case id | derive (one-derive ledger, root = selftest temp fixture) | want |
|---|---|---|
| python-no-option-head-refused | `python3 corpus/instruments/frontier-recheck-count.py` | 2 |
| python-selftest-refused | `python3 corpus/instruments/capture-binding-check.py --selftest` | 2 |
| python-short-o-refused | `python3 corpus/instruments/capture-source.py -o out.txt` | 2 |
| python-output-long-refused | `python3 corpus/instruments/capture-source.py --output out.txt` | 2 |
| python-url-refused | `python3 corpus/instruments/capture-source.py --url file:///dev/null` | 2 |
| python-unknown-head-refused | `python3 corpus/instruments/not-in-census.py` | 2 |
| python-per-script-root-admitted | `python3 corpus/instruments/ok.py --root .` (ok.py = fixture head) | 0 |
| python-per-script-json-path-refused | `python3 corpus/instruments/kill-rule-check.py --json j.json` | 2 |
| python-out-only-refused | `python3 corpus/instruments/capture-source.py --out out.txt` | 2 |
| python-census-covers-instruments | tail check: instruments/*.py − PY_SCRIPT_CENSUS − fixture heads = ∅ | 0 |

(An admitted-but-failing derive in a killed run surfaces as audit exit 1
[upstream exit 2, fixture script absent], i.e. != want — that is the observed kill face.)

## (2) Case → limb → one-limb mutant → result

Mutant edits (each applied alone to the pristine gate):

| id | limb removed | edit |
|---|---|---|
| M01 | PY_HEAD_REFUSED limb `frontier-recheck-count.py` | tuple → `()` |
| M02 | PY_DENIED_ANY element `--selftest` | → `("--out", "--output")` |
| M03 | python_flags_ok short `-o`/`-oVALUE` arm | two lines deleted (fall through to `continue`) |
| M04 | PY_DENIED_ANY element `--output` | → `("--out", "--selftest")` |
| M05 | PY_DENIED_BY_SCRIPT[capture-source] `--url` | → `("--work", "--scratch")` |
| M06 | python_head_ok fail-closed census membership check | 2-line check deleted |
| M07 | per-script scoping `.get(script, ())` | → blanket union of all per-script flags |
| M08 | PY_DENIED_BY_SCRIPT[kill-rule-check] `--json` | → `()` |
| M09a | PY_DENIED_ANY element `--out` | → `("--output", "--selftest")` |
| M09c | python_flags_ok abbreviation arm `flag.startswith(name)` | → `if name == flag:` |
| M10 | PY_SCRIPT_CENSUS entry `density.py` | entry deleted (census completeness pin) |
| M11 | PY_DENIED_BY_SCRIPT[recheck-audit] `--root` | → `("--json",)` |
| M12 | PY_DENIED_BY_SCRIPT[recheck-audit] `--json` | → `("--root",)` |
| M13 | python_flags_ok `--name=value` split | `name = tok` (no split) |

Measured runs (`selftest cases=106 failures=N`; failing case ids verbatim from receipts):

| case | limb pinned | mutant | result |
|---|---|---|---|
| python-no-option-head-refused | PY_HEAD_REFUSED[frontier-recheck-count.py] | M01 | KILLED — `failures=1` exit 1; fail: python-no-option-head-refused (got 1 want 2) |
| python-selftest-refused | PY_DENIED_ANY `--selftest` | M02 | KILLED — failures=1 exit 1; python-selftest-refused (1/2) |
| python-short-o-refused | short `-o` arm | M03 | KILLED — failures=1 exit 1; python-short-o-refused (1/2) |
| python-output-long-refused | PY_DENIED_ANY `--output` | M04 | KILLED — failures=1 exit 1; python-output-long-refused (1/2) |
| python-url-refused | per-script capture-source `--url` | M05 | KILLED — failures=1 exit 1; python-url-refused (1/2) |
| python-unknown-head-refused | census fail-closed allowlist check | M06 | KILLED — failures=1 exit 1; python-unknown-head-refused (1/2) |
| python-per-script-root-admitted | per-script denial scoping (`.get(script,())`) | M07 | KILLED — failures=1 exit 2; python-per-script-root-admitted (2/0) |
| python-per-script-json-path-refused | per-script kill-rule-check `--json` | M08 | KILLED — failures=1 exit 1; python-per-script-json-path-refused (1/2) |
| python-out-only-refused | PY_DENIED_ANY `--out` | M09a | **SURVIVED — exit 0, `selftest cases=106 failures=0`** |
| python-census-covers-instruments | census completeness vs instrument dir | M10 | KILLED — failures=1 exit 2; python-census-covers-instruments (2/0, census_missing=density.py) |

Attribution: every killing mutant failed EXACTLY its target case(s); no run had collateral
failures (all 15 receipts grepped: the only multi-fail run is M11 with the three root cases).

## ISOLATED=9/10

## (3) The surviving case: python-out-only-refused

Measured: M09a (delete `--out` from PY_DENIED_ANY) → exit 0, failures=0. Also survives
M04 (delete `--output`) and M09c (delete abbreviation arm) — all three single-limb mutants
leave it green; the token's refusal rests on any TWO of the three limbs {`--out` element,
`--output` element, abbreviation arm}. Differential probe (segment_ok called directly on
four gate variants, root="."):

```
argv                                            pristine M09a-no-out M04-no-output M09c-no-abbrev
capture-source.py --out out.txt                  refuse    refuse      refuse        refuse
capture-binding-check.py --out out.txt           refuse    refuse      refuse        refuse
capture-source.py --out=out.txt                  refuse    refuse      refuse        refuse
capture-source.py --ou out.txt                   refuse    refuse      refuse        ADMIT
capture-source.py --output out.txt               refuse    refuse      ADMIT         refuse
capture-source.py --output=x.txt                 refuse    refuse      ADMIT         refuse
capture-source.py                                ADMIT     ADMIT       ADMIT         ADMIT
```

Why NO additional case can kill it: under the abbreviation rule (`flag.startswith(name)`),
the denial set of declared flag `--out` is a subset of the denial set of `--output`
(every prefix of `--out` is a prefix of `--output`, and `--out` itself is a prefix of
`--output`), and PY_DENIED_ANY is global to every admitted head. So the M09a gate is
admission-equivalent to the pristine gate for every argv on every script; a selftest case
can only observe admission/exec outcomes, so none can distinguish the mutant from pristine.
Smallest fix is a gate-table change, not a new case: delete the redundant `--out` element
(subsumed by `--output`'s prefix coverage); `python-out-only-refused` then pins the
abbreviation arm's coverage of `--out` and M09c-class mutants kill it. Gate edit belongs to
the C1 authoring seat / L1; not done here (no lane-tree writes outside this report).

## Re-pinned r70 cases (root-space / root-equals / root-abbrev / json on recheck-audit.py)

All four still isolate their limbs now that `frontier-recheck-count.py` is head-refused —
they are pinned on `recheck-audit.py` (gate comment lines 759–760), which is census-admitted,
so the head-refusal cannot mask the flag rule:

| case | limb | mutant | result |
|---|---|---|---|
| python-head-root-space-refused | per-script `--root` (recheck-audit) | M11 | KILLED — (1/2) |
| python-head-root-equals-refused | per-script `--root` + `=`-split | M11 and M13 | KILLED by both — (1/2) each |
| python-head-root-abbrev-refused | abbreviation arm (+ per-script `--root`) | M09c and M11 | KILLED by both — (1/2) each |
| python-head-json-refused | per-script `--json` (recheck-audit) | M12 | KILLED — (1/2) |

M11 measured failing set: exactly {root-space, root-equals, root-abbrev} (failures=3);
python-head-json-refused stayed green under M11 and the root cases stayed green under M12.

## Incidental observations (evidence, no action taken)

1. `PY_DENIED_BY_SCRIPT["frontier-recheck-count.py"] = ("--root", "--json")` is now
   unreachable config: python_head_ok checks PY_HEAD_REFUSED before the flag check, so the
   head is refused before any flag is inspected. Dead weight; harmless.
2. The r70 capture-source out-space/out-equals/out-abbrev cases remain conjunction-pinned by
   their `--url` conjunct: under M09c `--ou out.txt` alone is ADMITTED (probe above) yet
   `python-head-out-abbrev-refused` (`--id x --url file:///dev/null --ou out.txt`) still
   passes because `--url` refuses. Same shape for out-space/out-equals via the surviving
   `--out`/abbrev limbs. Only `python-out-only-refused` was meant to fix this class and it
   does not achieve isolation (section above). Under M04, `--output`/`--output=x` are
   admitted and only python-output-long-refused (no other case names `--output` alone) fails.
3. Tooling: none installed or upgraded (pacman guard honored); host python3 3.14.8 used as-is,
   matching the C1 scope statement ("this host's PATH python3 3.14.8").

## Verdict

ISOLATED=9/10. Missing-case list: `python-out-only-refused` — not fixable by any added
selftest case (admission-equivalence proof above); requires dropping the redundant `--out`
element from PY_DENIED_ANY (or accepting it as a redundancy canary and renaming its claim).
The four re-pinned r70 cases: 4/4 still isolate. No other gap found in the ten-case set:
every case kills exactly its nominal one-limb mutant.
