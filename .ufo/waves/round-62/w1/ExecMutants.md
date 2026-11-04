# ExecMutants — round 62 predata

Axes: **depth:verifiability**, **coverage**. Runnable draft complete; base is deliberately red. No production instrument changes or claim freeze; no sandbox claim.

## Deliverables

All paths below are relative to the lane root:

- `.ufo/waves/round-62/w1/ExecMutants/figure-audit-mutbat.py`: standalone five-mutant battery, accepting `--instrument /absolute/path`; default is sibling `figure-audit.py` for eventual production placement.
- `.ufo/waves/round-62/w1/ExecMutants/prefix-boundary-witness.py`: reproducible, non-executing direct-gate proof that the two added mutants are non-equivalent on base.
- `.ufo/waves/round-62/w1/ExecMutants/baseline-battery.txt`: actual command, instrument SHA, pristine/equivalent outcomes, all five mutant outputs and exit1.
- `.ufo/waves/round-62/w1/ExecMutants/baseline-witness.txt`: actual command, all variant hashes and nine gate observations, exit0.
- `.ufo/waves/round-62/w1/ExecMutants/setup.txt`: guarded clone setup, checked toplevel before detached checkout, versions and constraints.

## Behavior and measured controls

Base: `f7dcab84b104ccc03083fa1ad8c38e12830d25c9`. Its instrument SHA256 is `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`.

| variant | selftest exit | summary | classification |
|---|---:|---|---|
| pristine | 0 | cases24 failures0 | held |
| equivalent trailing space | 0 | cases24 failures0 | held |
| m4 drop stale-literal case | 1 | cases23 failures1 | killed by case pin |
| m6 readonly gate off | 1 | cases24 failures4 | killed |
| m7 Python confinement off | 1 | cases24 failures2 | killed |
| m8 Python prefix off | 0 | cases24 failures0 | **survives** |
| m9 Python boundary separator off | 0 | cases24 failures0 | **survives** |

Actual battery summary: `mutbat killed=3/5 survivors=2 invalid=0 controls=pass`, exit1. Each mutation site occurred exactly once and compiled. Original three mutant identities/edits and pristine/trailing-space controls remain. Added m8/m9 are the exact round61 survivor edits:

- m8 removes only the literal-prefix condition, retaining the length guard. Hash `336cabbc73af4053ab80279cab601fd36b327f7c9e5e2e6881a1314cf2e5d8aa`.
- m9 changes `return target.startswith(base + os.sep)` to `return target.startswith(base)`. Hash `e83dd9d5bc080a82a81b4a93ce3d1785f55bf1090a23822432b325c870662af9`.

Direct witnesses reproduce pristine absolute-inside=False/sibling-prefix=False; m8 absolute-inside=True; m9 sibling-prefix=True. Same-directory stays False throughout. These are gate-only witnesses, not executed escape payloads. Their hashes exactly match the filed round61 report.

Exact commands and full outputs are retained in the two baseline receipts. Core baseline invocation, cwd `/fast/scratch/hyaku/kasegi-r62/ExecMutants`:

```sh
env TMPDIR=/fast/scratch/hyaku/kasegi-r62/ExecMutants/tmp PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-62/w1/ExecMutants/figure-audit-mutbat.py --instrument /fast/scratch/hyaku/kasegi-r62/ExecMutants/clone/corpus/instruments/figure-audit.py
```

## Candidate coordination and integration command

Read ExecArgv's draft after its direct availability message. Its decoded-argv `python_head_ok(root, parts)` retains exact prefix and separator anchors; stale-literal case also remains. Its generic-head expression changes from `return head.startswith(READ_ONLY_HEADS)` to `return parts[0] in READ_ONLY_HEADS`. The final battery explicitly recognizes these two known anchors and requires exactly ONE occurrence across both, then uses that exact-once site for m6 and trailing-space control. It never silently skips an unrecognized profile. This compatibility selection was added after the retained baseline measurement; no final-draft or candidate rerun is claimed.

The battery rejects unusable/duplicate sites, syntax-invalid mutants and infrastructure exits instead of crediting them as kills. Mutants must return selftest exit1 with a selftest-summary line; pristine/equivalent must return0. Timeout/error exits fail closed. Scratch is cleaned by its context manager. This is a selftest discriminator, not independent proof of every gate limb or runtime confinement.

L1 should run the final draft once against the integrated instrument, with TMPDIR and HYAKU_SCRATCH pointing to a newly created L1-owned guarded scratch directory:

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-62/w1/ExecMutants/figure-audit-mutbat.py --instrument /absolute/integrated/corpus/instruments/figure-audit.py
```

Expected acceptance is five valid kills, zero survivors/invalids, both controls held and battery exit0; **not measured here**. The witness script intentionally uses base's string-head API and is not a candidate gate witness. Do not run it against decoded-argv code without adapting its caller.

## Scope, limits and cleanup

Read round61 lesson, non-author verifier spotcheck, QUALITY applicable record criteria and SCORECARD planned62. No tests/full suites, linters, formatters, C2 source checks, named r61 shell runner replay or live network were run. Only assigned baseline battery and direct-gate witnesses were executed. Candidate integration verification belongs to L1.

No production writes beyond this exclusive report/draft directory; no sibling edits, commits, pushes, fleet/index/bookmark mutations or external substrate changes. No background jobs/subagents. Scratch `/fast/scratch/hyaku/kasegi-r62/ExecMutants` removed using `rm -rf --` (exit0) before delivery. No tool installs/updates; available Python3.14.8 and git2.56.0 sufficed. Pacman remained paused. LSP unavailable in mounted tool inventory; symbol inspection used read/grep.

Risks: mutation anchors are deliberately exact and may need coordinated changes if the final candidate moves them. Baseline receipt predates the compatibility-selector-only addition. Selftest mutation detection does not establish a sandbox; m4 is a count-pin kill. No blocker to delivering this draft; integrated green outcome remains unmeasured.

Self-evaluation: accuracy4 (full base receipts, no candidate result inferred); completeness4 (scoped five-mutant draft complete, integration remains parent-owned); clarity4 (controls separated from survivor findings); actionability4 (explicit interface/anchors/commands, scratch must be recreated); conciseness4 (retained raw outputs avoid repeated phase transcripts). Overall4.0. Highest-impact next action is the parent's integrated five-kill run. A user should agree because no unexercised candidate result is represented as observed.
