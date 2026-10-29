VERDICT: HOLDS

# R46bW2MutLanding — mutation test of the landing gate (round 46, attempt 2, wave 2)

Scope: one wave item. Attacked artifact: `corpus/instruments/r46-landing-gate.py` at the frozen tree `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (sha256 `2c31138639dd621e6ab95c7800a3993ad0cb87579e5895b6612bfdf27d00e9ab`, identical to the working-tree file). `git ls-tree -r --name-only fe0f56b… corpus/instruments | grep -iE 'land|gate'` lists no attempt-2 successor, so the attempt-1-era file is the artifact under attack. Commit `93140c1` is the last commit touching it.

## Method (what was run)

1. Pristine export: `git archive fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 corpus/instruments/r46-landing-gate.py | tar -x -C <scratch>`; the export's sha256 matched the working tree.
2. Pristine self-test: `python3 pristine.py --selftest --work <scratch>/work` → `selftest cases=30 failures=0` (this is the do-nothing baseline for the self-test).
3. Mutants: 13 single-edit mutants plus 2 controls, generated from the pristine export by exact-string replacement with `src.count(old) == 1` and `out != src` asserted for every edit. `py_compile` passes for all. `diff` line counts: each mutant differs from pristine by one replaced line (or one deleted line for A1); X0 differs by 0 lines.
4. Fixtures: 18 independent fixture pairs, each built from scratch under `mktemp -d` inside the scratch directory (`git init -q` for lane and fleet, a bare `origin.git`, `symbolic-ref HEAD refs/heads/master`, pushes, fixed committer/author dates). Every fixture is run through both `--pre-report` and `--post-report` with pristine and with each mutant. The clean fixture `P-clean` is green in both modes (`landing-gate mode=post-report checks=7 fail=0 exit=0`; pre `checks=4 fail=0 exit=0`). Each defect fixture is red under pristine for the defect it names (e.g. `dirty-tracked`, `unpushed-ahead-of-remote`, `two-shonen`, `committer-date-inversion`, `final-hash-not-tip`, `tip-moved-after-report`, `non-ancestor-hash`, `report-missing`, …).
5. Kill rule: a mutant is KILLED if its gate output differs from pristine's on any fixture/mode (exit code or check pass bit), OR any of its own self-test cases fail. A control is clean only if it produces zero differences and the self-test stays at `failures=0`.

Scratch was removed on exit. Re-run recipe: the anchors below plus the fixture list above reproduce the table; no artifact is cited from scratch.

## Per-mutant results

| id | single edit (anchor count = 1) | self-test failures (of 30) | exit-level red→green fixtures (pristine exit 1 → mutant exit 0) | verdict-level flips | verdict |
|---|---|---|---|---|---|
| A1 drop-tree-clean-check | delete the `checks.append(("tree-clean", …))` line | 3 | `dirty-tracked/pre`, `untracked-file/pre` | 2 (the other 16 differ only by the removed tree-clean line and the `checks=4`→`checks=3` summary; no other verdict changes) | KILLED |
| A2 tree-clean-ignores-porcelain | `("tree-clean", rc == 0 and n == 0,` → `("tree-clean", rc == 0,` | 2 | `dirty-tracked/pre`, `untracked-file/pre` | 2 | KILLED |
| B1 drop-ls-remote-equality-pre | `bool(remote) and remote == local` → `bool(remote)` | 2 | `unpushed-ahead-of-remote/pre` | 1 | KILLED |
| B2 drop-ls-remote-equality-post | `bad = [short(h) for h in finals if h != tip]` → `bad = []` | 2 | `final-hash-not-tip/post`, `tip-moved-after-report/post` | 3 | KILLED |
| C1 accept-two-shonen | `("shonen-heading", n == 1,` → `("shonen-heading", n <= 2,` | 4 | `two-shonen/post`, `zero-shonen/post` | 3 | KILLED |
| C2 accept-zero-shonen | `("shonen-heading", n == 1,` → `("shonen-heading", n <= 1,` | 2 | `zero-shonen/post` | 2 | KILLED |
| D1 drop-jj-state | `("jj-state", a == 0 and t == 0 and u == 0,` → `("jj-state", True,` | 3 | `jj-state-ahead/pre` | 1 | KILLED |
| D2 placeholder-count-ignored | `ok = ok and c == 0` → `ok = ok and c >= 0` | 4 | `placeholder-scorecard-backtick/pre`, `placeholder-lesson-bare/pre` | 2 | KILLED |
| D3 scorecard-not-strict | `("SCORECARD.md", True)` → `("SCORECARD.md", False)` | 1 | `placeholder-scorecard-backtick/pre` | 1 | KILLED |
| E1 drop-date-order | `ok = not unreadable and worst_ct <= lim` → `ok = not unreadable` | 1 | `committer-date-inversion/post` | 1 | KILLED |
| E2 drop-ancestor | `("ancestor", bool(cites) and not bad,` → `("ancestor", True,` | 5 | `non-ancestor-hash/post` | 4 | KILLED |
| G1 drop-resolves | `("resolves", bool(cites) and not bad,` → `("resolves", True,` | 3 | none | 3 | KILLED (check level and self-test only) |
| H1 report-missing-ignored | `checks.append(("report-readable", False, …))` → `…True, …` | 1 | none | 1 | KILLED (check level and self-test only) |
| X0 control: do-nothing (identity) | none | 0 | none | 0 | clean (control) |
| X1 control: equivalent (trailing comment on `TABLE_SEP`) | comment appended | 0 | none | 0 | clean (control) |

Results: 13 of 13 non-equivalent mutants are KILLED; both controls are clean (zero fixture differences, self-test `failures=0`). The three named mutants from the item: drop the cleanliness check = A1 (and A2); drop the ls-remote equality = B1 (pre-report) and B2 (post-report); accept two SHONEN headings = C1.

## Quoted outputs (verbatim from the run)

Pristine, clean fixture, post-report:
```
check report-readable pass=1 read=bytes=228
check cited-hashes pass=1 read=n=2,final=1
check resolves pass=1 read=unresolved=0
check ancestor pass=1 read=non-ancestor=0
check final-is-tip pass=1 read=final-not-tip=0,tip=6474bdd947a2(ls-remote)
check date-order pass=1 read=latest-cited=6474bdd947a2@2023-11-14T22:15:00Z,report-commit-committer=2023-11-14T22:16:50Z
check shonen-heading pass=1 read=count=1
landing-gate mode=post-report checks=7 fail=0 exit=0
```

A1 (tree-clean check deleted), fixture `dirty-tracked`, pre-report: pristine `check tree-clean pass=0 read=porcelain-lines=1` / `landing-gate mode=pre-report checks=4 fail=1 exit=1`; mutant `landing-gate mode=pre-report checks=3 fail=0 exit=0`. Same flip on `untracked-file`.

A2 (`rc == 0` only), fixture `dirty-tracked`, pre: mutant `check tree-clean pass=1 read=porcelain-lines=1` / `landing-gate mode=pre-report checks=4 fail=0 exit=0`.

B1 (`bool(remote)` only), fixture `unpushed-ahead-of-remote`, pre: pristine `check remote-tip pass=0 read=remote=6474bdd947a2,local=212f0a9f179f` / `exit=1`; mutant `check remote-tip pass=1 read=remote=6474bdd947a2,local=212f0a9f179f` / `landing-gate mode=pre-report checks=4 fail=0 exit=0`.

B2 (post tip equality dropped), fixture `tip-moved-after-report`, post: pristine `check final-is-tip pass=0 read=final-not-tip=6474bdd947a2,tip=2d36becd04a2(ls-remote)` / `exit=1`; mutant `check final-is-tip pass=1 read=final-not-tip=0,tip=2d36becd04a2(ls-remote)` / `exit=0`.

C1 (`n <= 2`), fixture `two-shonen`, post: pristine `check shonen-heading pass=0 read=count=2` / `landing-gate mode=post-report checks=7 fail=1 exit=1`; mutant `check shonen-heading pass=1 read=count=2` / `landing-gate mode=post-report checks=7 fail=0 exit=0`. Self-test under C1: `selftest case=cli-two-shonen exit=0 last=landing-gate_mode=post-report_checks=7_fail=0_exit=0 verdict=fail` plus `post-two-shonen-headings` and `post-zero-shonen-headings` failing.

Self-test counts under mutants (`selftest cases=30 failures=F`): A1 F=3, A2 F=2, B1 F=2, B2 F=2, C1 F=4, C2 F=2, D1 F=3, D2 F=4, D3 F=1, E1 F=1, E2 F=5, G1 F=3, H1 F=1, X0 F=0, X1 F=0.

## Findings

1. No survivor. Every non-equivalent mutant produces a verdict difference on at least one of the 18 fixtures, and the frozen gate's own self-test catches every one of them. The gate's named checks (tree-clean, remote-tip, shonen-heading, plus jj-state, placeholders, date-order, ancestor, final-is-tip) each carry a fixture that goes red→green when the check is removed.
2. Two checks are shadowed at the exit-code level (G1, H1). For `unresolvable-hash`, the `resolves` check goes red and the mutant still exits 1 because `ancestor` also fails (the ancestor expression requires `resolved[h]`), so `resolves` is only enforced by its per-check line and by the self-test case `post-unresolvable-hash`. For `report-missing`, `report-readable` is likewise shadowed by the other six checks. Neither is a break of the item's named mutants; both mean the exit code alone would not notice these two checks being dropped. This is a coverage observation, not a claim of defect.
3. The controls discriminate: X0 (identity) and X1 (equivalent comment) produce zero differences on all 36 gate runs each and self-test `failures=0`, so the harness is not trivially red.
4. The `--tip` replay override path of `final-is-tip` was not exercised by any fixture (the item's named mutants do not touch it).

## Limitations

- The `jj-lane.sh state` call was replaced by a per-fixture stub that prints `ahead=N tracked=0 untracked=0`; the real `scripts/hyaku/jj-lane.sh` was not run against a fixture. D1's kill depends on the stub's output format matching the gate's regex, which it does by construction.
- Fixtures are my own construction (independent of the gate's `make_ctx`), 18 pairs; mutants are single-edit by exact anchor. The item's "fixture pair" is read as: the defect fixture that the named check exists to catch, against pristine, with the verdict difference as the kill signal. Kill semantics are stated above; no other reading was tested.
- No equivalence proof beyond the one comment control; no mutation of the `--tip` path, of `commit_all`/selftest fixtures inside the gate, or of the `git()` read-only guard.
- No live target, no credentials, no commits, no changes to git/jj/index, no shared production files touched.
- Tooling: none installed; `git 2.56.0` and `Python 3.14.8` were used as found.
