# SentinelGate — R70 C1 admission-parity / widening audit

Seat: SentinelGate (leaf; no dispatch, no lane writes). Lane read-only; all work in
`/fast/scratch/hyaku/kasegi-r70/SentinelGate` (removed at yield).

Inputs, all fetched from committed bytes with `git -C <lane> show|archive|clone`:

| object | source | sha256 |
|---|---|---|
| base gate | `e74ba6b5:.ufo/waves/round-70/controls/base-gate-r70.py` | `c09b0fb1…d882bde` |
| candidate gate | `c1051749:corpus/instruments/figure-audit.py` | `7a8d52eb…cee59b5` |
| candidate gate copy | `e74ba6b5:.ufo/waves/round-70/controls/candidate-gate-r70.py` | `7a8d52eb…` (identical to the c1051749 export) |
| ledger | `c1051749:corpus/instruments/figure-audit-ledger.json` | 35 figures |
| full tree | `git clone` of the lane, detached at `c1051749` (`rev-parse --show-toplevel` = the clone) | 1132 committed `derive` strings |

Method: both gates loaded as modules from scratch copies (no execution of the gates'
derives for the parity sweep — `check_read_only(root, cmd)` only, i.e. `parse_derive`).
Root for the sweep = the clone at `c1051749` (real counter paths resolve), plus a
`fixture-root` holding the selftest's `g.txt` / `corpus/instruments/ok.py`.

## 1. Disagreement set

**`measurements=482  ADMITTED_NOW=0  REFUSED_NOW=189`**

Corpus: 35 ledger derives + 90 selftest derives (AST walk of `run_case`/`_one`/
`SELFTEST_LEDGER_*` in *both* gates) + 357 assembled variants (denied flags × spellings,
read-only heads, every instrument counter with its own `add_argument` CLI).

Structural reason ADMITTED_NOW is empty, not merely empty in this sample: the diff adds
exactly one limb, `if not python_flags_ok(parts[2:]): return False` inside
`python_head_ok`. `inspect.getsource` comparison of both modules:

```
tokenize identical=True   denied_flag identical=True   git_show_operands_ok identical=True
segment_ok identical=True  parse_derive identical=True   run_derive identical=True
python_head_ok identical=False
DENIED_FLAGS identical: True   READ_ONLY_HEADS identical: True
EXPECTED_CASES base=86 cand=96
```

The change is a monotone narrowing of one head; no code path gained admission.

### REFUSED-NOW by class (189)

| class | n | what |
|---|---|---|
| selftest pins | 7 | `s-pyroot`, `s-pyrooteq`, `s-pyrootab`, `s-pyout`, `s-pyouteq`, `s-pyoutab`, `s-pyjson` (the claim's P1–P7) |
| flag-space / flag-equals | 7 + 7 | each of the 7 denied names |
| flag-abbrev-space / -equals | 24 + 24 | every proper prefix, both spellings |
| flag-quoted / -in-pipeline / -second-segment / -not-first-token | 7 + 7 + 7 + 7 | placement variants of the 7 names |
| short-o | 5 | `-o`, `-oout.txt`, `-o=out.txt`, `-oout`, `-ox` |
| short-dash-dash-o / -eq | 1 + 1 | `--o`, `--o=out.txt` |
| near-miss | 2 | `--root=`, `--root==` (name before `=` is `--root`) |
| counter-doc | 51 | one row per (counter, documented denied flag) — §3 |
| counter-all | 32 | one row per counter whose whole documented CLI carries a denied flag (synthetic: joins every `add_argument` with a `VAL`) |

Exact abbreviation names refused (24): `--root`: `--r --ro --roo` · `--out`: `--o --ou` ·
`--output`: `--o --ou --out --outp --outpu` · `--json`: `--j --js --jso` ·
`--scratch`: `--s --sc --scr --scra --scrat --scratc` · `--url`: `--u --ur` ·
`--work`: `--w --wo --wor`.

Admitted and checked to stay admitted (not in the refused set): `--roots`, `--outputs`,
`--works`, `--urls`, `--jsons`, `--scratches`, `--rootx`, `---root`, `--`, `-`, `--=x`,
`-O`, `-r`, `-v`, `-vo` (a bundle not starting with `o`), and every read-only head with
`--` (`sort --root g.txt`, `grep --root x g.txt`, `cat --output g.txt`,
`git show --work HEAD:g.txt` — non-python heads untouched).

Quoting does not evade: the rule runs on the decoded argv, so `--r\oot`, `--ro\ot`,
`'--root'`, `"--root"`, `--'root'`, `-\o` are all refused (base admitted all six).

## 2. Each REFUSED-NOW: is the same value still derivable by an admitted spelling?

| refused shape | same value by an admitted spelling? | evidence |
|---|---|---|
| `--root <lane>` for the **8** counters whose default already is the gate's cwd (lane root) | **yes** — omit the flag. `run_derive` executes with `cwd=root` (gate:223); defaults: `capture-binding-check.py:1110` dirname³, `frontier-recheck-count.py:494` dirname³, `gate-quote-audit.py` `parents[2]`, `kill-rule-check.py:141` `LANE_ROOT` dirname³, `limb-mutation-check.py:805` `lane_root_from_script()`, `score-gap.py`, `recheck-audit.py:413` `os.getcwd()`, `r46-c1-gate.py:352` `"."` | source read; `python3 corpus/instruments/frontier-recheck-count.py` parses admitted under both gates |
| `--root` for the **2** counters defaulting to `corpus/` (`citation-ground-check.py:82` `ROOT=dirname(HERE)`; `shonen-shipped-fixture-check.py:35` `DEFAULT_ROOT=dirname(HERE)`) | **no** at the lane root — the default is `corpus/`, not the lane | source read |
| `--root`/`--work` for the **11** counters where it is `required=True` or `ap.error`s when absent (`r44-frontier-count.py:369`; `r44-routed-defects`, `r45-c2-gate`, `r45-routed-defects`, `r46-c2-gate`, `r46-f29-gate`, `r46-mutbat`, `r47-f30-gate`, `r47-routed-defects`, `shonen-form`, `shonen-form-selftest`) | **no** — no admitted spelling exists for their lane-grading mode at all (their `--selftest` mode stays admitted) | source read |
| `--root <fixture>` (e.g. the README-documented `--root corpus/instruments/limb-fixtures/fr/fr-missing-entry`) | **no** — the counter has no positional root. Capability lost *as a derive*; still available by direct exec | README:352; `--root` is the only root selector |
| `--json PATH` | **yes for the measurement** — stdout is written unconditionally and `--json` only adds a receipt (`frontier-recheck-count.py:552-560`; same shape at `citation-ground-check.py:530`) | measured: `entries=1 pass=0 exit=1` byte-identical with and without `--json` on the fixture root |
| `--scratch DIR`, `--work DIR` (where optional) | **yes** — selftest-only scratch; default `$HYAKU_SCRATCH` then `$TMPDIR` (`scratch_base`). Where `--work` is `required=True` (`r46-mutbat`, `shonen-form-selftest`) there is no admitted spelling — see the required row above | source read |
| `--out PATH`, `--url URL` | **no** — `capture-source.py` needs both to write; `wave-registry.py --out` is required. The written bytes exist as committed snapshots (`cat`/`sha256sum` derives), but that is a different derive | argparse read |
| `--output` | n/a — no counter declares it; it exists to refuse the literal token (`--out` already covers `--outp`/`--outpu` prefixes) | 0 matches over all `add_argument` calls |

### Would a committed ledger figure or control script break?

- **No committed ledger breaks.** Every committed `derive` string in the lane at
  `c1051749` (all JSON, `.git` excluded): **1132 derives, 109 python-head, 0
  base/candidate disagreements**. Only 5 committed python derives carry a denied flag
  (`round-68/w1/RevengerC1/probe-results-{py,x,xbase,z}.json`), and all 5 are
  `{F}`-template strings that **base also refuses** (brace tokenisation), so their
  verdicts do not move.
- **No committed gate/control breaks.** `figure-audit-mutbat.py` (the only live
  instrument that runs this gate's selftest) asserts `rc in (0,1)` and the prefix
  `selftest cases=` (`:106`) — it pins no count. Run against the candidate from the
  clone:

```
PRISTINE selftest_exit=0 last='selftest cases=96 failures=0'
MUT m4-drop-stale-literal-case  killed=1 last='selftest cases=95 failures=1'
MUT m6-readonly-gate-off        killed=1 last='selftest cases=96 failures=4'
MUT m7-python-confinement-off   killed=1 last='selftest cases=96 failures=4'
MUT m8-python-prefix-off        killed=1 last='selftest cases=96 failures=1'
MUT m9-python-boundary-separator-off killed=1 last='selftest cases=96 failures=1'
mutbat killed=5/5 survivors=0 invalid=0 controls=pass   exit=0
```

- The R103 pair really is pre-existing behaviour, not new refusal (non-claim check):
  `git show` base=False cand=False; `git show HEAD:g.txt -- g.txt` base=False cand=False;
  `git show HEAD:g.txt` base=True cand=True.

## 3. Real lane counters whose documented invocation the new rule refuses

51 `(counter, flag)` pairs over **32** counters (every `add_argument` whose option name is
a denied name or a proper prefix of one; scanned over `corpus/instruments/*.py`, AST-based
so fixture strings such as `r45-counters-selftest-c1.py`'s embedded
`ap.add_argument("--root"…)` are not miscounted):

```
capture-binding-check  --root --scratch        capture-source        --url --out
citation-ground-check  --root --json --scratch claim-package-check --json
freeze-check           --work                  frontier-recheck-count --root --json --scratch
gate-quote-audit       --root --json           kill-rule-check      --root --scratch --json
limb-mutation-check    --root                  mirror-containment-check --json
r44-frontier-count     --root --work           r44-routed-defects   --root --work
r45-c2-gate            --root                  r45-routed-defects   --root
r46-c1-gate            --root --work           r46-c2-gate          --root
r46-counters-selftest-c1 --work                r46-f29-gate         --root --work
r46-landing-gate       --work                  r46-mutbat           --root --work
r46-selftest-f29       --work                  r47-counters-selftest --work
r47-f30-gate           --root --work           r47-mutbat           --work
r47-routed-defects     --root --work           recheck-audit        --root --json
resolve-dispatch-check --json                  score-gap            --root
shonen-form-selftest   --root --work           shonen-form          --root
shonen-shipped-fixture-check --root --work     wave-registry        --out
```

`--output` matches **no** counter; the only real `--out` users are `capture-source.py`
and `wave-registry.py`.

Consequence for gate-mediated use, counted rather than asserted: **13 counters lose their
primary (non-`--selftest`) mode** — 11 because `--root`/`--work` is `required=True` or
`ap.error`s when absent (`r44-frontier-count`, `r44-routed-defects`, `r45-c2-gate`,
`r45-routed-defects`, `r46-c2-gate`, `r46-f29-gate`, `r46-mutbat`, `r47-f30-gate`,
`r47-routed-defects`, `shonen-form`, `shonen-form-selftest`), `wave-registry.py` because
`--out` is required, and `capture-source.py` because capture needs `--url`+`--out` (its
`--selftest` stays admitted). **2 more stay invokable but cannot be pointed at the lane
root** (`citation-ground-check`, `shonen-shipped-fixture-check`: default root is
`corpus/`). The other 8 `--root` declarers keep a flag-free spelling (§2).

### How those counters are invoked in committed gates/controls

- **Through the figure-audit gate: never with a denied flag — 0 of 1132 derives.**
  So the refusal removes no committed gate-mediated invocation.
- **Directly (bash / a control `.py` / a claims counting command): 262 invocation lines
  with a denied flag** — 33 in committed `.sh` files, 229 in `.py` files (that `.py` count
  includes usage strings and docstrings, so it is an upper bound, not an execution count).
  Per counter, `.sh` lines: `r44-frontier-count` 7, `frontier-recheck-count` 5,
  `r46-c1-gate` 4, `capture-binding-check` 3, `r46-c2-gate` 3, `r45-c2-gate` 2,
  `r45-routed-defects` 2, `r46-f29-gate` 2, `recheck-audit` 2, `capture-source` 1,
  `freeze-check` 1, `r46-landing-gate` 1 — in
  `.ufo/waves/round-{30,45,46,47,59}/controls/*.sh` and `post-commit-recheck.sh`.
  All of these exec the counter themselves; the gate is not in that path, so the rule
  does not touch them.
- The round-70 C1/C2 counting commands are unaffected: `python3
  corpus/instruments/frontier-recheck-count.py` and `python3
  corpus/instruments/capture-binding-check.py` carry no flags and parse admitted under
  both gates.

## 4. Ledger still re-derives 35/35 under the candidate

Clone at `c1051749`, `TMPDIR` in scratch, committed ledger, `--root clone`:

```
--- candidate  exit=0  FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
--- base       exit=0  FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
--- diff of the 35 FIG lines: IDENTICAL
```

(Negative control for the method: the same run against a `git archive` export with no
`.git` prints `figures=35 ok=11 stale=24 exit=1` — the ledger's `git show 32782bd:…`
figures need history, which is why the clone, not the tarball, is the receipt.)

Selftest receipts, both from scratch copies: candidate `selftest cases=96 failures=0`
exit 0; base `selftest cases=86 failures=0` exit 0 — the `+10` pin movement claimed
(`EXPECTED_CASES 86→96`) is real and the 10 new cases pass.

## 5. Residuals (scope, not widening)

The rule is an enumerated option set, as the claim states. Named, measured residuals that
remain **admitted** and still reach write/exec:

- `python3 corpus/instruments/kill-rule-check.py --instrument /tmp/x.py` — admitted, and
  `kill-rule-check.py:473` runs `[sys.executable, instrument_path, "--selftest",
  "--scratch", …]`, i.e. an admitted option reaches arbitrary python execution.
  `--row-file /tmp/rows.json` (arbitrary JSON read) is admitted too.
- `--selftest` is admitted everywhere; `frontier-recheck-count.py --selftest` runs the
  file as a subprocess (`:76`), though against its own fixtures.
- Positional arguments stay admitted (the claim says so); a counter's own writes on a
  positional path are not covered.
- Alternative interpreter spellings are not a gap: `python3.14`, `env python3 …`,
  `bash -c '…'` are all refused, by the head whitelist rather than by this rule.

Two precision notes on the claim text (narrowing, not widening):

1. The declared text says "any unique argparse abbreviation"; the code refuses **every
   proper prefix** of a denied name, including prefixes argparse would reject as
   ambiguous or undeclared (`--s` in a counter that also has `--selftest`, `--j` in a
   counter with no `--json`). Broader than declared ⇒ safe direction, but the word
   "unique" overstates the precision of the rule.
2. Short-option handling is asymmetric with the sort rule: `-o`, `-oVALUE` refused, but a
   bundle not starting with `o` (`-vo`) is admitted, and no counter declares `-o`, so the
   short limb currently refuses nothing real (it also cannot be evaded, because a
   `-o`-prefixed bundle is what argparse would read as `-o`).

## Verdict

**Widening-free.** `ADMITTED_NOW=0` over 482 derives, and structurally: only
`python_head_ok` changed, every other validator is byte-identical, and the added limb can
only return `False`. The 189 REFUSED-NOW derives are the 7 claim probes, their
spellings/abbreviations/placements, the short `-o` family, two `--root=` forms, and the
32 counters' documented denied flags. No committed ledger figure (1132 derives, 109
python-head, 0 disagreements), no committed control script, and no committed gate breaks:
the ledger still re-derives 35/35 identically to base, the candidate selftest is 96/0, and
the committed mutant battery kills 5/5 at the candidate. The real capability losses are
narrow and unused by any committed derive: deriving a counter against a **non-default
root** (`--root <fixture>`), and the primary mode of the 13 counters whose documented CLI
makes a denied flag mandatory (`--root`/`--work`/`--out`/`--url`). Every committed use of
those counters is a direct exec, not a gate-mediated derive.

Tooling: none installed or upgraded (no need); no pacman transaction attempted.
