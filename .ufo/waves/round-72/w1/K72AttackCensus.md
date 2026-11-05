# K72AttackCensus — attack on derive-head-census.py and the candidate gate's write-root claim (round-72 w1)

Seat: K72AttackCensus (leaf, read-only). Date: 2026-11-05.
Bytes under test (sha256 verified before use):
- CANDIDATE gate `corpus/instruments/figure-audit.py` (working tree, uncommitted): `b146c81a29437aef2d4e91576782a2829570ac12f13888cad099d6081d1fefdc`
- COUNTER `corpus/instruments/derive-head-census.py` (committed a34ce4c): `255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52`
- BASE gate `git show a34ce4c:corpus/instruments/figure-audit.py`: `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603`
Environment: `git clone --shared .../kasegi-shokunin $S/lane && git -C $S/lane checkout a34ce4c`; candidate gate copied in with `cp` (sha re-verified after copy). All work under `/fast/scratch/hyaku/kasegi-r72/K72AttackCensus/`; gate runs used `cwd=$S/lane`, `--root $S/lane` or a scratch fixture root; `TMPDIR=$S` on every run. No tools installed (system python3 only; nothing to record under the tooling authorization). Frozen tree has no symlinked heads: `find $S/lane/corpus/instruments -maxdepth 1 -type l | wc -l` → `0`.

Method: (a) an independent AST scan (counter-equivalent `declared_options` + substring filter out/output/work/scratch/url/json/dir/path/root) against the candidate's `PY_DENIED_ANY`/`PY_DENIED_BY_SCRIPT`/`PY_SCRIPT_CENSUS`/`PY_HEAD_REFUSED` literals; (b) an add_argument-visibility scan (non-literal option strings, alias bindings, non-Name receivers, manual argv parsing); (c) one-figure-ledger probes against the candidate gate in a scratch fixture; (d) census + selftest runs on the candidate; (e) census cross-check on base tables. 45 heads, 45 in `PY_SCRIPT_CENSUS`; `frontier-recheck-count.py` additionally in `PY_HEAD_REFUSED` (refused outright). 56 (head,flag) rows declare a substring-matching option; no other head declares any.

## (1) Enumeration: heads declaring out/output/work/scratch/url/json/dir/path/root options

A. Counter CHECKS (flag in WRITE_CLASS `("--out","--output","--work","--scratch","--url")`) — 22 pairs, candidate denies ALL 22:
`--out`: capture-source.py, wave-registry.py. `--url`: capture-source.py. `--scratch`: capture-binding-check.py, citation-ground-check.py, frontier-recheck-count.py, kill-rule-check.py. `--work`: freeze-check.py, r44-frontier-count.py, r44-routed-defects.py, r46-c1-gate.py, r46-counters-selftest-c1.py, r46-f29-gate.py, r46-landing-gate.py, r46-mutbat.py, r46-selftest-f29.py, r47-counters-selftest.py, r47-f30-gate.py, r47-mutbat.py, r47-routed-defects.py, shonen-form-selftest.py, shonen-shipped-fixture-check.py. No head declares `--output`. Independent scan: zero checked pairs admitted → READMITTED=0 corroborated.

B. Counter does NOT check, candidate DOES deny — 11 pairs (counter blind, gate covers):
`--json`: citation-ground-check.py, frontier-recheck-count.py, gate-quote-audit.py, kill-rule-check.py, mirror-containment-check.py, recheck-audit.py, resolve-dispatch-check.py. `--root`: frontier-recheck-count.py, limb-mutation-check.py, r46-c1-gate.py, recheck-audit.py.

C. Counter does NOT check, candidate does NOT deny (ADMITTED) — 23 pairs, classified:
- Read-root selectors (read-only tree pointers; the round-71 positive limb relies on admitting these): `--root` on capture-binding-check.py, citation-ground-check.py, gate-quote-audit.py, kill-rule-check.py, r44-frontier-count.py, r44-routed-defects.py, r45-c2-gate.py, r45-routed-defects.py, r46-c2-gate.py, r46-f29-gate.py, r46-mutbat.py, r47-f30-gate.py, r47-routed-defects.py, score-gap.py, shonen-form.py, shonen-form-selftest.py, shonen-shipped-fixture-check.py (17 pairs).
- Same class, differently named: `--lane-root` (census-freshness-check.py:162 — selftest copies resolve.py from it), `--fleet-root` (citation-ground-check.py:511 — comparison/JSON field only), `--cdroot` (recheck-audit.py — equality check against the audited cd target).
- `--json` stdout (store_true): claim-package-check.py:791 — the intended positive admit.
- `--timeout` (freeze-check.py:379, int) — neither read nor write root.
- Flagged for routing, NOT a C1 falsifier: freeze-check.py `--tool-root` (:376) + `--claims` (:375) + `--base` (:377) select the tree and command source for `bash -c` counter runs (freeze-check.py:67-73 `["bash","-c",cmd], cwd=tool_root`) — an exec-ingress surface admitted by the gate. The claims file itself routes this class: non_claims "the freeze-check.py bash -c exec primitive measured by SentinelC1 row 33 is NOT repaired this round; it is routed". Outside the frozen write-class set.

## (2) add_argument calls the counter cannot see

Searched all 45 heads for: first positional not an `ast` string Constant; alias binding (`x = parser.add_argument` then `x(...)`); `add_argument` reached through a non-Name receiver chain; `parse_known_args`/direct `sys.argv` option parsing. Result: ZERO non-literal option strings, ZERO alias calls, ZERO chained receivers in the frozen tree — every option string is a literal and `declared_options` sees it (it matches any receiver by `.add_argument` attribute name). Observed helper-object use, visible to the counter: r46-landing-gate.py:613 `g = ap.add_mutually_exclusive_group(required=True)`; `g.add_argument` at :614-616 (`--pre-report`, `--post-report`, `--selftest`, all store_true). Not invisible: counter keys on the attr name, not the receiver. The gate itself declares its `--ledger`/`--root` by manual argv slicing (figure-audit.py:953-965), not argparse — no option declarations for `declared_options` to miss, and neither flag is write-class. Two embedded-string `sys.argv[1]` uses are mutant-fixture code, not option declarations: limb-mutation-check.py:332 (`spec_from_file_location('limb_mutant', sys.argv[1])` — runs inside its denied `--root` flow) and r45-counters-selftest-c1.py:128 (`m = sys.argv[1]` in a generated mutant). All other argv touches are `main(sys.argv[1:])` feeding argparse. Only positional argument in the fleet: claim-package-check.py:790 `add_argument('package', nargs='?')` — a read-only package directory. Conclusion: no (head, flag) pair is invisible to the counter in the frozen tree.

## (3) `--json` heads under the candidate gate

Heads declaring `--json`: 8. Denied per-script for 7 (citation-ground-check, frontier-recheck-count, gate-quote-audit, kill-rule-check, mirror-containment-check, recheck-audit, resolve-dispatch-check — frontier-recheck-count additionally head-refused). Admitted for 1: **claim-package-check.py** (`--json` is `action='store_true'`, stdout; the round-71 positive limb).
Claim impact: **READMITTED=0 is NOT affected.** The census counts only flags exactly in WRITE_CLASS; `--json` is not in it, so neither the 7 denials nor the 1 admit moves READMITTED. The frozen claim's predicate is keyed on the claims-file write-class set, so an extra write-class NAME (e.g. a future head whose `--json` takes a path with no `PY_DENIED_BY_SCRIPT` entry) would be invisible to BOTH the counter and `PY_DENIED_ANY` — a real routing for the next round, not a defect of this round's bytes. Today each of the 7 path-writing `--json` heads carries its per-script entry, so there is no current exposure.

## (4) Argparse abbreviation and spelling surfaces (measured, one-figure ledger per probe)

Fixture: candidate gate + 5 heads copied to `$S/probe/corpus/instruments`; probe = `figure-audit.py --ledger <1 figure> --root $S/probe`, cwd=fixture, `TMPDIR=$S`. Verbatim outputs:
```
PROBE derive=python3 corpus/instruments/capture-source.py --wor s/wor.txt rc=2 REFUSED tail=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
PROBE derive=python3 corpus/instruments/citation-ground-check.py --js cj.json rc=2 REFUSED tail=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
PROBE derive=python3 corpus/instruments/wave-registry.py --out=o.txt rc=2 REFUSED tail=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
PROBE derive=python3 corpus/instruments/wave-registry.py --o=o.txt rc=2 REFUSED tail=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
PROBE derive=python3 corpus/instruments/capture-binding-check.py --ro . rc=1 ADMITTED tail=
PROBE derive=python3 corpus/instruments/claim-package-check.py . -- --json out/x.json rc=1 ADMITTED tail=
```
Reading: any `--` token whose name equals or is a non-empty (>2 char) prefix of a denied flag is refused (`--wor`→`--work`, `--js`→`--json`, `--o`→`--out`), including the `=` form. The rule is a superset of argparse's unique-abbreviation resolution, so no abbreviation of a denied flag slips through. The one ADMITTED abbreviation, `--ro` on capture-binding-check, resolves to `--root`, which is deliberately not denied for that head (positive limb; the gate's own selftest pins the same pair as `s-pyrootab` on recheck-audit and `s-pyoutab` on capture-source, both refused). Single-dash forms: the only single-dash options declared anywhere are `-v` (r46-counters-selftest-c2.py:463) and `-v/--verbose` (r46-selftest-f29.py:809), both store_true, non-write; no single-dash write-class spelling exists to abuse. Post-`--` separator: the gate admits the derive (designed: operands after `--`; selftest pin `s-pydashdash` `ok.py -- --root` want_exit=0 "a counter may still receive a dash-named positional argument"), and the head then cannot bind them as options — direct run `claim-package-check.py . -- --json out/x.json` → `error: unrecognized arguments: --json out/x.json`, rc=2; through the gate: `FIG probe recorded=0 derived=UNAVAILABLE reason=derive-exit-2 stale` (gate rc=1), fixture `out/` empty — no write executed, and the fleet's only positional is a read path. **No head accepts a write-class abbreviation the gate's rule misses.**

## (5) Verdict

Frozen predicate (claims.json C1): "the derive gate's python-head policy denies every write-class option a head declares, keyed on the head the derive actually resolves to"; expected counter output READMITTED=0, ALIAS-PROBE refused, POSITIVE 2/2, CENSUS-RESULT ok; selftest failures=0 with ≥107 cases.

**C1 attack: HOLDS on frozen predicate.**
Measured:
```
$ cd $S/lane && TMPDIR=$S python3 corpus/instruments/derive-head-census.py
CENSUS heads=45 write_class_pairs=5 READMITTED=0
ALIAS-PROBE verdict=refused rc=2 FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=probe
POSITIVE admitted=2/2
CENSUS-RESULT ok
$ cd $S/lane && TMPDIR=$S python3 corpus/instruments/figure-audit.py --selftest | tail -1
selftest cases=110 failures=0
$ ... derive-head-census.py --gate corpus/instruments/base-figure-audit.py   # base tables
CENSUS heads=46 write_class_pairs=5 READMITTED=19   (+ 19 READMITTED-ROW lines)
```
The base run's 19 READMITTED-ROW lines are byte-identical to the do-nothing control receipt `controls/c1-census-donothing-r72.txt` (same heads/flags; base gate sha and counter sha in the receipt match my verified copies). Independent cross-checks: my AST scan (not the counter's code) finds zero admitted WRITE_CLASS pairs; the realpath alias probe refused; the four new R72 global write-root limbs are pinned in the selftest (`python-work`/`python-scratch` cases within cases=110).
Falsifying example: searched and found none. Strongest near-misses, both measured and both outside the predicate: (i) post-`--` denied-flag spellings are admitted at gate level but become head operands (`s-pydashdash` pin; probe 6, `derive-exit-2`, no write, fleet's only positional is read-only); (ii) freeze-check `--tool-root`/`--claims` exec ingress is admitted but is not a write-class option and is already routed in claims non_claims.

Residual risk / verification gaps:
- The census's `probes()` copies the gate bytes from the DIRECTORY of `--gate` (`here = os.path.dirname(gate)`), not from the `--gate` file itself, so a `--gate <other-gate>` run pairs the other gate's static tables with the directory's `figure-audit.py` behavioural bytes (my base run showed candidate behavioural limbs: ALIAS-PROBE refused, POSITIVE 2/2, while READMITTED=19 came from base tables). Counter robustness note for a future round; the committed receipt ran the base bytes in place and shows the true base behaviour (ALIAS-PROBE admitted).
- "Admitted" ≠ "figure passed": an admitted derive whose head fails yields stale rc=1, not refusal (probe 5/6 observed). This is designed fail-closed bookkeeping; a write-capable flag admitted would have executed, so admission is the correct refusal boundary for C1.
- Item-3 routing stands: a future path-writing `--json` (or any new write-root name outside WRITE_CLASS) needs a `PY_DENIED_BY_SCRIPT` entry AND a WRITE_CLASS/wide-census update; neither counter nor `PY_DENIED_ANY` would see it today.

Scratch `/fast/scratch/hyaku/kasegi-r72/K72AttackCensus` deleted after writing this report; no lane file was modified (the candidate gate copy inside `$S/lane` lived only in my scratch clone).

Report: .ufo/waves/round-72/w1/K72AttackCensus.md
